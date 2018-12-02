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

    def __init__(self, data_file='C:/Users/rakee/Downloads/livedata.txt'):
        self.data = pd.DataFrame()
        self.data_file = data_file

    def loaddata(self):
        try:
            self.data = pd.read_fwf(self.data_file, skiprows=7)
            # Lets just keep the data points which have id == 1
            self.data = self.data.loc[self.data['ID'] == '1']
        except KeyError:
            self.data = pd.read_fwf(self.data_file, skiprows=8)
            # Lets just keep the data points which have id == 1
            self.data = self.data.loc[self.data['ID'] == '1']

        # Lets read in how many lines we had in the last iter
        line_number = int(pd.read_fwf('History.txt')['History'][0])
        # cum sum from last iter
        cum_sum_ener = int(pd.read_fwf('History.txt')['History'][1])
        temp_data = pd.DataFrame(columns=self.data.columns)
        self.data = pd.concat([temp_data, self.data.iloc[line_number:]], join="inner")
        self.data = self.data.astype('float')

        self.data['cum_sum_ENER'] = self.data['ENER'].cumsum() + cum_sum_ener

        txt_file = open("History.txt", "w")  # Lets update our history file for the next iter
        txt_file.write('History\n')
        txt_file.write(str(len(self.data)))
        txt_file.write('\n')
        txt_file.write(str(int(self.data['cum_sum_ENER'].iloc[-1])))
        txt_file.close()

        plot_data = self.data[['SSSSSSSS.mmmuuun', 'cum_sum_ENER', 'DURATION', 'AMP']]
        print(plot_data)
        plot_data.to_csv('C:/Users/rakee/Downloads/fog_plot_data.txt')

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
