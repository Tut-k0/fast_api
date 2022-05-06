from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = "197f18d71bb9d02914b321fb5a2903b43f9315602af8047adf2c9ee4ba91ed0f"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    token = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return token
