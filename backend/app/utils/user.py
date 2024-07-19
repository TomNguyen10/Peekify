from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate


def get_user_by_spotify_id(db: Session, spotify_user_id: str):
    return db.query(User).filter(User.id == spotify_user_id).first()


def create_user(db: Session, user: UserCreate):
    db_user = User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: str, user_update: UserCreate):
    db_user = get_user_by_spotify_id(db, user_id)
    for key, value in user_update.model_dump(exclude_unset=True).items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user
