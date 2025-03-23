from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ..crud import product as product_crud
from ..schemas.schemas import Product, ProductCreate
from ..database.config import get_db

router = APIRouter(
    prefix="/products",
    tags=["products"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=Product, status_code=201)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    """
    Créer un nouveau produit avec les informations suivantes :
    - name: Nom du produit
    - description: Description du produit
    - price: Prix du produit
    - stock: Quantité en stock
    - category_id: ID de la catégorie
    - image_url: URL de l'image du produit (optionnel)
    """
    return product_crud.create_product(db=db, product=product)

@router.get("/", response_model=List[Product])
def read_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    category_id: Optional[int] = Query(None, description="Filtrer par catégorie"),
    db: Session = Depends(get_db)
):
    """
    Récupérer la liste des produits.
    - Pagination avec skip et limit
    - Filtrage optionnel par catégorie
    """
    products = product_crud.get_products(
        db, 
        skip=skip, 
        limit=limit,
        category_id=category_id
    )
    return products

@router.get("/{product_id}", response_model=Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    """
    Récupérer un produit par son ID
    """
    db_product = product_crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.put("/{product_id}", response_model=Product)
def update_product(
    product_id: int,
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    """
    Mettre à jour un produit existant
    """
    return product_crud.update_product(
        db=db,
        product_id=product_id,
        product_data=product
    )

@router.delete("/{product_id}", response_model=Product)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """
    Supprimer un produit
    """
    return product_crud.delete_product(db=db, product_id=product_id)
