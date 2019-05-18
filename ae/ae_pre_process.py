# By Rakeen Rouf
import pandas as pd
import os
import platform
import time


class TxtToCsv:
    """
    Converts ae txt files into csv. History.csv keeps track of incoming data. The CSV is updated based on modification
    time
    """

    def __init__(self, data_file=r'livedata0.TXT',
                 destination='fog_plot_data.txt', mongo_dest='mongo_data.txt'):

        self.dest = destination
        self.mongo_dest = mongo_dest
        self.data = pd.DataFrame()
        self.data_file = data_file
        self.skip_rows = 0
        self.iter = 0
        self.line = 0  # For getting new data later on
        self.data_cols = None  # Placeholder

    def read_txt(self):
        self.data = pd.read_fwf(self.data_file, skiprows=self.skip_rows)
        self.data = self.data.loc[self.data['ID'] == 1]

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
            self.data_cols = self.data.columns
            print(self.data_cols)
            # Extracts the column names
            #processed_cols = self.raw_columns[0].replace('"', '')
            #processed_cols = processed_cols.replace('.', '_')
            #self.processed_cols = processed_cols.split(';')


        # Lets just keep the data points which have id == 1

        # self.data['ID'], self.data['SSSSSSSS.mmmuuun'] = self.data['ID     SSSSSSSS.mmmuuun'].str.split('    ', 1).str
        # self.data['PARA1'], self.data['RISE'], self.data['COUN'] = self.data['PARA1  RISE  COUN'].str.split('   ', 2).str



        # self.data['RISE'] = self.data['RISE'].str.strip()
        # self.data['COUN'] = self.data['COUN'].str.strip()
        self.data['SSSSSSSS.mmmuuun'] = self.data['SSSSSSSS.mmmuuun'].astype(str).str.strip()

        self.data = self.data[['ENER', 'DURATION', 'AMP', 'A-FRQ', 'RMS', 'ASL', 'PCNTS', 'THR',
                               'R-FRQ', 'I-FRQ', 'SIG STRNGTH', 'ABS-ENERGY', 'FREQPP1',
                               'FREQPP2', 'FREQPP3', 'FREQPP4', 'FRQ-C', 'P-FRQ', 'ID', 'SSSSSSSS.mmmuuun']]

    def loaddata(self):
        self.get_file_data()

        if self.iter == 0:
            temp_data = pd.DataFrame(columns=self.data.columns)
            new_data = self.data
            self.line += len(self.data) - 1
            self.iter = 1
        else:
            temp_data = pd.read_csv(self.dest)
            print(self.line)
            new_data = self.data.iloc[self.line:]
            self.line += len(new_data) - 1

        self.data = pd.concat([temp_data, new_data], join="inner")
        # self.data = self.data.astype('float')

        plot_data = self.data[['SSSSSSSS.mmmuuun', 'DURATION', 'ENER', 'AMP']]

        mongo_data = new_data[['SSSSSSSS.mmmuuun', 'DURATION', 'ENER', 'AMP', 'A-FRQ', 'RMS', 'ASL',
                               'PCNTS', 'THR', 'R-FRQ', 'I-FRQ', 'SIG STRNGTH', 'ABS-ENERGY', 'FREQPP1',
                               'FREQPP2', 'FREQPP3', 'FREQPP4']]

        plot_data.to_csv(self.dest)
        mongo_data.to_csv(self.mongo_dest)

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
