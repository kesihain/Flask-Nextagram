from models.base_model import BaseModel
import peewee as pw
from werkzeug.security import generate_password_hash
import re
from flask_login import UserMixin

class User(UserMixin,BaseModel):
    username = pw.CharField(unique=True,null=False)
    email = pw.CharField(unique=True,null=False)
    password_hash=pw.TextField(null=False)
    password = None

    def validate(self):
        self.password_hash=generate_password_hash(self.password)
        # Unique email
        if User.get_or_none(User.email==self.email):
            self.errors.append(f"Email {self.email} already in use!")
        if User.get_or_none(User.username==self.username):
            self.errors.append(f"Username {self.username} already in use!")
        if len(self.password)<6:
            self.errors.append(f"Password is less that 6 characters")
        has_lower = re.search(r"[a-z]",self.password)
        has_upper = re.search(r"[A-Z]",self.password)
        has_special = re.search(r"[\[ \] \* \$ \% \^ \& \# \? ]", self.password)
        if not (has_lower and has_upper and has_special):
            self.errors.append(f"Password needs to have a combination of lowercase, uppercase and special characters")    
    
    # def check_username(self,username):
    #     return get_or_none(User.username==username)
    # def check_email(self,email):
    #     return get_or_none(User.email==email)
    
