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


def box_plots(values, labelled, x_label, y_label, t_itle, fname, n_repetitions, n_scen):
    # vals=np.zeros([len(values[0]), len(values)])
    # for i in range(len(values)):
    #     for j in range(len(values[0])):
    #         vals[j][i]=values[j][i]
    
        
    pyplot.boxplot(values, labels = labelled)
    pyplot.xlabel(x_label)
    pyplot.ylabel(y_label)
    pyplot.title(t_itle)
    pyplot.grid()
    pyplot.savefig(f"./results/box_plot_"+fname+".png")
    pyplot.close()
 
def bar_plots(values, labelled, x_label, y_label, t_itle, fname, which_sample):
    means = []
    variances = []
    
    for i in values:
        means.append(np.mean(i))
        variances.append((np.var(i))**0.5)
  

    pyplot.errorbar(labelled, means, yerr=variances, linestyle='None', marker='o', ecolor='r', color='k')
    pyplot.xlabel(x_label)
    pyplot.ylabel(y_label)
    pyplot.title(t_itle)
    pyplot.grid()
    pyplot.savefig(f"./results/bar_plot_"+fname+".png")
    pyplot.close()


def bar_plots_gap(values_ex, values_heu, labelled, x_label, y_label, t_itle, fname):
    values=[]
    for j in range(len(values_ex)):
        values.append(abs(values_ex[j][0]-values_heu[j][0])/values_ex[j][0]*100)
    
    means = []
    variances = []
    
    for i in values:
        means.append(np.mean(i))
        variances.append((np.var(i))**0.5)
  

    pyplot.errorbar(labelled, means, yerr=variances, linestyle='None', marker='o', ecolor='r', color='k')
    pyplot.xlabel(x_label)
    pyplot.ylabel(y_label)
    pyplot.title(t_itle)
    pyplot.grid()
    pyplot.savefig(f"./results/bar_plot_"+fname+".png")
    pyplot.close()