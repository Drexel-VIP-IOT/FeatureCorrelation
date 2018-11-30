from pymongo import MongoClient
import pandas as pd
from io import StringIO


# Rakeen Rouf
# To connect to our mongodb server
client = MongoClient(host=['129.25.20.11:27017'])
db = client.pythonbicookbook  # This is our collection
files = db.files

# To create the .txt file
# we are skipping the first seven rows of the .txt file since it contains no useful data. And the
data = pd.read_fwf(r'C:\Users\rakee\Downloads\livedata.txt', skiprows=7)  # Update the name of the text file here
data = data.loc[data['ID'] == '1']  # Lets only keep the rows where the id = 1
data = data.to_csv()
doc = {"file_name": "livedata_rakeen.txt", "contents": data}
files.insert(doc)

# To read the uploaded data as a pandas data frame
text_file_doc = files.find_one({"file_name": "livedata_rakeen_rouf.txt"})
test_file_doc = text_file_doc['contents']
output_data = pd.concat([pd.read_csv(StringIO(d), sep=",") for d in [test_file_doc]])

# The output data is a pandas data frame
print(output_data)
print(type(output_data))

client.close()
