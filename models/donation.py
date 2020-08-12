from models.base_model import BaseModel
import peewee as pw
from models.user import User
from models.image import Image

class Donation(BaseModel):
    user_id=pw.ForeignKeyField(User,backref='donations', on_delete="CASCADE")
    image_id=pw.ForeignKeyField(Image,backref='donations', on_delete="CASCADE")
    amount = pw.DecimalField()