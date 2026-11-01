from fastapi import FastAPI

from models import Product

app = FastAPI()
# run with  uvicorn main:app --reload 
@app.get("/")
def greet():
    return "Hello";

products = [
    Product(id=1,name="iPhone",description="Expensive Phone with features you won't use anyway", price=999.99, quantity=20),
    Product(id=2,name="macBook",description="Expensive Laptop that can't run most apps and games", price=1999.99, quantity=10),
    Product(id=4,name="iPad",description="Expensive tablet that can actually be good for artists", price=899.99, quantity=30),
]

@app.get("/product")
def get_all_products():
    return products

@app.get("/product/{id}")
def get_product_by_id(id:int):
    for product in products:
        if product.id == id:
            return product
    return "Product Id not found in the database"

@app.post("/product")
def add_product(product: Product):
    products.append(product)
    return product

@app.put("/product")
def update_product(id: int, newProduct:Product):
   for i in range(len(products)):
        if products[i].id == id:
            products[i] = newProduct
            return "Product updated"
    return "No products fpind"