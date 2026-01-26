from sqlalchemy.dialects.postgresql import JSONB, UUID, ARRAY, ENUM, VARCHAR
from models import ModelBase
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey

class CampaignMembers(ModelBase):
    __tablename__ = "campaign_members"

    #declare table columns, dtypes, and mappings
