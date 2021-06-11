# -*- coding: utf-8 -*-
import numpy as np
from matplotlib import pyplot
import matplotlib.pyplot as plt


def plot_comparison_hist(values, labels, colors, x_label, y_label, indexes=0):
    for i, item in enumerate(values):
        pyplot.hist(item, color=colors[i], bins=100, alpha=0.5, label=labels[i])
    pyplot.xlabel(x_label)
    pyplot.ylabel(y_label)
    pyplot.legend(loc='upper left')
    if indexes==0:
        pyplot.savefig(f"./results/hist_influence_in_sample"".png")
    elif indexes==1:
        pyplot.savefig(f"./results/hist_influence_out_of_sample"".png")
    pyplot.close()
