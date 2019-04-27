# By Rakeen Rouf
import matplotlib.pyplot as plt
import math
import time
import matplotlib.animation as animation
import pandas as pd
import numpy as np
from scipy.spatial import distance


class FogDataPlotter:
    def __init__(self):
        self.fig_iter_num = 0
        self.v = 0
        self.iv = 0

    def update_data(self, curr, ax1, ax2, ax3, ax4):
        start = time.time()
        dataa = pd.read_csv('fog_plot_data.txt')
        time_data = dataa['SSSSSSSS.mmmuuun']
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

        cmsd = np.cumsum(msd)
        self.fig_iter_num = curr  # updates figure number

        for ax in (ax1, ax2, ax3, ax4):  # Lets Clear the plot for the animation
            ax.clear()

        try:  # Lets try to update our animation
            ax1.plot(time_data, cmsd, 'b', linewidth=2)
            plt.setp(ax1.xaxis.get_majorticklabels())
            ax1.set_ylabel('Cumulative Mahalanobis Distance')
            ax1.set_xlabel('Time')

            ax3.plot(time_data, dataa['ABS-ENERGY'].cumsum(), 'b', linewidth=2)
            plt.setp(ax3.xaxis.get_majorticklabels())
            ax3.set_ylabel('Cumilative Energy')
            ax3.set_xlabel('Time')

            dur_data = dataa['DURATION']
            min_dur = int(math.floor(dur_data.min()))
            max_dur = int(math.floor(dur_data.max()))

            ax4.hist(dur_data, bins=range(min_dur, max_dur + 100, 100), facecolor='blue', alpha=0.5,
                     edgecolor='black', linewidth=1.2, density=True)
            ax4.set_xlabel('Duration')

            amp_data = dataa['AMP']
            min_amp = int(math.floor(amp_data.min()))
            max_amp = int(math.floor(amp_data.max()))
            ax2.hist(amp_data, bins=range(min_amp, max_amp + 1, 1), facecolor='blue', alpha=0.5,
                     edgecolor='black', linewidth=1.2, density=True)
            ax2.set_xlabel('Amplitude')

            print(time.time() - start)

        except Exception as e:
            print(repr(e))


if __name__ == '__main__':
    """
    Assumptions
    The first 7 lines of the txt files is not necessary in the plots
    A txt file will always be available
    Only Id=1 rows are used in calculations and plots
    Data is dumped at least after 5 seconds after inception
    """
    data_plotter = FogDataPlotter()
    # data_plotter.loaddata()

    fig, ((axx1, axx2), (axx3, axx4)) = plt.subplots(2, 2)
    simulation = animation.FuncAnimation(fig, data_plotter.update_data, repeat=False, fargs=(axx1, axx2, axx3, axx4))
    plt.tight_layout()
    plt.show()
