"""."""
import iogui
import matplotlib.pyplot as plt


def getdata(instructions, n=1, endlinechar="end"):
    """Collect data and return it in a vector of vector.

    The output vector's has the format [position , data1, data2]
    position -- data in the first column of the input file
    data1 -- data in the second column of the file
    data2 -- data in the third column of the file

    Input parameters:
    instructions -- Instructions for the file tree window that opens when the
    user choose the data.
    """
    file_ = iogui.pickfiles(instructions)
    with open(file_[0]) as f:
        textdata = f.read().split(endlinechar)
        # textdata[0] contains the line with the lable, textdata[1] contains
        # the rest of the file
    data = textdata[1].splitlines()
    data.pop(0)
    return splitcolumns(data)


def splitcolumns(data):
    """Split the a text file that has been split in lines into columns."""
    datamatrix = []
    templine = data[0]
    templine = templine.split()
    datanumber = len(templine)
    datamatrix = []
    for i in range(datanumber):
        datamatrix.append([])
    for line in data:
        number = line.split()
        for idx, n in enumerate(number):
            datamatrix[idx].append(n)
    return datamatrix


def lngraphfromdata(xdata, ydata, legend=None, name="Graph", filetype=".png",
                    xerr=None, yerr=None, pxerr=0, pyerr=0):
    """Make a graph using the data given in parameters."""
    if not (len(xdata) == 1 or len(xdata) == len(ydata)):
        print(len(xdata))
        print(len(ydata))
        print("Tried to make a graph with data that didn't have the same" +
              " number of x data set as the number of y data set. " +
              "If the all y data sets have the same x data set, xdata should" +
              " be an array containing only one array")
        return 0
    if legend is None or len(legend) != len(ydata):
        legend = []
        for x in range(len(ydata)):
            legend.append("")
    plt.figure(figsize=(18.5, 10.5))
    plt.xlim(0, 35)
    plt.ylim(0.01, 105)
    plt.xlabel("Position from Isocenter(cm)")
    plt.ylabel("Percent of isocenter dose")
    if (len(xdata) == 1):
        x = xdata[0]
        x = [float(i) for i in x]
        for idx, y in enumerate(ydata):
            y = [float(i) for i in y]
            plt.plot(x, y, 'o', label=legend[idx])
            if pxerr != 0:
                xerr = [pxerr*float(datapoint) for datapoint in x]
            if yerr != 0:
                yerr = [pyerr*float(datapoint) for datapoint in y]
            plt.errorbar(x, y, xerr=xerr, yerr=yerr, fmt='none', mec='black')
    else:
        for idx, (x, y) in zip(xdata, ydata):
            x = [float(i) for i in x]
            y = [float(i) for i in y]
            plt.plot(x, y, "o", label=legend[idx])
            if pxerr != 0:
                xerr = [pxerr*float(datapoint) for datapoint in x]
            if yerr != 0:
                yerr = [pyerr*float(datapoint) for datapoint in y]
            plt.errorbar(x, y, xerr=xerr, yerr=yerr, fmt='none', mec='black')
    plt.yscale('log')
    plt.axvline(x=3.5, ymin=0.01, ymax=105, ls='--', color="red",
                label="PTV edge")
    plt.legend()
    plt.savefig(name + filetype)
    return 1


def normalize(data, factor=None):
    """Normalize the data in the array to the first data in the array."""
    normdata = data
    for idx, array in enumerate(data):
        if factor is None:
            normdata[idx][:] = [float(datapoint)/float(normdata[idx][0])*100
                                for datapoint in normdata[idx]]
        else:
            normdata[idx][:] = [float(datapoint)/float(factor)*100
                                for datapoint in normdata[idx]]
    return normdata


def choosecolumngraph(column, legend=None, name=None, pxerr=0, pyerr=0):
    """Draw semilogy graph with data column whose index are given as input."""
    datamatrix = getdata("The Data")
    xdata = [datamatrix[0]]
    ydata = []
    for idx in column:
        ydata.append(datamatrix[idx])
    ydata = normalize(ydata, 1000)
    if name is None:
        name = "myGraph"
    lngraphfromdata(xdata, ydata, legend=legend, name=name, pxerr=pxerr,
                    pyerr=pyerr)


