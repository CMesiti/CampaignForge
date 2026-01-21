from sqlalchemy import text, select, update, delete, insert
from sqlalchemy.orm import Session, selectinload
from models import Users, Campaigns, ModelBase, user_to_dict