import os
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from app.core.config import settings

# Utilizes python libraries to create and decode unique access tokens for authentication purposes (mainly used for S3)
SECRET_KEY = settings.JWT_SECRET_KEY 
ALGORITHM = settings.JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_HOURS = settings.ACCESS_TOKEN_EXPIRE_HOURS

def create_access_token(team_id):
    now = datetime.now(timezone.utc)
    payload = {
        "sub" : team_id,
        "iat" : int(now.timestamp()),
        "exp" : int((now + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)).timestamp()),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        team_id = payload.get("sub")
        if not team_id:
            raise ValueError("Missing sub")
        return team_id
    except (JWTError, ValueError):
        raise