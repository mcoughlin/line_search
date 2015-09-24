import numpy as np
import math as math
import os,sys,optparse
import scipy.io
import matplotlib.pyplot as plt

import os
from bokeh.plotting import * 
from bokeh.objects import HoverTool
from collections import OrderedDict
from bokeh.resources import CDN
from bokeh.embed import components

import h5py

# Calls makeBokehMatrix.py an appropriate number of times given maximum number 
# of frequencies you want in a given coherence matrix. You can input maximum 
# number of frequencies with the -f flag. 

def parse_commandline():
    """ 
    Parse the options given on the command-line.
    """
    parser = optparse.OptionParser()

    parser.add_option("-i", "--inputFile", help="input mat file that contains coherence data",default="./lock.mat")
    parser.add_option("-o", "--outputFile", help="output prefix for data",default="./STAMP_COH.html")
    parser.add_option("-f", "--maxFreqs", help="maximum number of frequencies in a single matrix.",default=500) 
    parser.add_option("--fmax", type=float, default=None)
    parser.add_option("--fmin", type=float, default=None)
    parser.add_option("--vmax", type=float, default=0)
    parser.add_option("--vmin", type=float, default=-4)

    opts, args = parser.parse_args()

    return opts

opts = parse_commandline()

def pcolormeshPlot(chnls,ff,coh,cohSNR,color,opts):
    ff = np.asarray(ff)
    #reshape_rows = np.minimum(len(ff),opts.maxFreqs)
    reshape_rows = len(ff)
    reshape_cols = len(chnlsCount)/reshape_rows
    coh2 = np.asarray(coh).reshape((reshape_rows,reshape_cols))
    coh2 = np.transpose(coh2)
    #coh2 = np.vstack((coh2,(np.zeros(1,ff.size))))
    #coh2 = np.hstack((coh2,(np.zeros(len(chnls)/len(ff)+1,1))))
    x = ff
    y = np.arange(0,len(chnls)/len(ff)+1)
    X,Y = np.meshgrid(x,y)
    fig = plt.figure()
    plt.pcolormesh(X,Y,coh2,vmin=opts.vmin,vmax=opts.vmax)
    plt.colorbar()
    plt.xlabel('frequency')
    plt.ylabel('channels')
    plt.axis([ff[0], ff[len(ff)-1], 0, len(chnls)/len(ff)])
    plt.savefig(opts.outputFile+'-pcmesh-'+str(int(freqs[0]))+'_'+str(int(freqs[-1]))+'.png')

# Make bokeh plot for requested frequency bands
def makeMatrix(chnls, chnlsCount, freqs, coh, cohSNR, color, opts, TOOLS):
    """ 
    Make the coherence matrix plot.
    """

    outputFile = str(opts.outputFile)
    directoryStructure = outputFile.split('/')
    sourcetitle = directoryStructure[len(directoryStructure)-1]
    directoryStructurein = str(opts.inputFile).split('/')
    titlename = directoryStructurein[len(directoryStructurein)-1]
    titleForPlot = titlename.split('_');
    titleForPlot = titleForPlot[len(titleForPlot)-1]
    freqs = np.array(map(float,freqs))
    chnlsCount = np.array(map(int,chnlsCount))
    source = ColumnDataSource(
                data=dict(
                     chnlsCount=chnlsCount,
                     chnls=chnls,
                     freqs=freqs,
                     color=color,
                     coh=coh,
                     cohSNR=cohSNR,
                )
    )

    reset_output()
    #output_file(str(opts.outputFile) + "_" + str(int(freqs[0])) + "-" + str(int(freqs[-1])) + ".html", mode="cdn")
    hold()
    plot = rect(freqs, chnlsCount, 1, 1, source=source, fill_color=color, 
                line_color=None, fill_alpha=1, tools=TOOLS, 
                title="coherence of DARM with other channels " + 
                "("+titleForPlot[0:-4]+")",
                plot_width=1775, plot_height=813, x_range=[min(freqs), 
                max(freqs)], y_range=[min(chnlsCount), max(chnlsCount)])

    grid().grid_line_color = None
    yaxis().axis_line_color = None
    yaxis().major_tick_line_color = None
    axis()[1].ticker.num_minor_ticks = 0
    yaxis().major_label_text_font_size = "0pt"
    yaxis().minor_label_text_font_size = "0pt"
    xaxis().major_label_text_font_size = "15pt"
    axis().major_label_standoff = 0
    xaxis().axis_label='Freq (Hz)'
    xaxis().axis_label_text_font_size = "18pt"
    yaxis().axis_label='HAM4/5/6       ETMY                 ETMX              ITMX              ITMY       BS  IMC     PSL ALS/C'
    yaxis().axis_label_text_font_size = "13pt"
    
    hover = [t for t in curplot().tools if isinstance(t, HoverTool)][0]
    hover.tooltips = OrderedDict([('(f,chnl)','(@freqs Hz, @chnls)'),('(Coh,CohSNR)','(@coh, @cohSNR)')])

    script, div = components(plot, CDN)
    outFile = open(str(opts.outputFile) + "_" + str(int(freqs[0])) + "-" + str(int(freqs[-1])) + "_script", "w")
    outFile.write("%s" % script[32:-10])
    outFile.close()

    outhtmlFile = open(str(opts.outputFile) + "_" + str(int(freqs[0])) + "-" + str(int(freqs[-1])) + ".html", "w")
    outhtmlFile.write("<!DOCTYPE html> \n<html lang=\"en\"> \n\t<head>")
    outhtmlFile.write("\n\t\t<meta charset=\"utf-8\">\n\t\t<title>STAMP-PEM COH</title>")
    outhtmlFile.write("\n\t\t<link rel=\"stylesheet\" href=\"bokeh-0.6.1.css\" type=\"text/css\" />")
    outhtmlFile.write("\n\t\t<script type=\"text/javascript\" src=\"bokeh-0.6.1.js\"></script>")
    outhtmlFile.write("\n\t\t<script type=\"text/javascript\">\n\t\t\tBokeh.set_log_level(\"info\");\n\t\t</script>")
    outhtmlFile.write("\n\t<script type=\"text/javascript\" src=\"%s_%s-%s_script\"></script>"%(sourcetitle,str(int(freqs[0])),str(int(freqs[-1]))))
    outhtmlFile.write("\n\t</head>\n\t<body>")
    outhtmlFile.write("\n\t\t<TABLE>\n\t\t\t<TR>")
    outhtmlFile.write("\n\t\t\t<TD>%s</TD>" % div)
    outhtmlFile.write("\n\t\t\t <TD> <img src=\"colorbar.png\"> </TD>")
    outhtmlFile.write("\n\t\t\t</TR>\n\t\t</TABLE>\n\t</body>\n</html>")
    outhtmlFile.close()
    printTopng = "./bokeh/phantomjs ./bokeh/rasterize.js %s_%s-%s.html %s_%s-%s.png" %(str(opts.outputFile),str(int(freqs[0])),str(int(freqs[-1])),str(opts.outputFile),str(int(freqs[0])),str(int(freqs[-1])))
    os.system(printTopng)
  
    #show()

