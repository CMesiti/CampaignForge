from sqlalchemy import text, select, update, delete, insert
from config.db import db
from sqlalchemy.orm import Session, selectinload
from models import Users, user_to_dict
from services.util import hash_pass, check_pass

#class holds CRUD
class ServiceError(Exception):
    pass
#db.session is our session obj, 
# Calling the Session.scalars() method is the equivalent to calling upon 
# Session.execute() to receive a Result object, then calling upon Result.scalars() to receive a ScalarResult object.
class UserService:
    def get_user_data(self):
        #this is a eager loading technique solving the N+1 Query problem
        stmt = select(Users).options(selectinload(Users.campaigns))
        #scalars returns list of objs and execute returns list of rows
        users_ls = db.session.scalars(stmt).all()
        return [user_to_dict(user) for user in users_ls]
    
    def register_new_user(self, user_data:dict) -> list:
        if "email" not in user_data:
            raise ServiceError("Missing Email")
        if "password" not in user_data:
            raise ServiceError("Missing Password")
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
            raise ServiceError("Email Taken")
        if len(pswd) <= 12:
            raise ServiceError("Password must be 12 or more chars")
        elif " " in pswd or pswd.isalnum():
            raise ServiceError("Must contain special character and no spaces")
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
    
    def update_existing_user(self, user_id, updates):
        pswd = updates.get("password", None)
        display_name = updates.get("display_name", None)
        if pswd:
            #add password constraints
            if len(pswd) <= 12:
                raise ServiceError("Password must be 12 or more chars")
            elif pswd.isalnum() or " " in pswd:
                raise ServiceError("Must contain special character and no spaces")
            #hash and store
            hash = hash_pass(pswd)
            #get user
            user = db.session.get(Users, user_id)
            user.pass_hash = hash
            db.session.commit()
            return user_to_dict(user)
        elif display_name:
            if len(display_name) > 50:
                raise ServiceError("Name must be less than 50 chars")
            elif " " in display_name:
                raise ServiceError("No Spaces Allowed")
            user = db.session.get(Users, user_id)
            user.display_name = display_name
            db.session.commit()
            return user_to_dict(user)
        else:
            raise ServiceError("Missing Update Information")
    def remove_existing_user(self, user_id, pswd):
        user = db.session.get(Users, user_id)
        if not pswd:
           raise ServiceError("Password Required")
        is_valid, e = check_pass(pswd, user.pass_hash)
        if not is_valid:
            raise ServiceError(f"Validation Error {e}")
        db.session.delete(user)
        db.session.commit()
        return user_to_dict(user)