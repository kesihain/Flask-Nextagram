import peewee as pw
from models.base_model import BaseModel
from models.user import User
from playhouse.hybrid import hybrid_property

class Image(BaseModel):
    user_id=pw.ForeignKeyField(User,backref='images', on_delete="CASCADE")
    image_path=pw.TextField(unique=True,null=False)

    @hybrid_property
    def full_image_path(self):
        from app import app
        return app.config.get("S3_LOCATION")+self.image_path