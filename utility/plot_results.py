# -*- coding: utf-8 -*-
import numpy as np
from matplotlib import pyplot
import matplotlib.pyplot as plt


def plot_comparison_hist(values, labels, colors, x_label, y_label, indexes=0):
    for i, item in enumerate(values):
        pyplot.hist(item, color=colors[i], bins=100, alpha=0.5, label=labels[i])
    v1=np.mean(values.pop())
    v2=np.mean(values.pop())
    gap=abs(v1-v2)/v1

    pyplot.xlabel(x_label)
    pyplot.ylabel(y_label)
    pyplot.legend(loc='upper left')
    if indexes==0:
        pyplot.title("In-sample gap: "+str(round(gap*100, 3))+" %")
        pyplot.savefig(f"./results/hist_influence_in_sample"+str(indexes)+".png")
    elif indexes==1:
        pyplot.title("Out-of-sample gap: "+str(round(gap*100,3))+" %")
        pyplot.savefig(f"./results/hist_influence_out_of_sample"+str(indexes)+".png")
    pyplot.close()


def box_plots(values, labelled, x_label, y_label, t_itle):

    pyplot.boxplot(values, labels = labelled)
    pyplot.xlabel(x_label)
    pyplot.ylabel(y_label)
    pyplot.title(t_itle)
    pyplot.grid()
    pyplot.savefig(f"./results/box_plot "+t_itle+".png")
    pyplot.close()
 
def bar_plots(values, labelled, x_label, y_label, t_itle, VSS_best=None):
    means = []
    variances = []
    if VSS_best==None:
        for i in values:
            means.append(np.mean(i))
            variances.append((np.var(i))**0.5)
    else:
        
        variances=[]
        for i in values:
            sums=0
            means.append(np.mean(i))
            for j in i:
                sums+=(j-VSS_best)**2
            sums=sums/len(i)
            variances.append((sums)**0.5)

    pyplot.errorbar(labelled, means, yerr=variances, linestyle='None', marker='o', ecolor='r', color='k')
    pyplot.xlabel(x_label)
    pyplot.ylabel(y_label)
    pyplot.title(t_itle)
    pyplot.grid()
    pyplot.savefig(f"./results/bar_plot "+t_itle+".png")
    pyplot.close()