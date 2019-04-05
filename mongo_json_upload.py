import csv
import json
from pymongo import MongoClient


class MongoJsonUpload:
    def __init__(self, csvfile = open('/mnt/nfsserver/rasp/fog_plot_data.txt', 'r')):
        self.reader = csv.DictReader(csvfile)
        self.mongo_client = MongoClient(host=['129.25.20.11:27017'])
        db = self.mongo_client.shm_data
        self.acoustic_data = db.acoustic_data
        self.headers = ['SSSSSSSS.mmmuuun', 'cum_sum_ENER', 'DURATION', 'AMP']
        
    def data_loader(self):
        for line in self.reader:
            mongo_upload = {}            
            for field in self.headers:
                
                if field == 'SSSSSSSS.mmmuuun':
                    mongo_upload['time'] = line[field]
                else:
                    mongo_upload[field] = line[field]
                    
            self.acoustic_data.insert(mongo_upload)
    
        self.mongo_client.close()
        
if __name__ == '__main__':
    json_loader = MongoJsonUpload()
    json_loader.data_loader()
        
        
        
    


