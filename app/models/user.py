from app import db, bcrypt
from datetime import datetime, timezone

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(254), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(120), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    
    def set_password(self, password: str):
        self.password_hash = bcrypt.generate_password_hash(password=password).decode("utf-8")
    
    def check_password(self, password: str) -> bool:
        return bcrypt.check_password_hash(pw_hash=self.password_hash, password=password)
    
    @classmethod
    def create(cls, email:str, name:str, password:str):
        user = cls(email=email.lower().strip(), name=name)
        user.set_password(password)
        return user
        