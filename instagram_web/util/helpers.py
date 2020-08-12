import boto3,botocore
from app import app
import braintree
from flask_login import current_user

s3 = boto3.client(
    's3',
    aws_access_key_id=app.config['S3_KEY'],
    aws_secret_access_key=app.config['S3_SECRET']
)
def upload_file_to_s3(file,username, acl='public-read'):
    try:
        s3.upload_fileobj(
            file,
            app.config.get('S3_BUCKET'),
            "{}/{}".format(username,file.filename),
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )
    except Exeption as e:
        # This is a catch all exception, edit this part to fit your needs.
        print("Something Happened: ", e)
        return e
    return "{}/{}".format(username, file.filename)

gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id=app.config['BT_MERC'],
        public_key=app.config['BT_PUB'],
        private_key=app.config['BT_PRIV']
    )
)

def generate_client_token():
    return gateway.client_token.generate()

def transact(options):
    return gateway.transaction.sale(options)

def find_transaction(id):
    return gateway.transaction.find(id)

def check_user(user_id):
    return current_user.id==int(user_id)