# Make matrix plots for various frequency ranges

TOOLS="pan,wheel_zoom,box_zoom,reset,hover,previewsave"

# Load data file
#cohmat = scipy.io.loadmat(str(opts.inputFile), squeeze_me=True)
cohmat = h5py.File(opts.inputFile,'r')
ff = np.array(cohmat["ff"].value)[0]
coherence_matrix = np.array(cohmat["coherence_matrix"].value)
chnlnames = []
for column in cohmat["chnlnames"]:
    chnlnames.append(''.join(map(unichr, cohmat[column[0]][:])))

df = ff[1] - ff[0]
chnlnames0 = [str(item)[3:] for item in chnlnames]
chnlnames = chnlnames0[::-1]
data0 = coherence_matrix.T
data = data0[::-1]

indexes = np.intersect1d(np.where(ff >= opts.fmin)[0],np.where(ff <= opts.fmax)[0])
ff = ff[indexes]
data = data[:,indexes]

print "Number of frequency bins: %d"%len(ff)
print "Number of channels: %d"%len(chnlnames)
print "Analyzing %.5f - %.5f Hz"%(ff[0],ff[-1])

# Colormap definitions
colors = ["#00008F", "#00009F", "#0000AF", "#0000BF", "#0000CF", "#0000DF", "#0000EF", "#0000FF", "#0010FF", "#0020FF", "#0030FF", "#0040FF", "#0050FF", "#0060FF", "#0070FF", "#0080FF", "#008FFF", "#009FFF", "#00AFFF", "#00BFFF", "#00CFFF", "#00DFFF", "#00EFFF", "#00FFFF", "#10FFEF", "#20FFDF", "#30FFCF", "#40FFBF", "#50FFAF", "#60FF9F", "#70FF8F", "#80FF80", "#8FFF70", "#9FFF60", "#AFFF50", "#BFFF40", "#CFFF30", "#DFFF20", "#EFFF10", "#FFFF00", "#FFEF00", "#FFDF00", "#FFCF00", "#FFBF00", "#FFAF00", "#FF9F00", "#FF8F00", "#FF8000", "#FF7000", "#FF6000", "#FF5000", "#FF4000", "#FF3000", "#FF2000", "#FF1000", "#FF0000", "#EF0000", "#DF0000", "#CF0000", "#BF0000", "#AF0000", "#9F0000", "#8F0000", "#800000"]

cohs = np.linspace(opts.vmin,opts.vmax,len(colors))

chnls = []
freqs = []
color = []
coh = []
cohSNR = []
chnlsCount = []
for f in xrange(len(ff)):
    for c in range(0,len(chnlnames)):
        #for c in [0]:
        chnls.append(chnlnames[c])
        chnlsCount.append(c)
        freqs.append(ff[f])
        coh_value = data[c][f]
        coh_value = np.log10(coh_value)

        if np.isnan(coh_value):
            coh_value = 0
            coh_value = -4

        index = np.argmin(np.abs(cohs-coh_value))
        color.append(colors[index])
        coh.append(coh_value)
        cohSNR.append(coh_value)

ff = np.asarray(ff)
pcolormeshPlot(chnls,ff,coh,cohSNR,color,opts)
makeMatrix(chnls, chnlsCount, freqs, coh, cohSNR, color, opts, TOOLS)

