from pymongo import MongoClient
import urllib
client = MongoClient("mongodb+srv://mma343:" + urllib.quote("Elish2ta:)") + "@cluster0-obfic.mongodb.net/test?retryWrites=true")
db = client["test_database"]  # use a database called "test_database"
collection = db["test_collection"]  # and inside that DB, a collection called "files"

f = open('livedata.txt')  # open a file
text = f.read()    # read the entire contents, should be UTF-8 text

# build a document to be inserted
text_file_doc = {"file_name": "livedata.txt", "contents" : text }
# insert the contents into the "file" collection
collection.insert(text_file_doc)
posts = db.posts
post_id = posts.insert_one(text_file_doc).inserted_id