from sqlalchemy.orm import DeclarativeBase
from .campaignModel import Campaigns
from .userModel import Users

class ModelBase(DeclarativeBase):
    pass