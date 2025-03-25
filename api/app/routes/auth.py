from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..crud.user import authenticate_user, create_user, get_user_by_email
from ..schemas.schemas import Token, UserCreate, User
from ..auth.utils import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    get_current_active_user,
    get_db
)
from ..monitoring import app_logger, auth_success_total, auth_failure_total, create_span

router = APIRouter(
    prefix="/auth",
    tags=["authentication"]
)

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    app_logger.info(f"Tentative de connexion: {form_data.username}")
    
    with create_span("authenticate_user_flow"):
        user = authenticate_user(db, form_data.username, form_data.password)
        
        if not user:
            app_logger.warning(f"Échec d'authentification: {form_data.username}")
            # Incrémenter le compteur d'échecs d'authentification
            auth_failure_total.labels(method="password", reason="invalid_credentials").inc()
            
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Incrémenter le compteur de succès d'authentification
        auth_success_total.labels(method="password").inc()
        
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        
        app_logger.info(f"Utilisateur connecté avec succès: {user.email}")
        return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", response_model=User)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    app_logger.info(f"Tentative d'inscription: {user.email}")
    
    with create_span("register_user_flow"):
        db_user = get_user_by_email(db, email=user.email)
        if db_user:
            app_logger.warning(f"Échec d'inscription - email déjà enregistré: {user.email}")
            auth_failure_total.labels(method="register", reason="email_already_registered").inc()
            
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        created_user = create_user(db=db, user=user)
        auth_success_total.labels(method="register").inc()
        
        app_logger.info(f"Utilisateur inscrit avec succès: {user.email}")
        return created_user

@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    app_logger.debug(f"Récupération du profil utilisateur: {current_user.email}")
    return current_user
