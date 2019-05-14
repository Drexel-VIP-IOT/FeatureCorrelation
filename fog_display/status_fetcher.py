# By Rakeen Rouf
from pymongo import MongoClient


# To connect to our mongodb server
client = MongoClient(host=['129.25.20.11:27017'])
db = client.shm_data  # This is our collection
collection = db.statusid

# To read the status from Mongo
status = collection.find_one({})['status']
client.close()
