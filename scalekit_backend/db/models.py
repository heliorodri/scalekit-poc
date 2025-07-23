from scalekit_backend.db import db

class UserCredentials(db.Model):
    __tablename__ = 'user_credentials'
    id = db.Column(db.Integer, primary_key=True)
    access_token = db.Column(db.String(255))
    id_token = db.Column(db.String(255))
    refresh_token = db.Column(db.String(255))
    scalekit_user_id = db.Column(db.String(255))
    # Add more fields as needed

    def __init__(self, access_token, id_token, refresh_token, scalekit_user_id):
        self.access_token = access_token
        self.id_token = id_token
        self.refresh_token = refresh_token
        self.scalekit_user_id = scalekit_user_id