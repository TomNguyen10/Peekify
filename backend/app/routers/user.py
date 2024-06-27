from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from data.postgresql import get_db
from models.user import User
from schemas.user import UserCreate, User as UserSchema

router = APIRouter()


def get_user_by_spotify_id(db: Session, spotify_user_id: str):
    return db.query(User).filter(User.spotify_user_id == spotify_user_id).first()


def create_user(db: Session, user: UserCreate):
    db_user = User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post("/users/", response_model=UserSchema)
def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_spotify_id(db, user.spotify_user_id)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    return create_user(db, user)
