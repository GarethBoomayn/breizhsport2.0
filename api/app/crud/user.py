from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from passlib.context import CryptContext
from ..models.models import User
from ..schemas.schemas import UserCreate, UserUpdate
from ..monitoring import app_logger, db_queries_total, db_query_duration_seconds, create_span
import time

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_user(db: Session, user_id: int) -> User | None:
    app_logger.debug(f"Recherche de l'utilisateur avec ID: {user_id}")
    start_time = time.time()
    
    with create_span("db_get_user_by_id"):
        user = db.query(User).filter(User.id == user_id).first()
    
    # Enregistrer la métrique
    db_queries_total.labels(
        operation="select",
        table="users"
    ).inc()
    
    duration = time.time() - start_time
    db_query_duration_seconds.labels(
        operation="select",
        table="users"
    ).observe(duration)
    
    return user

def get_user_by_email(db: Session, email: str) -> User | None:
    app_logger.debug(f"Recherche de l'utilisateur avec email: {email}")
    start_time = time.time()
    
    with create_span("db_get_user_by_email"):
        user = db.query(User).filter(User.email == email).first()
    
    # Enregistrer la métrique
    db_queries_total.labels(
        operation="select",
        table="users"
    ).inc()
    
    duration = time.time() - start_time
    db_query_duration_seconds.labels(
        operation="select",
        table="users"
    ).observe(duration)
    
    return user

def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
    app_logger.debug(f"Récupération des utilisateurs - skip: {skip}, limit: {limit}")
    start_time = time.time()
    
    with create_span("db_get_users"):
        users = db.query(User).offset(skip).limit(limit).all()
    
    # Enregistrer la métrique
    db_queries_total.labels(
        operation="select",
        table="users"
    ).inc()
    
    duration = time.time() - start_time
    db_query_duration_seconds.labels(
        operation="select",
        table="users"
    ).observe(duration)
    
    return users

def create_user(db: Session, user: UserCreate) -> User:
    # Vérifier si l'email existe déjà
    if get_user_by_email(db, user.email):
        app_logger.warning(f"Tentative de création d'un utilisateur avec un email déjà existant: {user.email}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Créer l'utilisateur
    app_logger.info(f"Création d'un nouvel utilisateur: {user.email}")
    start_time = time.time()
    
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        username=user.username,
        full_name=user.full_name,
        hashed_password=hashed_password
    )
    
    try:
        with create_span("db_create_user"):
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
        
        # Enregistrer la métrique
        db_queries_total.labels(
            operation="insert",
            table="users"
        ).inc()
        
        duration = time.time() - start_time
        db_query_duration_seconds.labels(
            operation="insert",
            table="users"
        ).observe(duration)
        
        app_logger.info(f"Utilisateur créé avec succès: {user.email}")
        return db_user
    except IntegrityError:
        db.rollback()
        app_logger.warning(f"Échec de création d'utilisateur - nom d'utilisateur déjà existant: {user.username}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

def update_user(db: Session, user_id: int, user: UserUpdate) -> User:
    app_logger.info(f"Mise à jour de l'utilisateur avec ID: {user_id}")
    db_user = get_user(db, user_id)
    if not db_user:
        app_logger.warning(f"Tentative de mise à jour d'un utilisateur inexistant: {user_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    start_time = time.time()
    
    # Mettre à jour les champs modifiables
    if user.email is not None:
        # Vérifier si le nouvel email n'est pas déjà utilisé
        existing_user = get_user_by_email(db, user.email)
        if existing_user and existing_user.id != user_id:
            app_logger.warning(f"Tentative de mise à jour avec un email déjà existant: {user.email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        db_user.email = user.email
    
    if user.username is not None:
        db_user.username = user.username
    if user.full_name is not None:
        db_user.full_name = user.full_name
    if user.password is not None:
        db_user.hashed_password = get_password_hash(user.password)
    
    try:
        with create_span("db_update_user"):
            db.commit()
            db.refresh(db_user)
        
        # Enregistrer la métrique
        db_queries_total.labels(
            operation="update",
            table="users"
        ).inc()
        
        duration = time.time() - start_time
        db_query_duration_seconds.labels(
            operation="update",
            table="users"
        ).observe(duration)
        
        app_logger.info(f"Utilisateur mis à jour avec succès: {user_id}")
        return db_user
    except IntegrityError:
        db.rollback()
        app_logger.warning(f"Échec de mise à jour - nom d'utilisateur déjà existant: {user.username}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

def delete_user(db: Session, user_id: int) -> User:
    app_logger.info(f"Suppression de l'utilisateur avec ID: {user_id}")
    db_user = get_user(db, user_id)
    if not db_user:
        app_logger.warning(f"Tentative de suppression d'un utilisateur inexistant: {user_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    start_time = time.time()
    
    with create_span("db_delete_user"):
        db.delete(db_user)
        db.commit()
    
    # Enregistrer la métrique
    db_queries_total.labels(
        operation="delete",
        table="users"
    ).inc()
    
    duration = time.time() - start_time
    db_query_duration_seconds.labels(
        operation="delete",
        table="users"
    ).observe(duration)
    
    app_logger.info(f"Utilisateur supprimé avec succès: {user_id}")
    return db_user

def authenticate_user(db: Session, email: str, password: str) -> User | None:
    app_logger.info(f"Tentative d'authentification pour: {email}")
    start_time = time.time()
    
    with create_span("authenticate_user"):
        user = get_user_by_email(db, email)
        
        if not user:
            app_logger.warning(f"Échec d'authentification - utilisateur non trouvé: {email}")
            return None
            
        if not verify_password(password, user.hashed_password):
            app_logger.warning(f"Échec d'authentification - mot de passe incorrect: {email}")
            return None
    
    duration = time.time() - start_time
    db_query_duration_seconds.labels(
        operation="authenticate",
        table="users"
    ).observe(duration)
    
    app_logger.info(f"Authentification réussie pour: {email}")
    return user
