from sqlalchemy import  ForeignKey, VARCHAR, text, func
from sqlalchemy.dialects.postgresql import UUID, TEXT, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional
from models import ModelBase, CampaignMembers
from datetime import datetime

#models follow tables under DBQueries docs, refer SQLalchemy ORM documentation
class Campaigns(ModelBase):
    #table metadata
    __tablename__ = "campaigns"
    #mapped column function provides extra constraints and information about the field relating to the DDL
    campaign_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True),primary_key= True,server_default=text("gen_random_uuid()"))
    title: Mapped[str] = mapped_column(VARCHAR(100),nullable=False)
    description: Mapped[Optional[str]] = mapped_column(TEXT)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.current_timestamp())
    #Foreign key constraint takes text SQL referencing another table attribute
    created_by: Mapped[UUID] = mapped_column(ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    
    #Many-to-One Relationship, 1 user can have many campaigns
    user = relationship("Users", back_populates="campaigns")
    campaign_members = relationship()
    def __repr__(self):
        return f"""Campaign:
            campaign_id - {self.campaign_id}
            Title - {self.title}
            Description - {self.description}
            Created_By - {self.created_by}
            Owner_Email - {self.user.email}\n"""

    
#Basic DTO Method
def campaign_to_dict(campaign:Campaigns)->dict:
    return {
        "campaign_id": campaign.campaign_id,
        "title":campaign.title,
        "description":campaign.description,
        "created_at":campaign.created_at,
        "created_by":campaign.created_by
    }