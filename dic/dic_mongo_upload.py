# By Rakeen Rouf
import csv
from pymongo import MongoClient
import os
import platform
import time


class MongoJsonUpload:
    def __init__(self, csv_file='mongo_data.txt'):
        self.csv_file = csv_file
        self.iter = 0

        self.mongo_client = MongoClient(host=['129.25.20.11:27017'])
        db = self.mongo_client.shm_dic
        self.dic_data = db.test_data

        self.headers = ['Time UTC', 'Surface component 1_epsX_1 [%]', 'Surface component 1_min(epsX) [%]']

    def data_loader(self):
        # Keeps track of active and inactive states
        txt_writer = open("dic_mongo_upload_status.txt", "w")
        txt_writer.write('Status\n')
        txt_writer.write(str(0))

        reader = csv.DictReader(open(self.csv_file, 'r'))
        for line in reader:
            mongo_upload = {}
            for field in self.headers:
                mongo_upload[field] = line[field]

            self.dic_data.insert_one(mongo_upload)

        self.mongo_client.close()

        # Keeps track of active and inactive states
        txt_writer = open("dic_mongo_upload_status.txt", "w")
        txt_writer.write('Status\n')
        txt_writer.write(str(1))

    def modification_date(self):
        if platform.system() == 'Windows':
            return os.path.getmtime(self.csv_file)
        else:
            stat = os.stat(self.csv_file)
            return stat.st_mtime


if __name__ == '__main__':
    # Lets write a txt file containing all running history
    txt_file_writer = open("dic_mongo_upload_status.txt", "w")
    txt_file_writer.write('Status\n')
    txt_file_writer.write(str(1))

    json_loader = MongoJsonUpload()

    mod_time = 0
    while True:
        cur_mod_time = json_loader.modification_date()
        if mod_time < cur_mod_time:
            time.sleep(0.01)
            json_loader.data_loader()
            print('works')
            mod_time = json_loader.modification_date()
