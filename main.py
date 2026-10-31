from fastapi import FastAPI

from models import Product

app = FastAPI()

@app.get("/")
def greet():
    return "Hello"

products = [
    Product(id=1,name="iPhone",description="Expensive Phone with features you won't use anyway", price=999.99, quantity=20),
    Product(id=2,name="macBook",description="Expensive Laptop that can't run most apps and games", price=1999.99, quantity=10),
]

@app.get("/products")
def get_all_products():
    return products