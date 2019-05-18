#  By Rakeen Rouf
import pandas as pd
from copy import deepcopy
from platform import system
import os
import time


class DicPrePros:
    def __init__(self, input_file_loc, mongo_dest='mongo_data.txt'):
        self.input_file = input_file_loc
        self.skip_rows = 0
        self.raw_columns = None  # Place holder
        self.mongo_dest = mongo_dest
        self.processed_cols = None
        self.append_count = 0

    def parse_data(self):
        processed_df = pd.DataFrame()

        if self.skip_rows == 0:
            raw_df = pd.read_csv(self.input_file, skiprows=1)
            self.raw_columns = raw_df.columns
            # Extracts the column names
            processed_cols = self.raw_columns[0].replace('"', '')
            processed_cols = processed_cols.replace('.', '_')
            self.processed_cols = processed_cols.split(';')

        else:
            raw_df = pd.read_csv(self.input_file, skiprows=self.skip_rows)
            raw_df.columns = self.raw_columns

        try:
            raw_df[self.raw_columns] = raw_df[self.raw_columns].replace({'"': ''}, regex=True)
        except KeyError:
            pass

        index, processed_df[self.processed_cols[1]] = raw_df[self.raw_columns[0]].str.split(' ', 1).str
        del index  # We don't have any use for index

        processed_cols = self.processed_cols[2:]  # Lets move on
        processed_cols_data = deepcopy(processed_cols)
        processed_cols_data = raw_df[self.raw_columns[1]].str.split(';', len(processed_cols_data)).str
        count = 0
        for j in range(len(processed_cols) + 1):
            if count > 0:
                processed_df[processed_cols[j-1]] = processed_cols_data[j]
            else:
                count = 1

        self.skip_rows += len(processed_df)

    def output_data(self, data):
        status = pd.read_fwf('dic_mongo_upload_status.txt')['Status'][0]

        if status == 1:
            data.to_csv(self.mongo_dest)
            self.append_count = 0
        else:
            if self.append_count != 0:
                data.to_csv(self.mongo_dest, mode='a', header=False)
            else:
                data.to_csv(self.mongo_dest)

            self.append_count = 1

    def modification_date(self):
        if system() == 'Windows':
            return os.path.getmtime(self.input_file)
        else:
            stat = os.stat(self.input_file)
            return stat.st_mtime


if __name__ == '__main__':
    inp = r'C:\Users\rakee\Downloads\Tracking.csv'
    dic = DicPrePros(inp)

    mod_time = 0
    while True:
        cur_mod_time = dic.modification_date()
        if mod_time < cur_mod_time:
            time.sleep(0.01)
            dic.parse_data()
            print('works')
            mod_time = dic.modification_date()
