from sqlalchemy import text, select, update, delete, insert
from config.db import db
from sqlalchemy.orm import Session, selectinload
from models import Users, user_to_dict
from util import hash_pass, check_pass

#class holds CRUD
class ServiceError(Exception):
    pass

class UserService:
    def get_user_data():
        #this is a eager loading technique solving the N+1 Query problem
        db.session.select(Users).options(selectinload(Users.campaigns))
        #scalars returns list of objs and execute returns list of rows
        users_ls = db.session.scalars(stmt).all()
        return [user_to_dict(user) for user in users_ls]
    
    def register_new_user(user_data:dict) -> list:
        if "email" not in user_data:
            raise "Missing Email"
        if "password" not in user_data:
            raise "Missing Password"
        if "display_name" not in user_data:
            user_data["display_name"] = user_data["email"].split('@')[0]
        pswd = user_data["password"]
        email = user_data["email"]
        display_name = user_data["display_name"]
        #Assign and Commit New User
        email_stmt = select(Users).where(Users.email == email)
        rows = db.session.scalars(email_stmt).first()
        print(rows)
        if rows:
            raise "Email Taken"
        if len(pswd) <= 12:
            raise "Password must be 12 or more chars"
        elif " " in pswd or pswd.isalnum():
            raise "Must contain special character and no spaces"
        newUser = Users()
        newUser.email = email
        newUser.pass_hash = hash_pass(pswd)
        newUser.display_name = display_name
        #Add_all adds list of objects, commit method flushes pending transactions and commits to user_database.
        db.session.add(newUser)
        db.session.commit()
        #after flush we assign server defaults to obj
        created_user = [user_to_dict(newUser)]
        return created_user
        

        