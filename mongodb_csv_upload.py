# By Rakeen Rouf
from pymongo import MongoClient
import os
import platform
import time


class MongoDbCsvUpload:
    def __init__(self):
        # To connect to our mongodb server
        self.client = MongoClient(host=['129.25.20.11:27017'])
        self.db = self.client.pythonbicookbook  # This is our collection
        self.files = self.db.files
        self.data_file = 'C:/Users/rakee/Downloads/fog_plot_data.txt'

    def data_loader(self):
        self.files.delete_one({"file_name": "plot_final.txt"})
        data = open('C:/Users/rakee/Downloads/fog_plot_data.txt', 'r').read()
        doc = {"file_name": "plot_final.txt", "contents": data}
        self.files.insert(doc)
        self.client.close()

    def modification_date(self):
        if platform.system() == 'Windows':
            return os.path.getmtime(self.data_file)
        else:
            stat = os.stat(self.data_file)
            return stat.st_mtime


if __name__ == '__main__':
    mongo_csv_loader = MongoDbCsvUpload()
    mod_time = 0
    while True:
        cur_mod_time = mongo_csv_loader.modification_date()
        if mod_time < cur_mod_time:
            time.sleep(0.01)
            mongo_csv_loader.data_loader()
            print('works')
            mod_time = mongo_csv_loader.modification_date()
