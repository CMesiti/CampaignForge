from server.config.db import db
from server.services.util import ServiceError
from flask_jwt_extended import get_jwt_identity
from sqlalchemy import select, update
from server.models.playerCharModel import PlayerCharacters, pc_to_dict

#**ADD jwt verification, only user_ids enrolled in the requested campaign can perform these actions.***
class PlayerService:
    #get all player characters under a specific campaign
    def get_campaign_players(self, campaign_id):
        stmt = select(PlayerCharacters).where(PlayerCharacters.campaign_id == campaign_id)
        player_characters = db.session.scalars(stmt).all()
        #we need DTO for player character object
        return [pc_to_dict(pc) for pc in player_characters]
    
    def get_user_characters(self, campaign_id):
        #Get all players under the current user in specific campaign.
        current_user = get_jwt_identity()
        stmt = select(PlayerCharacters).where(PlayerCharacters.campaign_id == campaign_id,
                                              PlayerCharacters.user_id == current_user)
        player_characters = db.session.scalars(stmt).all()
        if not player_characters:
            raise ServiceError("Invalid Character")
        return [pc_to_dict(pc) for pc in player_characters]

    def create_new_player(self, player_data, campaign_id):
        #validate player data
        name = player_data.get("character_name", None)
        level = player_data.get("character_level", None)
        classes = player_data.get("character_class", None)
        stats = player_data.get("character_stats", None)
        hitpoints = player_data.get("character_hitpoints", None)
        if not all([name, level, classes, stats, hitpoints]):
            raise ServiceError("Missing required player fields.")
        current_user = get_jwt_identity()
        #check if already exists
        stmt = select(PlayerCharacters).where(PlayerCharacters.character_name == name)
        existing_player = db.session.scalars(stmt).first()
        if existing_player:
            raise ServiceError("Already Existing Character")
        new_player = PlayerCharacters(
            campaign_id = campaign_id,
            user_id = current_user, 
            character_name = name,
            character_level = level,
            character_class = classes,
            character_stats = stats,
            character_hitpoints = hitpoints
        )
        db.session.add(new_player)
        db.session.commit()
        return pc_to_dict(new_player)
    
    def update_existing_player(self, updates, character_id):
        #check for existing character
        #limit updates to specific fields
        current_user = get_jwt_identity()
        allowed_fields = {"character_name", 
                          "character_level", 
                          "character_class", 
                          "character_stats", 
                          "character_hitpoints"}
        for k in updates.keys():
            if k not in allowed_fields:
                raise ServiceError(f"Invalid Update request: {k}")
        existing_player = db.session.get(PlayerCharacters, character_id)
        if not existing_player:
            raise ServiceError("Invalid Character")
        if str(existing_player.user_id) != current_user:
            raise ServiceError("Unauthorized Access")
        if not updates:
            raise ServiceError("No Update Arguments")
        for key, val in updates.items(): #must ensure request schema
            setattr(existing_player, key, val)
        db.session.commit()
        return pc_to_dict(existing_player)
    
    def delete_existing_player(self, character_id):
        current_user = get_jwt_identity()
        existing_player = db.session.get(PlayerCharacters, character_id)
        if not existing_player:
            raise ServiceError("Invalid Character")
        if str(existing_player.user_id) != current_user:
            raise ServiceError("Unauthorized Access")
        db.session.delete(existing_player)
        db.session.commit()
        

