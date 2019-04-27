# By Rakeen Rouf
import pandas as pd
import matplotlib.pyplot as plt
import math
import numpy as np
from scipy.spatial import distance
import matplotlib.animation as animation
import os


class CloudDataPlotter:

    def __init__(self):
        self.data = pd.DataFrame()
        self.fig_iter_num = 0
        self.k = 15
        self.b=0

    def update_data(self, curr, ax1, ax2, ax3, ax4):

        self.fig_iter_num = curr
        try:

            data = pd.read_csv('fog_plot_data.txt')
            print(data.shape[0])
            print(self.k)

            if self.k < data.shape[0]:
                self.k = data.shape[0]
                msd = np.empty(data.shape[0])
                time_data = data['SSSSSSSS.mmmuuun']
                cum_sum_data = data['cum_sum_ENER']
                dur_data = data['DURATION']
                amp_data = data['AMP']
                Data = data.drop(['SSSSSSSS.mmmuuun'], axis=1).values

                v = np.mean(Data[0:14, :], axis=0)
                COV = np.cov(Data, rowvar=False)
                COV[np.isnan(COV)]=0
                iv = np.linalg.pinv(COV)

                for x in range(1, data.shape[0]):
                    msd[x] = distance.mahalanobis(Data[x, :], v, iv)
                cmsd = np.cumsum(msd)

                for ax in (ax1, ax2, ax3, ax4):  # Lets Clear the plot for the animation
                    ax.clear()

                    try:  # Lets try to update our animation

                        ax3.plot(time_data, cum_sum_data, 'b', linewidth=2)
                        plt.setp(ax3.xaxis.get_majorticklabels(), rotation=90)
                        ax3.set_ylabel('Cumulative Energy')
                        ax3.set_xlabel('Time')


                        ax1.plot(time_data,cmsd, 'b', linewidth=2)
                        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=90)
                        ax1.set_ylabel('Cumulative Mahalanobis Distance')
                        ax1.set_xlabel('Time')


                        min_dur = int(math.floor(min(dur_data)))
                        max_dur = int(math.floor(max(dur_data)))
                        ax4.hist(dur_data, bins=range(min_dur, max_dur + 100, 100), facecolor='blue', alpha=0.5,
                                 edgecolor='black', linewidth=1.2, normed=True)
                        ax4.set_xlabel('Duration')


                        min_amp = int(math.floor(min(amp_data)))
                        max_amp = int(math.floor(max(amp_data)))
                        ax2.hist(amp_data, bins=range(min_amp, max_amp + 1, 1), facecolor='blue', alpha=0.5,
                                 edgecolor='black', linewidth=1.2, normed=True)
                        ax2.set_xlabel('Amplitude')
                        fi = 'livecloud' + str(self.b) + '.png'
                        self.b=self.b+1
                        print(fi)
                        THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
                        #print(THIS_FOLDER)
                        file = os.path.join(THIS_FOLDER, fi)
                    # file=' C:/Users/kwm38/Desktop/FOG/'+fi
                        plt.savefig(file)

                    except Exception as e:
                        print(repr(e))

        except pd.io.common.EmptyDataError:
            df = pd.DataFrame()


if __name__ == '__main__':
    data_plotter = CloudDataPlotter()
    fig, ((axx1, axx2), (axx3, axx4)) = plt.subplots(2, 2)
    simulation = animation.FuncAnimation(fig, data_plotter.update_data, repeat=False, fargs=(axx1, axx2, axx3, axx4))
    plt.show()
