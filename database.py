from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from datetime import datetime

# Detalhes da conexão com o MongoDB Atlas
MONGO_DETAILS = "mongodb+srv://root:fabioramos%40@cluster0.jtr8vjf.mongodb.net/?retryWrites=true&w=majority"

client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.uploads

file_collection = database.get_collection("files")

def file_helper(file) -> dict:
    return {
        "id": str(file["_id"]),
        "filename": file["filename"],
        "upload_time": file["upload_time"],
    }

async def add_file(file_data: dict) -> dict:
    file = await file_collection.insert_one(file_data)
    new_file = await file_collection.find_one({"_id": file.inserted_id})
    return file_helper(new_file)

async def retrieve_file(id: str) -> dict:
    file = await file_collection.find_one({"_id": ObjectId(id)})
    if file:
        return file_helper(file)
