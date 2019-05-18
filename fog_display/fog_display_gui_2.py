#!/usr/bin/python3
# By Rakeen Rouf
import sys
from PyQt5 import QtWidgets, QtGui, uic
import matplotlib.pylab as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib
import matplotlib.animation as animation
import pandas as pd
from pymongo import MongoClient
from platform import system
import os
from time import sleep
import numpy as np
from scipy.spatial import distance


matplotlib.use('QT5Agg')


class FogDataPlotter:
    def __init__(self, mongo_data='fog_plot_data.txt'):
        self.fig_iter_num = 0
        self.plt_1 = 0  # Place holder
        self.mongo_data = mongo_data
        self.old_mod_time = 0
        self.cum_energy = 0
        self.min_dur = 0
        self.max_dur = 100
        self.min_time = 0
        self.max_time = 30
        self.min_rise = 0
        self.max_rise = 100
        self.min_cum_ener = 0
        self.max_cum_ener = 20
        self.min_cmsd = 0
        self.max_cmsd = 20
        self.v = 0
        self.iv = 0
        self.msd_cum_sum = 0

    def modification_time(self):
        if system() == 'Windows':
            return os.path.getmtime(self.mongo_data)
        else:
            stat = os.stat(self.mongo_data)
            return stat.st_mtime

    def update_data(self, curr, ax1, ax2, ax3, ax4, win):
        cur_mod_time = self.modification_time()
        if cur_mod_time > self.old_mod_time:
            dataa = pd.read_csv(self.mongo_data)
            self.update_plot(curr, ax1, ax2, ax3, ax4, win, dataa)
            self.old_mod_time = cur_mod_time
        else:
            pass

    @staticmethod
    def find_limits(val_1, val_2, old_val_1_min, old_val_2_min, old_val_1_max, old_val_2_max):
        """
        General function to find x,y limits of a plot
        """
        min_val_1 = min(val_1)
        max_val_1 = max(val_1)
        min_val_2 = min(val_2)
        max_val_2 = max(val_2)

        if min_val_1 > old_val_1_min:
            min_val_1 = old_val_1_min

        if min_val_2 > old_val_2_min:
            min_val_2 = old_val_2_min

        if max_val_1 < old_val_1_max:
            max_val_1 = old_val_1_max

        if max_val_2 < old_val_2_max:
            max_val_2 = old_val_2_max

        return min_val_1, min_val_2, max_val_1, max_val_2

    def calc_msd(self, dataa):
        """
        Calculates Cumulative Mahalanobis Distance
        :return: Cumulative MHD
        """
        data_shape = dataa.shape
        msd = np.empty(data_shape[0])

        if self.fig_iter_num == 0:
            msd_data = dataa.drop(['SSSSSSSS.mmmuuun'], axis=1).values
            self.v = np.mean(msd_data[0:14, :], axis=0)
            cov = np.cov(msd_data, rowvar=False)
            cov[np.isnan(cov)] = 0
            self.iv = np.linalg.pinv(cov)
        else:
            msd_data = dataa.drop(['SSSSSSSS.mmmuuun'], axis=1).values

        for x in range(1, data_shape[0]):
            msd[x] = distance.mahalanobis(msd_data[x, :], self.v, self.iv)

        cmsd = msd + self.msd_cum_sum
        self.msd_cum_sum = cmsd[-1]

        return cmsd

    def update_plot(self, curr, ax1, ax2, ax3, ax4, win, dataa):
        time_data = dataa['SSSSSSSS.mmmuuun']

        self.fig_iter_num = curr  # updates figure number
        cmsd = self.calc_msd(dataa)
        ax2.plot(time_data, cmsd, 'b', linewidth=2)
        ax2.set_ylabel('Cumulative Mahalanobis Distance', weight='bold', fontsize=12)
        ax2.set_xlabel('Time(μs)', weight='bold', fontsize=12)
        self.min_time, self.min_cmsd, self.max_time, self.max_cmsd = \
            self.find_limits(time_data, cmsd, self.min_time, self.min_cmsd, self.max_time, self.max_cmsd)
        ax2.set_xlim(self.min_time - 10, self.max_time + 10)
        ax2.set_ylim(self.min_cmsd - 50, self.max_cmsd + 50)

        duration = dataa['DURATION']
        rise = dataa['RISE']
        ax1.scatter(duration, rise, color='b', edgecolor='k')
        ax1.set_ylabel('Rise(μs)', weight='bold', fontsize=12)
        ax1.set_xlabel('Duration(μs)', weight='bold', fontsize=12)
        self.min_dur, self.min_rise, self.max_dur, self.max_rise = \
            self.find_limits(duration, rise, self.min_dur, self.min_rise, self.max_dur, self.max_rise)
        ax1.set_xlim(self.min_dur - 100, self.max_dur + 100)
        ax1.set_ylim(self.min_rise - 100, self.max_rise + 100)

        energy = dataa['ENER']
        energy += self.cum_energy
        self.cum_energy = energy.iloc[-1]
        ax4.plot(time_data, energy, 'b', linewidth=2)
        ax4.set_ylabel('Cumilative Energy(aJ)', weight='bold', fontsize=12)
        ax4.set_xlabel('Time(s)', weight='bold', fontsize=12)
        self.min_time, self.min_cum_ener, self.max_time, self.max_cum_ener = \
            self.find_limits(time_data, energy, self.min_time, self.min_cum_ener, self.max_time, self.max_cum_ener)
        ax4.set_xlim(self.min_time - 10, self.max_time + 10)
        ax4.set_ylim(self.min_cum_ener - 50, self.max_cum_ener + 50)

        win.status_bar()


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self, figure):
        super(MyWindow, self).__init__()
        uic.loadUi('test.ui', self)  # Lets load the user interface file
        self.old_status = 1
        self.figure = figure
        self.button = QtWidgets.QPushButton('Health Status: OK', self)
        self.button.resize(410, 40)
        self.button.move(10, 10)
        self.button.setStyleSheet("background-color: green; color: black; font: bold 20px;"
                                  "border: 3px solid black")

    def status_bar(self):
        # To connect to our mongodb server
        client = MongoClient(host=['129.25.20.11:27017'])
        db = client.shm_data  # This is our collection
        collection = db.status_id

        # To read the status from Mongo
        status = collection.find_one({})['status']
        client.close()

        if status == self.old_status:
            pass
        elif status == 2:
            self.old_status = status
            self.button.setText('Health Status: Damage Initiated')
            self.button.setStyleSheet("background-color: yellow; color: black; font: bold 20px;"
                                      "border: 3px solid black")
        elif status == 3:
            self.old_status = status
            self.button.setText('Health Status: CRITICAL')
            self.button.setStyleSheet("background-color: red; color: black; font: bold 20px;"
                                      "border: 3px solid black")

    def change_button_color(self):
        count = 0
        while count < 3:
            count += 1
            self.button.setStyleSheet("background-color: green; color: black; font: bold 20px;"
                                      "border: 3px solid black")
            sleep(1)
            self.button.setStyleSheet("background-color: black; color: black; font: bold 20px;"
                                      "border: 3px solid black")
            sleep(1)

    def layout(self):
        self.setWindowIcon(QtGui.QIcon('drexel.png'))

        # plot
        plot_widget = FigureCanvas(self.figure)
        lay = QtWidgets.QVBoxLayout(self.content_plot)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(plot_widget)

        # code to add a toolbar
        # self.addToolBar(QtCore.Qt.BottomToolBarArea, NavigationToolbar(self.plotWidget, self))


if __name__ == '__main__':
    # Initializing the figure
    fig, ((axx1, axx2), (axx3, axx4)) = plt.subplots(2, 2)
    fig.patch.set_facecolor((0.96, 0.968, 0.851))

    # Initializing GUI
    window = MyWindow(fig)
    window.layout()
    window.show()
    app = QtWidgets.QApplication(sys.argv)

    # Initializing Animation
    data_plotter = FogDataPlotter()
    simulation = animation.FuncAnimation(fig, data_plotter.update_data, repeat=False, fargs=(axx1, axx2, axx3, axx4,
                                                                                             window))

    # Exit program
    sys.exit(app.exec_())
