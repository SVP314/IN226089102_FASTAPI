from fastapi import FastAPI, Query

app = FastAPI()

products = [
    {"id":1,"name":"Wireless Mouse","price":499,"category":"Electronics"},
    {"id":3,"name":"Notebook","price":99,"category":"Stationery"},
    {"id":2,"name":"USB Hub","price":799,"category":"Electronics"},
    {"id":4,"name":"Pen Set","price":49,"category":"Stationery"},
]
orders = []


# Q1 SEARCH PRODUCTS
@app.get("/products/search")
def search_products(keyword:str):

    result=[p for p in products if keyword.lower() in p["name"].lower()]

    if not result:
        return {"message":f"No products found for: {keyword}"}

    return {
        "keyword":keyword,
        "total_found":len(result),
        "products":result
    }


# Q2 SORT PRODUCTS
@app.get("/products/sort")
def sort_products(sort_by:str="price",order:str="asc"):

    if sort_by not in ["price","name"]:
        return {"error":"sort_by must be 'price' or 'name'"}

    result=sorted(products,key=lambda p:p[sort_by],reverse=(order=="desc"))

    return{
        "sort_by":sort_by,
        "order":order,
        "products":result
    }


# Q3 PAGINATION
@app.get("/products/page")
def paginate_products(page:int=Query(1,ge=1),limit:int=Query(2,ge=1)):

    start=(page-1)*limit
    total=len(products)

    return{
        "page":page,
        "limit":limit,
        "total":total,
        "total_pages":-(-total//limit),
        "products":products[start:start+limit]
    }


# CREATE ORDER
@app.post("/orders")
def create_order(customer_name:str):

    order={
        "order_id":len(orders)+1,
        "customer_name":customer_name
    }

    orders.append(order)

    return order


# Q4 SEARCH ORDERS
@app.get("/orders/search")
def search_orders(customer_name:str):

    result=[o for o in orders if customer_name.lower() in o["customer_name"].lower()]

    if not result:
        return {"message":f"No orders found for: {customer_name}"}

    return{
        "customer_name":customer_name,
        "total_found":len(result),
        "orders":result
    }


# Q5 SORT BY CATEGORY THEN PRICE
@app.get("/products/sort-by-category")
def sort_by_category():

    result=sorted(products,key=lambda p:(p["category"],p["price"]))

    return{
        "total":len(result),
        "products":result
    }


# Q6 BROWSE PRODUCTS
@app.get("/products/browse")
def browse_products(
        keyword:str=None,
        sort_by:str="price",
        order:str="asc",
        page:int=1,
        limit:int=4
):

    result=products

    if keyword:
        result=[p for p in result if keyword.lower() in p["name"].lower()]

    if sort_by in ["price","name"]:
        result=sorted(result,key=lambda p:p[sort_by],reverse=(order=="desc"))

    total=len(result)

    start=(page-1)*limit

    paged=result[start:start+limit]

    return{
        "keyword":keyword,
        "sort_by":sort_by,
        "order":order,
        "page":page,
        "limit":limit,
        "total_found":total,
        "total_pages":-(-total//limit),
        "products":paged
    }


# BONUS PAGINATE ORDERS
@app.get("/orders/page")
def paginate_orders(page:int=1,limit:int=3):

    start=(page-1)*limit

    return{
        "page":page,
        "limit":limit,
        "total":len(orders),
        "total_pages":-(-len(orders)//limit),
        "orders":orders[start:start+limit]
    }