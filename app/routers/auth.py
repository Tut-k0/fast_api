from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import models, oauth
from ..database import get_db
from ..utils import verify_password

router = APIRouter(tags=['Authentication'])


@router.post('/login')
def login(credentials: OAuth2PasswordRequestForm = Depends(),
          db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.email == credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Invalid credentials.")

    if not verify_password(credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Invalid credentials.")

    # Create and Return Token
    token = oauth.create_access_token(data={"user_id": user.id})
    return {"access_token": token, "token_type": "bearer"}