def graphfromdata(xdata, ydata, legend=None, name="Graph", filetype=".png",
                  xerr=None, yerr=None, pxerr=0, pyerr=0, uylim=100,
                  lylim=0, yhline=0, ylabel="Percent of isocenter dose"):
    """Make a graph using the data given in parameters."""
    if not (len(xdata) == 1 or len(xdata) == len(ydata)):
        print(len(xdata))
        print(len(ydata))
        print("Tried to make a graph with data that didn't have the same" +
              " number of x data set as the number of y data set. " +
              "If the all y data sets have the same x data set, xdata should" +
              " be an array containing only one array")
        return 0
    if legend is None or len(legend) != len(ydata):
        legend = []
        for x in range(len(ydata)):
            legend.append("")
    plt.figure(figsize=(18.5, 10.5))
    plt.xlim(-2, 35)
    plt.ylim(lylim, uylim)
    plt.xlabel("Position from Isocenter(cm)")
    plt.ylabel(ylabel)
    if (len(xdata) == 1):
        x = xdata[0]
        x = [float(i) for i in x]
        for idx, y in enumerate(ydata):
            y = [float(i) for i in y]
            plt.plot(x, y, '-', label=legend[idx])
            if pxerr != 0:
                xerr = [pxerr*float(datapoint) for datapoint in x]
            if yerr != 0:
                yerr = [pyerr*float(datapoint) for datapoint in y]
            plt.errorbar(x, y, xerr=xerr, yerr=yerr, fmt='none',
                         ecolor='black')
    else:
        for idx, (x, y) in zip(xdata, ydata):
            x = [float(i) for i in x]
            y = [float(i) for i in y]
            plt.plot(x, y, "-", label=legend[idx])
            if pxerr != 0:
                xerr = [pxerr*float(datapoint) for datapoint in x]
            if yerr != 0:
                yerr = [pyerr*float(datapoint) for datapoint in y]
            plt.errorbar(x, y, xerr=xerr, yerr=yerr, fmt='none',
                         ecolor='black')
    plt.axhline(y=yhline, xmin=-2, xmax=35, color='black', ls='--')
    plt.axvline(x=3.5, ymin=lylim, ymax=uylim, ls='--', color="red",
                label="PTV edge")
    plt.legend()
    plt.savefig(name + filetype)
    return 1


def drawabsolutedifference(column, legend=None, name=None, pxerr=0, pyerr=0,
                           ylim=10,
                           ylabel="Absolute normalized difference"):
    """."""
    datamatrix = getdata("The Data")
    xdata = [datamatrix[0]]
    tempydata = []
    ydata = []
    for idx in column:
        tempydata.append(datamatrix[idx])
    for datacolumn in tempydata:
        data = []
        for idx, datapoint in enumerate(datacolumn):
            data.append(float(tempydata[0][idx])-float(datapoint))
        ydata.append(data)
    ydata = normalize(ydata, 1000)
    ydata.pop(0)
    if name is None:
        name = "myGraph"
    graphfromdata(xdata, ydata, legend=legend, name=name, pxerr=pxerr,
                  pyerr=pyerr, uylim=ylim, lylim=-ylim, yhline=0,
                  ylabel=ylabel)


def drawrelativedifference(column, legend=None, name=None, pxerr=0, pyerr=0,
                           ylim=1, ylabel="Relative Dose"):
    """."""
    datamatrix = getdata("The Data")
    xdata = [datamatrix[0]]
    tempydata = []
    ydata = []
    for idx in column:
        tempydata.append(datamatrix[idx])
    for datacolumn in tempydata:
        data = []
        for idx, datapoint in enumerate(datacolumn):
            data.append(float(datapoint)/float(tempydata[0][idx]))
        ydata.append(data)
    ydata.pop(0)  # because ydata[0] is 6x/6x
    if name is None:
        name = "myGraph"
    graphfromdata(xdata, ydata, legend=legend, name=name, pxerr=pxerr,
                  pyerr=pyerr, uylim=ylim, lylim=0, yhline=1,
                  ylabel=ylabel)


def printnumbers(column):
    """."""
    datamatrix = getdata("The Data")
    tempydata = []
    ydata = []
    for idx in column:
        tempydata.append(datamatrix[idx])
    for datacolumn in tempydata:
        data = []
        for idx, datapoint in enumerate(datacolumn):
            data.append(float(datapoint)/float(tempydata[0][idx]))
        ydata.append(data)
    ydata.pop(0)  # because ydata[0] is 6x/6x
    for data in ydata:
        print(data)
        print("\n")
