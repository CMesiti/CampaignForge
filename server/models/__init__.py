from sqlalchemy.orm import DeclarativeBase

class ModelBase(DeclarativeBase):
    pass

from .campaignModel import Campaigns, campaign_to_dict
from .userModel import Users, user_to_dict