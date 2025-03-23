from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from ..models.models import Category
from ..schemas.schemas import CategoryCreate, CategoryUpdate
from typing import List, Optional

def get_categories(db: Session, skip: int = 0, limit: int = 100) -> List[Category]:
    return db.query(Category).offset(skip).limit(limit).all()

def get_category(db: Session, category_id: int) -> Optional[Category]:
    return db.query(Category).filter(Category.id == category_id).first()

def get_category_by_name(db: Session, name: str) -> Optional[Category]:
    return db.query(Category).filter(Category.name == name).first()

def create_category(db: Session, category: CategoryCreate) -> Category:
    try:
        db_category = Category(
            name=category.name,
            description=category.description
        )
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Category already exists")

def update_category(db: Session, category_id: int, category: CategoryUpdate) -> Category:
    try:
        db_category = get_category(db, category_id)
        if db_category is None:
            raise HTTPException(status_code=404, detail="Category not found")
        
        if category.name is not None:
            existing_category = get_category_by_name(db, category.name)
            if existing_category and existing_category.id != category_id:
                raise HTTPException(status_code=400, detail="Category name already exists")
            db_category.name = category.name
        if category.description is not None:
            db_category.description = category.description
        
        db.commit()
        db.refresh(db_category)
        return db_category
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Category name already exists")

def delete_category(db: Session, category_id: int) -> Category:
    db_category = get_category(db, category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Vérifier si la catégorie a des produits associés
    if db_category.products:
        raise HTTPException(
            status_code=400,
            detail="Impossible de supprimer une catégorie qui contient des produits"
        )
    
    db.delete(db_category)
    db.commit()
    return db_category
