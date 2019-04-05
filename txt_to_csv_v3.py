# By Rakeen Rouf
import pandas as pd
import os
import platform
import time
import numpy as np

class TxtToCsv:
    """
    Converts ae txt files into csv. History.csv keeps track of incoming data. The CSV is updated based on modification
    time
    """

    def __init__(self, data_file='/mnt/nfsserver/rasp/livedata2.TXT',
                 destination='/mnt/nfsserver/rasp/fog_plot_data.txt'):
        
        self.dest = destination
        self.data = pd.DataFrame()
        self.data_file = data_file
        self.skip_rows = 0
        self.iter = 0
        
    def get_file_data(self):
        try:
            self.data = pd.read_fwf(self.data_file, skiprows=self.skip_rows)
            
            self.data = self.data.loc[self.data['ID'] == '1']
        except KeyError:
            self.data = pd.read_fwf(self.data_file)
            for i in range(len(self.data)):
                if self.data.iloc[:, 0][i] == 'ID     SSSSSSSS.mmmuuun':
                    self.skip_rows = i + 1
                    break
            self.data = pd.read_fwf(self.data_file, skiprows=self.skip_rows)
       
            
        # Lets just keep the data points which have id == 1
        self.data['ID'], self.data['SSSSSSSS.mmmuuun'] = self.data['ID     SSSSSSSS.mmmuuun'].str.split('    ', 1).str
        self.data = self.data.loc[self.data['ID'] == '1']
        self.data = self.data[['ENER', 'DURATION', 'AMP', 'A-FRQ', 'RMS', 'ASL', 'PCNTS', 'THR',
                               'R-FRQ', 'I-FRQ', 'SIG STRNGTH', 'ABS-ENERGY', 'FREQPP1',
                               'FREQPP2', 'FREQPP3', 'FREQPP4', 'FRQ-C', 'P-FRQ', 'ID', 'SSSSSSSS.mmmuuun']]

    def loaddata(self):
        # Lets read in how many lines we had in the last iter
        line_number = int(pd.read_fwf('History.txt')['History'][0])
        # cum sum from last iter
        cum_sum_ener = int(pd.read_fwf('History.txt')['History'][1])
        
        
        # Which line do I start at?
        start_line = int(pd.read_fwf('History.txt')['History'][2])

        self.get_file_data()
        
        if self.iter == 0:
            temp_data = pd.DataFrame(columns=self.data.columns)
            self_iter = 1
        else:
            temp_data = pd.read_fwf(self.dest)
            temp_data.columns = self.data.columns
            
        self.data = pd.concat([temp_data, self.data.iloc[line_number:]], join="inner")
        #self.data = self.data.astype('float')
        self.data['cum_sum_ENER'] = self.data['ENER'].cumsum() + cum_sum_ener

        txt_file = open("History.txt", "w")  # Lets update our history file for the next iter
        txt_file.write('History\n')
        txt_file.write(str(len(self.data)))
        txt_file.write('\n')
        print(self.data['cum_sum_ENER'].iloc[-1])
        b=self.data['cum_sum_ENER'].iloc[-1]
        if np.isnan(self.data['cum_sum_ENER'].iloc[-1]):
            b=0
        txt_file.write(str(int(b)))
        txt_file.write('\n')
        txt_file.write(str(start_line - 1))
        txt_file.close()

        plot_data = self.data[['SSSSSSSS.mmmuuun', 'cum_sum_ENER', 'DURATION',
                               'ENER', 'DURATION', 'AMP', 'A-FRQ', 'RMS', 'ASL', 'PCNTS', 'THR',
                               'R-FRQ', 'I-FRQ', 'SIG STRNGTH', 'ABS-ENERGY', 'FREQPP1',
                               'FREQPP2', 'FREQPP3', 'FREQPP4', 'FRQ-C', 'P-FRQ']]
        
        plot_data.to_csv(self.dest)

    def modification_date(self):

        if platform.system() == 'Windows':
            return os.path.getmtime(self.data_file)
        else:
            stat = os.stat(self.data_file)
            return stat.st_mtime

if __name__ == '__main__':
    # Lets write a txt file containing all running history
    txt_file_writer = open("History.txt", "w")
    txt_file_writer.write('History\n')
    txt_file_writer.write(str(0))
    txt_file_writer.write('\n')
    txt_file_writer.write(str(0))
    txt_file_writer.write('\n')
    txt_file_writer.write(str(30))
    txt_file_writer.close()
    txt_to_csv = TxtToCsv()

    mod_time = 0
    while True:
        cur_mod_time = txt_to_csv.modification_date()
        if mod_time < cur_mod_time:
            time.sleep(0.01)
            txt_to_csv.loaddata()
            print('works')
            mod_time = txt_to_csv.modification_date()

