# By Rakeen Rouf
import pandas as pd
import matplotlib.pyplot as plt
import math
import matplotlib.animation as animation
from pymongo import MongoClient
from io import StringIO


class CloudDataPlotter:
    def __init__(self):
        self.data = pd.DataFrame()
        self.fig_iter_num = 0
        self.client = MongoClient(host=['129.25.20.11:27017'])
        self.db = self.client.pythonbicookbook  # This is our collection
        self.files = self.db.files

    def loaddata(self):
        """
        Loads new data from our MongoDb serve and saves it as a csv

        :return: updated data
        :rtype: pandas data frame
        """
        # Update the name of the text file here
        text_file_doc = self.files.find_one({"file_name": "plot_final.txt"})
        test_file_doc = text_file_doc['contents']
        self.data = pd.concat([pd.read_csv(StringIO(d), sep=",") for d in [test_file_doc]])
        self.client.close()

        self.data = self.data.astype('float')
        self.data.to_csv('cloud_plot_data.txt')


if __name__ == '__main__':
    data_plotter = CloudDataPlotter()
    while True:
        data_plotter.loaddata()
