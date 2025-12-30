from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.user import User
from app.core.security import hash_password, verify_password
from app.core.jwt import create_access_token


class AuthService:
    @staticmethod
    def register_user(db: Session, email: str, password: str) -> User:
        exists = db.query(User).filter(User.email == email).first()
        if exists:
            raise HTTPException(status_code=400, detail="Email ya registrado")

        new_user = User(
            email=email,
            hashed_password=hash_password(password)
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> str:
        user = db.query(User).filter(User.email == email).first()
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=400, detail="Credenciales inválidas")

        token = create_access_token({"sub": str(user.id)})
        return token