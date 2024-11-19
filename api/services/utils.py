# utils.py
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from api.models.getdb import get_db
from api.models.create_db import User

def validate_email_in_url(email: str, db: Session = Depends(get_db)) -> User:
    """Valide si un utilisateur avec l'email donné existe dans la base."""
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé.")
    return user
