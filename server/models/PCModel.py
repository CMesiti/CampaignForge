from sqlalchemy.dialects.postgresql import JSONB, UUID, ARRAY, ENUM, VARCHAR, TIMESTAMP, INTEGER
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey, func, text
from datetime import datetime
from models import ModelBase

# potential import - class JSONB.Comparator
# inherits from sqlalchemy.dialects.postgresql.json.Comparator
# Define comparison operations for JSON.


#All characters for all campaigns and their associated users.
class PlayerCharacters(ModelBase):
    __tablename__ = "player_characters"


    character_id:Mapped[UUID] =  mapped_column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    campaign_id:Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("campaigns.campaign_id", ondelete="CASCADE"), nullable = False)
    user_id:Mapped[UUID] = mapped_column(UUID(as_uuid=True),ForeignKey("users.user_id", ondelete="CASCADE"), nullable = False)
    character_name:Mapped[str] = mapped_column(VARCHAR(50), nullable = False)
    character_class:Mapped[dict] = mapped_column(JSONB)
    character_stats:Mapped[dict] = mapped_column(JSONB)
    character_level:Mapped[int] = mapped_column(INTEGER)
    character_hitpoints:Mapped[int] = mapped_column(INTEGER)
    created_at:Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.current_timestamp())
    #declare table columns, dtypes, and mappings. 

    def __repr__(self):
        return f"""
                character_id - {self.character_id}
                campaign_id - {self.campaign_id}
                user_id - {self.user_id}
                character_name - {self.character_name}
                character_stats - {self.character_stats}
                character_level - {self.character_level}
                character_hitpoints - {self.character_hitpoints}
                created_at - {self.created_at}
                """

def pc_to_dict(pc:PlayerCharacters):
    pass