from matplotlib import pyplot as plt
from helperFunctions import sort2Lists, sort3Lists, sort4Lists

def singleXYPlot(xs, ys,
                 linestlye = '-', color = 'k',
                 xlabel=None, ylabel=None,
                 legend=None,
                 xlim=None, ylim=None, isSort=False, isShow=True):
    if isSort:
        xs, ys = sort2Lists(xs, ys)
    if legend == None:
        plt.plot(xs, ys)
    else:
        plt.plot(xs, ys, label = legend)
        plt.legend()
    if xlim != None:
        plt.xlim(xlim)
    if ylim != None:
        plt.ylim(ylim)
    if xlabel != None:
        plt.xlabel(xlabel)
    if ylabel != None:
        plt.ylabel(ylabel)
    if isShow:
        plt.show()

def singleXYErrorPlot(xs, ys, xerrs=None, yerrs=None,
                 linestlye = '-', color = 'k',
                 xlabel=None, ylabel=None,
                 legend=None,
                 xlim=None, ylim=None,
                 xscale='linear', yscale='linear',
                 isSort=False, isShow=True):
    if isSort:
        if xerrs == None and yerrs == None:
            xs, ys = sort2Lists(xs, ys)
        elif xerrs != None and yerrs == None:
            xs, ys, xerrs = sort3Lists(xs, ys, xerrs)
        elif xerrs == None and yerrs != None:
            xs, ys, yerrs = sort3Lists(xs, ys, yerrs)
        elif xerrs != None and yerrs != None:
            xs, ys, xerrs, yerrs = sort4Lists(xs, ys, xerrs, yerrs)
    if legend == None:
        if xerrs == None and yerrs == None:
            plt.errorbar(xs, ys)
        elif xerrs != None and yerrs == None:
            plt.errorbar(xs, ys,xerr=xerrs)
        elif xerrs == None and yerrs != None:
            plt.errorbar(xs, ys,yerr=yerrs)
        elif xerrs != None and yerrs != None:
            plt.errorbar(xs, ys,yerr=yerrs, xerr=xerrs)
    else:
        if xerrs == None and yerrs == None:
            plt.errorbar(xs, ys, label = legend)
        elif xerrs != None and yerrs == None:
            plt.errorbar(xs, ys,xerr=xerrs, label = legend)
        elif xerrs == None and yerrs != None:
            plt.errorbar(xs, ys,yerr=yerrs, label = legend)
        elif xerrs != None and yerrs != None:
            plt.errorbar(xs, ys,yerr=yerrs, xerr=xerrs, label = legend)
        plt.legend()
    if xlim != None:
        plt.xlim(xlim)
    if ylim != None:
        plt.ylim(ylim)
    if xlabel != None:
        plt.xlabel(xlabel)
    if ylabel != None:
        plt.ylabel(ylabel)
    plt.xscale(xscale)
    plt.yscale(yscale)
    if isShow:
        plt.show()