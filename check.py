from pymongo import MongoClient
import certifi

# Connect to MongoDB
client = MongoClient("mongodb+srv://mazeez:Temilola%401209@cluster0.bsxpc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0", tlsCAFile=certifi.where())
db = client['customer_data']  # Replace with your actual database name
customers_collection = db['Customers']  # Replace with your actual collection name

# Check for customer_id 1
customer = customers_collection.find_one({"customer_id": 1})
print(customer)
