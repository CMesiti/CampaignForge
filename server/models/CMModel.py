from sqlalchemy.dialects.postgresql import JSONB, UUID, ARRAY, ENUM, VARCHAR, TIMESTAMP
from models import ModelBase
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey
from datetime import datetime
class CampaignMembers(ModelBase):
    __tablename__ = "campaign_members"


    campaign_id:Mapped[UUID]
    user_id: Mapped[UUID]
    user_role: Mapped[dict]
    joined_at: Mapped[datetime]
    
    #declare table columns, dtypes, and mappings
