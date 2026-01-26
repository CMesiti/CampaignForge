from sqlalchemy.dialects.postgresql import JSONB, UUID, ARRAY, ENUM, VARCHAR, TIMESTAMP
from models import ModelBase
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey
from datetime import datetime


class PlayerCharacters(ModelBase):
    __tablename__ = "player_characters"
    character_id:Mapped[UUID]
    campaign_id:Mapped[UUID]
    user_id:Mapped[UUID]
    character_name:Mapped[str]
    character_class:Mapped[dict]
    character_stats:Mapped[dict]
    character_level:Mapped[int]
    character_hitpoints:Mapped[int]
    created_at:Mapped[datetime]
    #declare table columns, dtypes, and mappings. 