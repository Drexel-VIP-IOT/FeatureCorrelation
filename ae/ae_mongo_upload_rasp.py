# By Rakeen Rouf
import csv
from pymongo import MongoClient
import os
import platform
import time
import RPi.GPIO as GPIO 


class MongoJsonUpload:
    def __init__(self, csv_file='/mnt/nfs/rasp/mongo_data.txt'):
        GPIO.setmode(GPIO.BCM)             # choose BCM or BOARD  
        GPIO.setup(25, GPIO.OUT)           # set GPIO24 as an output  
        
        self.csv_file = csv_file
        self.iter = 0

        self.mongo_client = MongoClient(host=['129.25.20.11:27017'])
        db = self.mongo_client.shm_data
        self.acoustic_data = db.acoustic_data_test_1_30

        self.headers = ['SSSSSSSS.mmmuuun', 'DURATION', 'ENER', 'AMP', 'A-FRQ', 'RMS', 'ASL',
                        'PCNTS', 'THR', 'R-FRQ', 'I-FRQ', 'SIG STRNGTH', 'ABS-ENERGY', 'FREQPP1',
                        'FREQPP2', 'FREQPP3', 'FREQPP4', 'FRQ-C', 'P-FRQ', 'RISE', 'COUN']

    def data_loader(self):
        # Keeps track of active and inactive states
        GPIO.output(25, 0)

        reader = csv.DictReader(open(self.csv_file, 'r'))
        for line in reader:
            mongo_upload = {}
            try:
                for field in self.headers:
                    if field == 'SSSSSSSS.mmmuuun':
                        mongo_upload['time'] = float(line[field])
                    else:
                        mongo_upload[field] = float(line[field])

                self.acoustic_data.insert(mongo_upload)
            except Exception as e:
                print(repr(e))
        self.mongo_client.close()

        # Keeps track of active and inactive states
        GPIO.output(25, 1)

    def modification_date(self):
        if platform.system() == 'Windows':
            return os.path.getmtime(self.csv_file)
        else:
            stat = os.stat(self.csv_file)
            return stat.st_mtime


if __name__ == '__main__':
    # Lets write a txt file containing all running history
    txt_file_writer = open("ae_mongo_upload_status.txt", "w")
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
            mod_time = cur_mod_time
