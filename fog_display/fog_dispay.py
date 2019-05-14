#!/usr/bin/python3
# By Rakeen Rouf
import matplotlib.pyplot as plt
import math
import time
import matplotlib.animation as animation
import pandas as pd


class FogDataPlotter:
    def __init__(self):
        self.fig_iter_num = 0
        self.v = 0
        self.iv = 0

    def update_data(self, curr, ax1, ax2, ax3, ax4):
        start = time.time()
        dataa = pd.read_csv('fog_plot_data.txt')
        time_data = dataa['SSSSSSSS.mmmuuun']

        self.fig_iter_num = curr  # updates figure number

        for ax in (ax1, ax2, ax3, ax4):  # Lets Clear the plot for the animation
            ax.clear()

        try:  # Lets try to update our animation
            ax1.scatter(dataa['DURATION'], dataa['RISE'], color='b', edgecolor='k')
            ax1.set_ylabel('Rise/μs', weight='bold', fontsize=12)
            ax1.set_xlabel('Duration/μs', weight='bold', fontsize=12)

            ax4.plot(time_data, dataa['ABS-ENERGY'].cumsum(), 'b', linewidth=2)
            ax4.set_ylabel('Cumilative Energy/aJ', weight='bold', fontsize=12)
            ax4.set_xlabel('Time/s', weight='bold', fontsize=12)

            dur_data = dataa['DURATION']
            min_dur = int(math.floor(dur_data.min()))
            max_dur = int(math.floor(dur_data.max()))

            ax3.hist(dur_data, bins=range(min_dur, max_dur + 100, 100), facecolor='blue', alpha=1,
                     edgecolor='black', linewidth=.8)
            ax3.set_xlabel('Duration/μs', weight='bold', fontsize=12)
            ax3.set_ylabel('Count', weight='bold', fontsize=12)

            amp_data = dataa['AMP']
            min_amp = int(math.floor(amp_data.min()))
            max_amp = int(math.floor(amp_data.max()))

            ax2.hist(amp_data, bins=range(min_amp, max_amp + 1, 1), facecolor='blue', alpha=1,
                     edgecolor='black', linewidth=.5)
            ax2.set_xlabel('Amplitude/db', weight='bold', fontsize=12)
            ax2.set_ylabel('Count', weight='bold', fontsize=12)

            print(time.time() - start)

        except Exception as e:
            print(repr(e))


if __name__ == '__main__':
    """
    Assumptions
    Data is dumped at least after 5 seconds after inception
    """
    data_plotter = FogDataPlotter()
    # data_plotter.loaddata()

    fig, ((axx1, axx2), (axx3, axx4)) = plt.subplots(2, 2)
    fig.suptitle('    Fog View', fontsize=18, weight='bold')
    fig.text(.485, .5, '.', fontsize='200', color='g')
    fig.patch.set_facecolor((0.96, 0.968, 0.851))

    simulation = animation.FuncAnimation(fig, data_plotter.update_data, repeat=False, fargs=(axx1, axx2, axx3, axx4))
    plt.tight_layout()
    plt.show()
