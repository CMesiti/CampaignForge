from sqlalchemy.dialects.postgresql import JSONB, UUID, ARRAY, ENUM, VARCHAR, TIMESTAMP
from models import ModelBase, Users, Campaigns
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey, text
from datetime import datetime



#classic many to many association table
class CampaignMembers(ModelBase):
    __tablename__ = "campaign_members"

    #declare table columns, dtypes, and mappings
    campaign_id:Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("campaigns.campaign_id", ondelete="CASCADE"), primary_key=True)
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True),ForeignKey("users.user_id", ondelete="CASCADE"), primary_key = True)
    user_role: Mapped[dict] = mapped_column(ENUM(('DM', 'Player', 'Viewer'), name = "USER_ROLE"))
    joined_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))

    
    user: Mapped["Users"] = relationship("Users", back_populates="campaign_members")
    campaign: Mapped["Campaigns"] = relationship("Campaigns", back_populates="campaign_members") 
    
    def __repr__(self):
        return f"""
            campaign_id - {self.campaign_id}
            user_id - {self.user_id}
            user_role - {self.user_role}
            joined_at - {self.joined_at}
            """


def cm_to_dict(cpm_member:CampaignMembers):
    pass