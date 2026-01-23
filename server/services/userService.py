from sqlalchemy import text, select, update, delete, insert
from flask import g
from sqlalchemy.orm import Session, selectinload
from models import Users, ModelBase, user_to_dict
from config.db import get_connection
from util import hash_pass, check_pass
#class holds CRUD
class UserService:
    def __init__(self):
        self.db = g.db
    def get_user_data(self):
        with Session(self.db) as session:
            #this is a eager loading technique solving the N+1 Query problem
            stmt = select(Users).options(selectinload(Users.campaigns))
            #scalars returns list of objs and execute returns list of rows
            users_ls = session.scalars(stmt).all()
            return [user_to_dict(user) for user in users_ls], "GET Successful"
    
    def register_new_user(self, user_data):
        if "email" not in user_data:
            return "","Missing Email"
        if "password" not in user_data:
            return "","Missing Password"
        if "display_name" not in user_data:
            user_data["display_name"] = user_data["email"].split('@')[0]
        pswd = user_data["password"]
        email = user_data["email"]
        display_name = user_data["display_name"]
        #Assign and Commit New User
        with Session(self.db) as session:
            email_stmt = select(Users).where(Users.email == email)
            rows = session.scalars(email_stmt).first()
            print(rows)
            if rows:
                return "","Email Taken"
            if len(pswd) <= 12:
                return "","Password must be 12 or more chars"
            elif pswd.isalnum() or " " in pswd:
                return "","Must contain special character and no spaces"
            newUser = Users()
            newUser.email = email
            newUser.pass_hash = hash_pass(pswd)
            newUser.display_name = display_name
            #Add_all adds list of objects, commit method flushes pending transactions and commits to user_database.
            session.add(newUser)
            session.commit()
            #after flush we assign server defaults to obj
            created_user = user_to_dict(newUser)
        return created_user,"Created User Successfully"
        

        