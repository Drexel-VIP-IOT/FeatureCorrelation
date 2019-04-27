# By Rakeen Rouf
import matplotlib.pyplot as plt
import math
import time
import matplotlib.animation as animation


class FogDataPlotter:
    def __init__(self):
        self.fig_iter_num = 0

    def update_data(self, curr, ax1, ax2, ax3, ax4):
        start = time.time()
        self.fig_iter_num = curr

        graph_data = open('C:/Users/rakee/Downloads/fog_plot_data.txt', 'r').read()
        lines = graph_data.split('\n')
        time_data = []
        cum_sum_data = []
        dur_data = []
        amp_data = []

        for line in lines[1:]:
            if len(line[1:]) > 1:
                data_points = line.split(',')
                time_data.append(float(data_points[1]))
                cum_sum_data.append(float(data_points[2]))
                dur_data.append(float(data_points[3]))
                amp_data.append(float(data_points[4]))

        for ax in (ax1, ax2, ax3, ax4):  # Lets Clear the plot for the animation
            ax.clear()

        try:  # Lets try to update our animation
            ax3.plot(time_data, cum_sum_data, 'b', linewidth=2)
            plt.setp(ax3.xaxis.get_majorticklabels(), rotation=90)
            ax3.set_ylabel('Cumilative Energy')
            ax3.set_xlabel('Time')

            dur_data = dur_data
            min_dur = int(math.floor(min(dur_data)))
            max_dur = int(math.floor(max(dur_data)))
            ax4.hist(dur_data, bins=range(min_dur, max_dur + 100, 100), facecolor='blue', alpha=0.5,
                     edgecolor='black', linewidth=1.2, normed=True)
            ax4.set_xlabel('Duration')

            amp_data = amp_data
            min_amp = int(math.floor(min(amp_data)))
            max_amp = int(math.floor(max(amp_data)))
            ax2.hist(amp_data, bins=range(min_amp, max_amp + 1, 1), facecolor='blue', alpha=0.5,
                     edgecolor='black', linewidth=1.2, normed=True)
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
    plt.show()
