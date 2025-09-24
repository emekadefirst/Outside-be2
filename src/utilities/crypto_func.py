import jwt
from argon2 import PasswordHasher
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta, timezone
from fastapi import Depends, status
from jwt import ExpiredSignatureError, InvalidTokenError, decode
from src.apps.auth.models import User
from typing import Dict
from src.utilities.errorHandler import ErrorMessage
from src.config.env import (
    JWT_ACCESS_EXPIRY,
    JWT_REFRESH_EXPIRY,
    JWT_ACCESS_SECRET,
    JWT_ALGORITHM,
)

error = ErrorMessage(User)


class JWTService:
    @staticmethod
    def generate_token(subject: str) -> dict:
        now = datetime.now(timezone.utc)

        access_exp = now + timedelta(minutes=JWT_ACCESS_EXPIRY)
        refresh_exp = now + timedelta(days=JWT_REFRESH_EXPIRY)

        user_id = subject.get("user_id")  

        access_payload = {
            "sub": str(user_id),
            "exp": access_exp,
            "type": "access"
        }

        refresh_payload = {
            "sub": str(user_id),
            "exp": refresh_exp,
            "type": "refresh"
        }

        access_token = jwt.encode(access_payload, JWT_ACCESS_SECRET, algorithm=JWT_ALGORITHM)
        refresh_token = jwt.encode(refresh_payload, JWT_ACCESS_SECRET, algorithm=JWT_ALGORITHM)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }

    @staticmethod
    def decode_token(token: str):
        try:
            payload = jwt.decode(token, JWT_ACCESS_SECRET, algorithms=[JWT_ALGORITHM])
            return payload
        except jwt.JWTError:
            return None

    @staticmethod
    def refresh_token(refresh_token: str) -> Dict[str, str]:
        """
        Validates refresh token and issues a new pair of tokens.
        """
        payload = JWTService.decode_token(refresh_token)

        if payload.get("type") != "refresh":
            raise error.unauthorized("Invalid token type")

        user_id = payload.get("sub")   # sub is just the user_id string
        return JWTService.generate_token(user_id)

    @staticmethod
    def get_subject(token: str) -> str:
        payload = JWTService.decode_token(token)
        if not payload:
            raise error.unauthorized("Invalid or expired token")
        return payload.get("sub")
    
    @staticmethod
    async def get_current_user(
        token: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    ):
        from src.apps.auth import User  # <--- Local import
        from src.utilities.errorHandler import ErrorMessage
        error = ErrorMessage(User)

        try:
            payload = decode(
                token.credentials, JWT_ACCESS_SECRET, algorithms=[JWT_ALGORITHM]
            )
            user_id: str = payload.get("sub")
            if not user_id:
                raise error.unauthorized("Invalid authentication credentials")
            
            user = await User.get_or_none(id=user_id)
            if not user:
                raise error.unauthorized("User not found or invalid token")
            
            return user

        except (ExpiredSignatureError, InvalidTokenError):
            raise error.unauthorized("Token is expired or invalid")
