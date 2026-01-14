from sqlalchemy import String, ForeignKey, TIMESTAMP, VARCHAR, text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import List, Optional
from datetime import datetime, date

#models follow tables under DBQueries docs
class Base(DeclarativeBase):
    pass

class Users(Base):
    #table metadata
    __tablename__ = "users"
    #Python Dtypes = SQL Dtypes - Mapping
    user_id: Mapped[UUID] = mapped_column(primary_key = True, server_default=text("get_random_uuid()")) 
    #Mapped type hints, conversion python to database types
    email: Mapped[str] = mapped_column(VARCHAR(355), unique=True, nullable=False )
    pass_hash: Mapped[str] = mapped_column(VARCHAR(200), nullable=False)
    display_name: Mapped[Optional[str]] = mapped_column(VARCHAR(50))
    created_at: Mapped[str] = mapped_column(server_default = func.current_timestamp())

    def __repr__(self)->str:
        return f"USER: user_id - {self.user_id}, email - {self.email}, display_name - {self.display_name}"
    





    