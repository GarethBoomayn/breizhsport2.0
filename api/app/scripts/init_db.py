from sqlalchemy.orm import Session
from ..models.models import Category, Product
from ..database.config import SessionLocal

def init_db():
    db = SessionLocal()
    try:
        # Vérifier si des données existent déjà
        if db.query(Category).count() > 0:
            print("La base de données contient déjà des données. Initialisation ignorée.")
            return

        # Créer les catégories
        categories = [
            Category(name="Football", description="Équipement de football"),
            Category(name="Basketball", description="Équipement de basketball"),
            Category(name="Tennis", description="Équipement de tennis"),
            Category(name="Running", description="Équipement de course à pied"),
            Category(name="Fitness", description="Équipement de fitness et musculation")
        ]
        
        db.add_all(categories)
        db.commit()

        # Créer les produits
        products = [
            # Football
            Product(
                name="Ballon de football Nike Strike",
                description="Ballon de football pour terrain synthétique",
                price=24.99,
                stock=100,
                category_id=1,
                image_url="https://example.com/ball.jpg"
            ),
            Product(
                name="Chaussures de football Adidas Predator",
                description="Chaussures de football pour terrain sec",
                price=89.99,
                stock=50,
                category_id=1,
                image_url="https://example.com/shoes.jpg"
            ),
            # Basketball
            Product(
                name="Ballon de basketball Spalding NBA",
                description="Ballon officiel NBA",
                price=29.99,
                stock=75,
                category_id=2,
                image_url="https://example.com/basketball.jpg"
            ),
            Product(
                name="Panier de basketball portable",
                description="Panier réglable en hauteur",
                price=199.99,
                stock=20,
                category_id=2,
                image_url="https://example.com/hoop.jpg"
            ),
            # Tennis
            Product(
                name="Raquette Wilson Pro Staff",
                description="Raquette de tennis professionnelle",
                price=199.99,
                stock=30,
                category_id=3,
                image_url="https://example.com/racket.jpg"
            ),
            Product(
                name="Balles de tennis Head Tour",
                description="Lot de 4 balles de tennis",
                price=9.99,
                stock=200,
                category_id=3,
                image_url="https://example.com/tennis-balls.jpg"
            ),
            # Running
            Product(
                name="Chaussures Nike Air Zoom",
                description="Chaussures de running légères",
                price=129.99,
                stock=60,
                category_id=4,
                image_url="https://example.com/running-shoes.jpg"
            ),
            Product(
                name="Montre GPS Garmin Forerunner",
                description="Montre connectée pour running",
                price=299.99,
                stock=25,
                category_id=4,
                image_url="https://example.com/watch.jpg"
            ),
            # Fitness
            Product(
                name="Tapis de yoga premium",
                description="Tapis antidérapant 6mm",
                price=39.99,
                stock=150,
                category_id=5,
                image_url="https://example.com/yoga-mat.jpg"
            ),
            Product(
                name="Set d'haltères ajustables",
                description="Paires d'haltères 2-20kg",
                price=149.99,
                stock=40,
                category_id=5,
                image_url="https://example.com/dumbbells.jpg"
            ),
        ]
        
        db.add_all(products)
        db.commit()
        
        print("Base de données initialisée avec succès!")
        print(f"Catégories créées : {len(categories)}")
        print(f"Produits créés : {len(products)}")
        
    except Exception as e:
        print(f"Erreur lors de l'initialisation de la base de données : {e}")
        db.rollback()
    finally:
        db.close()
