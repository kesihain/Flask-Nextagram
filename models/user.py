from models.base_model import BaseModel
import peewee as pw
from playhouse.hybrid import hybrid_property
from werkzeug.security import generate_password_hash
import re
from flask_login import UserMixin

class User(UserMixin,BaseModel):
    username = pw.CharField(unique=True,null=False)
    email = pw.CharField(unique=True,null=False)
    password_hash=pw.TextField(null=False)
    password = None
    image_path = pw.TextField(null=True)
    is_private=pw.BooleanField(default=False)

    @hybrid_property
    def full_image_path(self):
        if self.image_path:
            from app import app
            return app.config.get("S3_LOCATION") + self.image_path
        else:
            return ""

    @hybrid_property
    def fans(self):
        current_list=self.followers
        user_list=[]
        for item in current_list:
            user_list.append(item.follower.id)
        return user_list

    @hybrid_property
    def idols(self):
        current_list=self.followings
        user_list=[]
        for item in current_list:
            user_list.append(item.following.id)
        return user_list
    
    def follow(self,fan):
        from models.user_follower_rel import UserFollowerRel
        if fan.is_private:
            UserFollowerRel.create(following=self,follower=fan,is_approved=False)
        else:
            UserFollowerRel.create(following=self,follower=fan,is_approved=True)

    def unfollow(self,idol):
        from models.user_follower_rel import UserFollowerRel
        UserFollowerRel.delete().where((UserFollowerRel.follower==self.id), (UserFollowerRel.following==idol.id)).execute()

    def validate(self):
        # Unique email
        existing_user_email= User.get_or_none(User.email==self.email)
        if existing_user_email and existing_user_email.id != self.id:
            self.errors.append(f"Email {self.email} already in use!")
        existing_user_username = User.get_or_none(User.username==self.username)
        if existing_user_username and existing_user_username.id != self.id:
            self.errors.append(f"Username {self.username} already in use!")
        if self.password:
            if len(self.password)<6:
                self.errors.append(f"Password is less that 6 characters")
            has_lower = re.search(r"[a-z]",self.password)
            has_upper = re.search(r"[A-Z]",self.password)
            has_special = re.search(r"[\[ \] \* \$ \% \^ \& \# \? ]", self.password)
            if not (has_lower and has_upper and has_special):
                self.errors.append(f"Password needs to have a combination of lowercase, uppercase and special characters")  
            if len(self.errors)==0:
                self.password_hash=generate_password_hash(self.password)
    
    # def check_username(self,username):
    #     return get_or_none(User.username==username)
    # def check_email(self,email):
    #     return get_or_none(User.email==email)
    
