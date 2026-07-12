from sqlalchemy.orm import Session
from models.user import User
from utils.hash import hash_password, verify_password
from utils.jwt import create_token

def create_user(db: Session, email: str, password: str):
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        return None

    user = User(
        email=email,
        password_hash=hash_password(password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return user

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()

    if not user or not verify_password(password, user.password_hash):
        return None

    token = create_token({"user_id": user.id, "email": user.email})
    return token
