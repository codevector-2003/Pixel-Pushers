from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Use a properly formatted connection string
uri = "mongodb+srv://himathnimpura:himathavenge@cluster0.bjaku.mongodb.net/User_Details?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["smartbaby_db"]  # Ensure database name is correct

# Collections
user_collection = db["User"]  
baby_collection = db["babies"]
milestone_collection = db["milestones"]
diet_collection = db["diet_records"]
vaccine_collection = db["vaccine_records"]
illness_collection = db["illness_records"]
growth_collection = db["growth_records"]
doctor_chat_collection = db["doctor_chats"]
allergy_collection = db["allergies"]
food_collection = db["food"]

# Check if connection is successful
try:
    client.admin.command('ping')
    print("Successfully connected to MongoDB!")
except Exception as e:
    print(f"MongoDB Connection Error: {e}")
