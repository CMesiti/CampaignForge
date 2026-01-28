from sqlalchemy.orm import DeclarativeBase

class ModelBase(DeclarativeBase):
    pass

from .campaignModel import Campaigns, campaign_to_dict
from .userModel import Users, user_to_dict
from .CMModel import CampaignMembers, cm_to_dict
from .PCModel import PlayerCharacters, pc_to_dict