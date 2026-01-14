from sqlalchemy import String, ForeignKey, TIMESTAMP, VARCHAR, text, func
from sqlalchemy.dialects.postgresql import UUID, TEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional
from models import ModelBase

#models follow tables under DBQueries docs
class Campaigns(ModelBase):
    #table metadata
    __tablename__ = "campaigns"
    campaign_id: Mapped[UUID] = mapped_column(primary_key= True, server_default = text("gen_random_uuid()"))
    title: Mapped[str] = mapped_column(VARCHAR(100), nullable= False)
    description: Mapped[Optional[str]] = mapped_column(TEXT)
    created_at: Mapped[TIMESTAMP] = mapped_column(server_default=func.current_timestamp())
    #Foreign key constraint takes text SQL referencing another table attribute
    created_by: Mapped[UUID] = mapped_column(ForeignKey("users.user_id"))


    def __repr__(self):
        return f"""Campaign:
            campaign_id - {self.campaign_id}
            Title - {self.title}
            Description - {self.description}
            Created_By - {self.created_by}"""
