from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from database import engine
import database_models
from models import Product
from database import session
from sqlalchemy.orm import Session
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"]
)
database_models.Base.metadata.create_all(bind = engine)
# run with  uvicorn main:app --reload 
@app.get("/")
def greet():
    return "Hello"

products = [
    Product(id=1,name="iPhone",description="Expensive Phone with features you won't use anyway", price=999.99, quantity=20),
    Product(id=2,name="macBook",description="Expensive Laptop that can't run most apps and games", price=1999.99, quantity=10),
    Product(id=4,name="iPad",description="Expensive tablet that can actually be good for artists", price=899.99, quantity=30),
]

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

def init_db():
    db = session()
    count = db.query(database_models.Product).count
    if count != 0:
        return
    for product in products:
        db.add(database_models.Product(**product.model_dump()))

    db.commit()

init_db()

@app.get("/product")
def get_all_products(db: Session = Depends(get_db)):
    db_products = db.query(database_models.Product).all()
    return db_products

@app.get("/product/{id}")
def get_product_by_id(id:int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        return db_product
    return "Product Id not found in the database"

@app.post("/product")
def add_product(product: Product,  db: Session = Depends(get_db)):
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return product

@app.put("/product/{id}")
def update_product(id: int, newProduct:Product, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        db_product.name = newProduct.name
        db_product.description = newProduct.description
        db_product.price = newProduct.price
        db_product.quantity = newProduct.quantity
        db.commit()
        return "Product Updated"
    else:
        return "No products found"

@app.delete("/product/{id}")
def delete_product(id:int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return "Product deleted"
    else:
        return "Product not found"