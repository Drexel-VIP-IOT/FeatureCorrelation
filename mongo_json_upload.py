# By Rakeen Rouf
import csv
from pymongo import MongoClient
import os
import platform
import time


class MongoJsonUpload:
    def __init__(self, csv_file='/mnt/nfsserver/rasp/mongo_data.txt'):
        self.csv_file = csv_file
        self.iter = 0

        self.mongo_client = MongoClient(host=['129.25.20.11:27017'])
        db = self.mongo_client.shm_data
        self.acoustic_data = db.acoustic_data

        self.headers = ['SSSSSSSS.mmmuuun', 'cum_sum_ENER', 'DURATION',
                        'ENER', 'DURATION', 'AMP', 'A-FRQ', 'RMS', 'ASL', 'PCNTS', 'THR',
                        'R-FRQ', 'I-FRQ', 'SIG STRNGTH', 'ABS-ENERGY', 'FREQPP1',
                        'FREQPP2', 'FREQPP3', 'FREQPP4', 'FRQ-C', 'P-FRQ']
        
    def data_loader(self):
        reader = csv.DictReader(open(self.csv_file, 'r'))
        for line in reader:
            mongo_upload = {}            
            for field in self.headers:
                
                if field == 'SSSSSSSS.mmmuuun':
                    mongo_upload['time'] = line[field]
                else:
                    mongo_upload[field] = line[field]
                    
            self.acoustic_data.insert(mongo_upload)
    
        self.mongo_client.close()

    def modification_date(self):
        if platform.system() == 'Windows':
            return os.path.getmtime(self.csv_file)
        else:
            stat = os.stat(self.csv_file)
            return stat.st_mtime
        

if __name__ == '__main__':
    json_loader = MongoJsonUpload()

    mod_time = 0
    while True:
        cur_mod_time = json_loader.modification_date()
        if mod_time < cur_mod_time:
            time.sleep(0.01)
            json_loader.data_loader()
            print('works')
            mod_time = json_loader.modification_date()
