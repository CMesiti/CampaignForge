from server.models import Campaigns, CampaignMembers, campaign_to_dict
from sqlalchemy import select
from server.services.util import ServiceError
from server.config.db import db #import db variable
from flask_jwt_extended import get_jwt_identity
from server.models.campaignMemModel import Role

class CampaignService():

    def get_campaigns(self):
        current_user = get_jwt_identity()
        stmt = select(CampaignMembers).where(CampaignMembers.user_id == current_user)
        campaign_members = db.session.scalars(stmt).all()
        user_campaigns = [campaign_to_dict(cm.campaign) for cm in campaign_members]
        return user_campaigns
    
    def get_campaign_by_id(self, campaign_id):
        current_user = get_jwt_identity()
        campaign = db.session.get(Campaigns, campaign_id)
        if not campaign:
            raise ServiceError(f"Cannot Find Campaign with ID: {campaign_id}")
        #only allow DM to get the campaign information. 
        member = db.session.get(CampaignMembers, (campaign_id, current_user))
        
        if not member:
            raise ServiceError(f"Not Enrolled in Campaign {campaign_id}")
        if member.user_role != Role.DM:
            raise ServiceError("Unauthorized User Must be DM")
        return campaign_to_dict(campaign)
    
    def create_new_campaign(self, campaign_data):
        title = campaign_data.get("title", None)
        description = campaign_data.get("description", None) #not required
        if not title:
            raise ServiceError("Missing Title")
        current_user = get_jwt_identity()
        #create new object
        #we use flask sql alchemy statements or 
        #execute ORM statements with session.scalars or execute 
        #scalars are 'ORM Objects' and execute are row objects
        campaign = Campaigns(title=title, description=description, created_by=current_user)
        db.session.add(campaign)
        db.session.commit()
        db.session.flush()
        campaign_member = CampaignMembers(
            campaign_id=campaign.campaign_id, 
            user_id = current_user,
            user_role = Role.DM)
        db.session.add(campaign_member)
        db.session.commit()
        return campaign_to_dict(campaign)
    
    def enroll_user(self, campaign_id):
        current_user = get_jwt_identity()
        #check if user already exists as a member
        existing_member = db.session.get(CampaignMembers, (campaign_id, current_user))
        existing_campaign = db.session.get(Campaigns, campaign_id )
        if existing_member:
            raise ServiceError("Already enrolled in campaign")
        if not existing_campaign:
            raise ServiceError("Invalid Campaign ID")
        campaign_member = CampaignMembers(
            campaign_id = campaign_id,
            user_id = current_user,
            user_role = "Player"
        )
        db.session.add(campaign_member)
        db.session.commit()
        
    def remove_user(self, campaign_id, user_id):
        current_user = get_jwt_identity
        campaign = db.session.get(Campaigns, campaign_id)
        if not campaign:
            raise ServiceError("Invalid Campaign ID")
        if str(campaign.created_by) != current_user:
            raise ServiceError("Unauthorized Access")
        existing_member = db.session.get(CampaignMembers, (campaign_id, user_id))
        if not existing_member:
            raise ServiceError("No existing user")
        db.session.delete(existing_member)
        db.session.commit()

    def update_existing_campaign(self, updates, campaign_id):
        title = updates.get("title", None)
        description = updates.get("description", None)
        current_user = get_jwt_identity()
        campaign = db.session.get(Campaigns, campaign_id)
        if not campaign:
            raise ServiceError("Invalid Campaign ID")
        if campaign.created_by != current_user:
            raise ServiceError("Unauthorized Access")
        if title:
            campaign.title = title
        if description:
            campaign.description = description
        db.session.commit()
        return campaign_to_dict(campaign)

    def delete_existing_campaign(self, campaign_id):
        #verify that the user deleting is created by
        current_user = get_jwt_identity()
        campaign = db.session.get(Campaigns, campaign_id)
        if not campaign:
            raise ServiceError("Invalid Campaign ID")
        if str(campaign.created_by) != current_user:
            raise ServiceError("Unauthorized Access")
        db.session.delete(campaign)
        db.session.commit()
        return campaign_to_dict(campaign)

