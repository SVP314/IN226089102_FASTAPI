from fastapi import FastAPI, HTTPException

app = FastAPI()

#product database
products = [
    {"id": 1, "name": "Keyboard", "price": 499, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Mouse Pad", "price": 99, "category": "Accessories", "in_stock": True},
    {"id": 3, "name": "USB Hub", "price": 799, "category": "Electronics", "in_stock": False},
]

# Q1 – Add Product

@app.post("/products")
def add_product(product: dict):

    # Check duplicate name
    for p in products:
        if p["name"].lower() == product["name"].lower():
            raise HTTPException(status_code=400, detail="Product with this name already exists")

    new_id = max(p["id"] for p in products) + 1 if products else 1

    product_data = {
        "id": new_id,
        "name": product["name"],
        "price": product["price"],
        "category": product["category"],
        "in_stock": product["in_stock"]
    }

    products.append(product_data)

    return {
        "message": "Product added",
        "product": product_data
    }

# Get All Products

@app.get("/products")
def get_products():
    return {
        "products": products,
        "total": len(products)
    }


# Q5 – Audit Endpoint

@app.get("/products/audit")
def product_audit():

    total_products = len(products)

    in_stock_count = sum(1 for p in products if p["in_stock"])

    out_of_stock_names = [p["name"] for p in products if not p["in_stock"]]

    total_stock_value = sum(p["price"] for p in products if p["in_stock"])

    most_expensive = max(products, key=lambda p: p["price"])

    return {
        "total_products": total_products,
        "in_stock_count": in_stock_count,
        "out_of_stock_names": out_of_stock_names,
        "total_stock_value": total_stock_value,
        "most_expensive": {
            "name": most_expensive["name"],
            "price": most_expensive["price"]
        }
    }

# BONUS – Discount Endpoint
@app.put("/products/discount")
def apply_discount(category: str, discount_percent: int):

    updated_products = []

    for p in products:
        if p["category"].lower() == category.lower():
            p["price"] = int(p["price"] * (1 - discount_percent / 100))
            updated_products.append(p)

    return {
        "message": f"{discount_percent}% discount applied to {category}",
        "updated_count": len(updated_products),
        "updated_products": updated_products
    }


# Get Product by ID

@app.get("/products/{product_id}")
def get_product(product_id: int):

    for p in products:
        if p["id"] == product_id:
            return p

    raise HTTPException(status_code=404, detail="Product not found")


# Q2 – Update Product

@app.put("/products/{product_id}")
def update_product(product_id: int, price: int = None, in_stock: bool = None):

    for p in products:

        if p["id"] == product_id:

            if price is not None:
                p["price"] = price

            if in_stock is not None:
                p["in_stock"] = in_stock

            return {
                "message": "Product updated",
                "product": p
            }

    raise HTTPException(status_code=404, detail="Product not found")

# Q3 – Delete Product

@app.delete("/products/{product_id}")
def delete_product(product_id: int):

    for p in products:

        if p["id"] == product_id:

            products.remove(p)

            return {
                "message": f"Product '{p['name']}' deleted"
            }

    raise HTTPException(status_code=404, detail="Product not found")