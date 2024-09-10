from bson import ObjectId
from pymongo import MongoClient
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder

# MongoDB connection
client = MongoClient("mongodb://root:password@localhost:27017/")
mydb = client["products_db"]
mycol = mydb["products"]





app = FastAPI(
    title="Product FastAPI",  # Set the name of your API
    version="1.2.0",      # Set the version of your API
)

@app.get("/")
async def read_root():
    return {
        "message": "Welcome to Product API"
        
        }

def convert_objectid_to_str(product):
    """Converts ObjectId to string for MongoDB documents."""
    if '_id' in product:
        product['_id'] = str(product['_id'])
    return product

@app.get("/api/products", tags=["Products"])
async def all_products():
    products = list(mycol.find())  # Get all products and convert to list
    serialized_products = [convert_objectid_to_str(product) for product in products]  # Convert ObjectId to string
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Products data retrieved successfully",
        "data": jsonable_encoder(serialized_products)  # Serialize the data safely
    }
 
 
@app.post("/api/products", tags=["Products"])
async def create_product(product: dict):
     result = mycol.insert_one(product)
     return {
         "status_code": 201,
         "response_type": "success",
         "description": "Product created successfully",
         "data": jsonable_encoder({"_id": str(result.inserted_id)})  # Convert ObjectId to string
         }
 
@app.get("/api/products/{product_id}", tags=["Products"])
async def single_product(product_id):
    product = mycol.find_one({"_id": ObjectId(product_id)})  # Convert product_id
    if product:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": "Product data retrieved successfully",
            "data": jsonable_encoder(convert_objectid_to_str(product))  # Convert ObjectId to string
            }
    else:
        return {
            "status_code": 404,
            "response_type": "error",
            "description": "Product not found"
            }


@app.put("/api/products/{product_id}", tags=["Products"])
async def update_product(product_id: str, product_data: dict):
    # Check if the product exists
    existing_product = mycol.find_one({"_id": ObjectId(product_id)})
    if not existing_product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Update the product with the provided data
    mycol.update_one({"_id": ObjectId(product_id)}, {"$set": product_data})
    
    # Fetch the updated product
    updated_product = mycol.find_one({"_id": ObjectId(product_id)})
    
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Product updated successfully",
        "data": jsonable_encoder(convert_objectid_to_str(updated_product))  # Serialize the updated product
    }
 
                 
@app.delete("/api/products/{product_id}", tags=["Products"])
async def delete_product(product_id):
    mycol.delete_one({"_id": ObjectId(product_id)})
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Product deleted successfully"
        }
 
 
 
# def insert():
    # mydoc = {
    #   "name": "Product 2",
    #   "price": 10.12,
    #   "category": "Shoe"
    #   }
    # mycol.insert_one(mydoc)
 

    
# def main():
#    insert();

# if __name__ == "__main__":
#     main()  # call the main function
