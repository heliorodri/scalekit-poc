from scalekit_backend.db import db
from scalekit_backend.db.models import UserCredentials

class UserCredentialRepository:
    def __init__(self):
        self.db = db

    def get(self, scalekit_user_id):
        return UserCredentials.query.filter_by(scalekit_user_id=scalekit_user_id).first()
    
    def create(self, user_credentials: UserCredentials):
        self.db.session.add(user_credentials)
        self.db.session.commit()