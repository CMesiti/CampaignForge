from sqlalchemy import VARCHAR, text, func
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional
from models import ModelBase, campaign_to_dict
from datetime import datetime

#models follow tables under DBQueries docs
class Users(ModelBase):
    #table metadata
    __tablename__ = "users"
    #Python Dtypes = SQL Dtypes - Mapping
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key = True, server_default=text("gen_random_uuid()")) 
    #Mapped type hints, conversion python to database types
    email: Mapped[str] = mapped_column(VARCHAR(355), unique=True, nullable=False )
    pass_hash: Mapped[str] = mapped_column(VARCHAR(200), nullable=False)
    display_name: Mapped[Optional[str]] = mapped_column(VARCHAR(50))
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default = func.current_timestamp())
    #One-to-Many Relationship
    campaigns = relationship("Campaigns", back_populates = "user")

    def __repr__(self)->str:
        return f"""USER: 
        user_id - {self.user_id},
        email - {self.email},
        display_name - {self.display_name}\n"""
    


def user_to_dict(user)->dict:
    return {"user_id":user.user_id, 
            "email":user.email, 
            "display_name":user.display_name, 
            "created_at": user.created_at,
            "campaigns": [campaign_to_dict(campaign) for campaign in user.campaigns]}




    