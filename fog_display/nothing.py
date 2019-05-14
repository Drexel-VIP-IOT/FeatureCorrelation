#!/usr/bin/python3
# By Rakeen Rouf
import sys
from PyQt5 import QtWidgets, QtGui, uic
import matplotlib.pylab as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib
import math
import time
import matplotlib.animation as animation
import pandas as pd
# By Rakeen Rouf
from pymongo import MongoClient


matplotlib.use('QT5Agg')


class FogDataPlotter:
    def __init__(self):
        self.fig_iter_num = 0
        self.v = 0
        self.iv = 0

    def update_data(self, curr, ax1, ax2, ax3, ax4, win):
        start = time.time()
        dataa = pd.read_csv('fog_plot_data.txt')
        time_data = dataa['SSSSSSSS.mmmuuun']

        self.fig_iter_num = curr  # updates figure number

        # for ax in (ax1, ax2, ax3, ax4):  # Lets Clear the plot for the animation
        #    ax.clear()

        try:
            ax1.scatter(dataa['DURATION'], dataa['RISE'], color='b', edgecolor='k')
            ax1.set_ylabel('Rise(μs)', weight='bold', fontsize=12)
            ax1.set_xlabel('Duration(μs)', weight='bold', fontsize=12)

            ax4.plot(time_data, dataa['ABS-ENERGY'].cumsum(), 'b', linewidth=2)
            ax4.set_ylabel('Cumilative Energy(aJ)', weight='bold', fontsize=12)
            ax4.set_xlabel('Time(s)', weight='bold', fontsize=12)

            dur_data = dataa['DURATION']
            min_dur = int(math.floor(dur_data.min()))
            max_dur = int(math.floor(dur_data.max()))

            ax3.hist(dur_data.dropna(), bins=range(min_dur, max_dur + 100, 100), facecolor='blue', alpha=1,
                     edgecolor='black', linewidth=.8)
            ax3.set_xlabel('Duration(μs)', weight='bold', fontsize=12)
            ax3.set_ylabel('Count', weight='bold', fontsize=12)

            amp_data = dataa['AMP']
            min_amp = int(math.floor(amp_data.min()))
            max_amp = int(math.floor(amp_data.max()))

            ax2.hist(amp_data.dropna(), bins=range(min_amp, max_amp + 1, 1), facecolor='blue', alpha=1,
                     edgecolor='black', linewidth=.5)
            ax2.set_xlabel('Amplitude(db)', weight='bold', fontsize=12)
            ax2.set_ylabel('Count', weight='bold', fontsize=12)

            win.status_bar()
            print(time.time() - start)

        except Exception as e:
            print(repr(e))


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self, figure):
        super(MyWindow, self).__init__()
        uic.loadUi('test.ui', self)
        self.old_status = 1
        self.figure = figure
        self.button = QtWidgets.QPushButton('Health Status: OK', self)
        self.button.resize(410, 40)
        self.button.move(10, 10)
        self.button.setStyleSheet("background-color: green; color: black; font: bold 20px;"
                                  "border: 3px solid black")

    def status_bar(self):
        # To connect to our mongodb server
        # client = MongoClient(host=['129.25.20.11:27017'])
        # db = client.shm_data  # This is our collection
        # collection = db.statusid

        # To read the status from Mongo
        # status = collection.find_one({})['status']
        # client.close()

        status = 0

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
            time.sleep(1)
            self.button.setStyleSheet("background-color: black; color: black; font: bold 20px;"
                                      "border: 3px solid black")
            time.sleep(1)

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

    for ax in (axx1, axx2, axx3, axx4):  # Lets Clear the plot for the animation
        ax.ion()

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
