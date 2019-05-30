# By Rakeen Rouf
import RPi.GPIO as GPIO 
import pandas as pd
import os
import platform
import time


class TxtToCsv:
    """
    Converts ae txt files into csv. History.csv keeps track of incoming data. The CSV is updated based on modification
    time
    """

    def __init__(self, data_file=r'livedata2',
                 destination='/mnt/nfsserver/rasp/fog_plot_data.txt', mongo_dest='/mnt/nfsserver/rasp/mongo_data.txt'):

        self.dest = destination
        self.mongo_dest = mongo_dest
        self.data = pd.DataFrame()
        self.data_file = '/mnt/nfsserver/rasp/{}.TXT'.format(data_file)
        self.skip_rows = 0
        self.iter = 0
        self.line = 0  # For getting new data later on
        self.data_cols = None  # Placeholder
        self.append_count = 0
        self.fog_append_count = 0
        GPIO.setmode(GPIO.BCM)             # choose BCM or BOARD  
        GPIO.setup(25, GPIO.IN)


    def parse_columns(self):
        """
        Parses joint columns to a more readable format
        """
        self.data['ID'], self.data['SSSSSSSS.mmmuuun'] = self.data['ID     SSSSSSSS.mmmuuun'].str.split('    ', 1).str
        self.data['PARA1'], self.data['RISE'], self.data['COUN'] = \
            self.data['PARA1  RISE  COUN'].str.split('   ', 2).str
        self.data['RISE'] = self.data['RISE'].str.strip()
        self.data['COUN'] = self.data['COUN'].str.strip()
        self.data['SSSSSSSS.mmmuuun'] = self.data['SSSSSSSS.mmmuuun'].astype(str).str.strip()
    
    def read_txt(self):
        """
        Reads appropriate columns from the ae data text file
        """
        self.data = pd.read_fwf(self.data_file, skiprows=self.skip_rows)
        
        if self.iter != 0:
            self.parse_columns()
        else:
            self.iter = 1
        
        self.data = self.data.loc[self.data['ID'] == '1']
        self.skip_rows += len(self.data)

    def get_file_data(self):
        try:
            self.read_txt()
        except KeyError:
            self.data = pd.read_fwf(self.data_file)

            for i in range(len(self.data)):
                if self.data.iloc[:, 0][i] == 'ID     SSSSSSSS.mmmuuun':
                    self.skip_rows = i + 1
                    break

            self.read_txt()

        self.data = self.data[['ENER', 'DURATION', 'AMP', 'A-FRQ', 'RMS', 'ASL', 'PCNTS', 'THR',
                               'R-FRQ', 'I-FRQ', 'SIG STRNGTH', 'ABS-ENERGY', 'FREQPP1',
                               'FREQPP2', 'FREQPP3', 'FREQPP4', 'FRQ-C', 'P-FRQ', 'ID', 'SSSSSSSS.mmmuuun', 'RISE',
                               'COUN']]

    @staticmethod
    def file_writer_logic(data, location, count):
        status = GPIO.input(25)
        if status == 1:
            data.to_csv(location)
            count = 0
        else:
            if count != 0:
                data.to_csv(location, mode='a', header=False)
            else:
                data.to_csv(location)

            count = 1

        return count

    def loaddata(self):
        self.get_file_data()
        new_data = self.data

        # self.data = self.data.astype('float')

        plot_data = new_data[['SSSSSSSS.mmmuuun', 'DURATION', 'ENER', 'AMP', 'ABS-ENERGY', 'RISE', 'COUN']]

        mongo_data = new_data[['SSSSSSSS.mmmuuun', 'DURATION', 'ENER', 'AMP', 'A-FRQ', 'RMS', 'ASL',
                               'PCNTS', 'THR', 'R-FRQ', 'I-FRQ', 'SIG STRNGTH', 'ABS-ENERGY', 'FREQPP1',
                               'FREQPP2', 'FREQPP3', 'FREQPP4', 'FRQ-C', 'P-FRQ', 'RISE', 'COUN']]

        if self.iter != 0:
            plot_data.to_csv(self.dest, mode='a', header=False)
        else:
            plot_data.to_csv(self.dest)

        self.fog_append_count = self.file_writer_logic(plot_data, self.dest, self.fog_append_count)
        self.append_count = self.file_writer_logic(mongo_data, self.mongo_dest, self.append_count)

    def modification_date(self):

        if platform.system() == 'Windows':
            return os.path.getmtime(self.data_file)
        else:
            stat = os.stat(self.data_file)
            return stat.st_mtime


if __name__ == '__main__':
    txt_to_csv = TxtToCsv()

    mod_time = 0
    while True:
        cur_mod_time = txt_to_csv.modification_date()
        if mod_time < cur_mod_time:
            time.sleep(0.01)
            txt_to_csv.loaddata()
            print('works')
            mod_time = cur_mod_time
