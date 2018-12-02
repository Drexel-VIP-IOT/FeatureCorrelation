# By Rakeen Rouf
import pandas as pd
import matplotlib.pyplot as plt
import math
import time
import matplotlib.animation as animation


class FogDataPlotter:
    def __init__(self):
        self.data = pd.DataFrame()
        self.fig_iter_num = 0


    def loaddata(self):
        # Update the name of the text file here
        self.data = pd.read_fwf('C:/Users/rakee/Downloads/livedata.txt', skiprows=7)
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

        return self.data

    def update_data(self, curr, ax1, ax2, ax3, ax4, data):
        start = time.time()
        self.fig_iter_num = curr

        for ax in (ax1, ax2, ax3, ax4):  # Lets Clear the plot for the animation
            ax.clear()

        try:  # Lets try to update our animation
            ax3.plot(data['SSSSSSSS.mmmuuun'], data['cum_sum_ENER'], 'b', linewidth=2)
            plt.setp(ax3.xaxis.get_majorticklabels(), rotation=90)
            ax3.set_ylabel('Cumilative Energy')
            ax3.set_xlabel('Time')

            dur_data = data['DURATION']
            min_dur = int(math.floor(min(dur_data)))
            max_dur = int(math.floor(max(dur_data)))
            ax4.hist(dur_data, bins=range(min_dur, max_dur + 100, 100), facecolor='blue', alpha=0.5,
                     edgecolor='black', linewidth=1.2, normed=True)
            ax4.set_xlabel('Duration')

            amp_data = data['AMP']
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
    # Lets write a txt file containing all running history
    txt_file_writer = open("History.txt", "w")
    txt_file_writer.write('History\n')
    txt_file_writer.write(str(0))
    txt_file_writer.write('\n')
    txt_file_writer.write(str(0))
    txt_file_writer.close()

    data_plotter = FogDataPlotter()

    fig, ((axx1, axx2), (axx3, axx4)) = plt.subplots(2, 2)
    simulation = animation.FuncAnimation(fig, data_plotter.update_data, repeat=False, fargs=(axx1, axx2, axx3, axx4,
                                                                                             data_plotter.loaddata()))
    plt.show()
