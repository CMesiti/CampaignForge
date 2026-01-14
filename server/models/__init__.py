from sqlalchemy.orm import DeclarativeBase

class ModelBase(DeclarativeBase):
    pass

from .campaignModel import Campaigns
from .userModel import Users