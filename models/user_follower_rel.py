from models.base_model import BaseModel
from models.user import User    
import peewee as pw
from playhouse.hybrid import hybrid_property

class UserFollowerRel(BaseModel):
    following=pw.ForeignKeyField(User,backref='followers',on_delete='CASCADE')
    follower=pw.ForeignKeyField(User,backref='followings',on_delete='CASCADE')
    is_approved= pw.BooleanField(default=True)
