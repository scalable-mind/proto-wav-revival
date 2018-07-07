from matplotlib import cm
from matplotlib import gridspec
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
from compressor import compress, decompress
from smoothing import smooth

if __name__ == '__main__':
    sample_rate = 48000
    silence_length = 0.4

    raw_data = np.fromfile('wtf.bin', dtype=np.int8)
    comp_data = compress(raw_data)


    smooth_data = smooth(comp_data, int(sample_rate * silence_length))

    # print(list(filter(lambda x: x > int(sample_rate * silence_length), zeros)))
    # print(list(filter(lambda x: x > int(sample_rate * silence_length), ones)))

    # plt.figure(figsize=(13, 8))
    #
    # ax = plt.subplot(1, 1, 1)
    # ax.set_title("Validation Data")
    #
    # ax.set_autoscaley_on(False)
    # ax.set_ylim([32, 43])
    # ax.set_autoscalex_on(False)
    # # ax.set_xlim([-126, -112])
    # plt.scatter(list(range(int(len(comp_data)))),
    #                  comp_data,
    #             cmap="coolwarm",
    #             c=np.array(comp_data))
    # ax = plt.subplot(1, 2, 1)
    # plt.hist(list(filter(lambda x: x > 20, comp_data[1::2])))
    # ax = plt.subplot(1, 2, 2)
    # plt.hist(list(filter(lambda x: 7 < x < 20, comp_data[1::2])))
    # plt.show()

    print('Raw data size: %d' % len(raw_data))
    print('-----------------')
    print('Compressed data size: %d' % len(comp_data))
    print('-----------------')
    print('Smoothed data size: %d' % len(smooth_data))
    print('-----------------')
    print(smooth_data)
