#!/usr/bin/env python
"""
Tomoki Isogai (isogait@carleton.edu)
    
$Id: plot_coh,v 1.01 2009/2/27$
"""

from __future__ import division
import optparse
import sys
import os
import glob
import cPickle
#import matplotlib
#matplotlib.use('Agg')
from pylab import *

import io

__author__ = "Tomoki Isogai <isogait@carleton.edu>"
__version__ = "$Revision: 1.01 $"[11:-2]

def parse_commandline():
    """
    Parse the options given on the command-line.
    """
    parser = optparse.OptionParser(usage=__doc__,\
                                   version="$Id: plot_coh,v 1.01 2009/2/27")
    parser.add_option("-r", "--result_glob",
                      help="the result files from pycoh in pickle file")
    parser.add_option("-o", "--out_dir", default = "plots",\
        help="an output directory name")
    parser.add_option("-M", "--max_ff", type="float", 
                      help="Max frequency. (Default: max possible)")
    parser.add_option("-m", "--min_ff", type="float",
                      help="Min frequency. (Default: min possible)")
    parser.add_option("-s", "--show_plot", action="store_true",
                      default=False, help="show plot on display")
    parser.add_option("-v", "--verbose", action="store_true",\
                      default=False, help="run verbosely")
    
    opts, args = parser.parse_args()
    
    # check if necessary input exists
    if opts.result_glob is None:
        print >>sys.stderr, "--result_glob is a required parameter"
        sys.exit(1)
        
    # make an output directory if it doesn't exist yet
    if not os.path.exists(opts.out_dir): os.makedirs(opts.out_dir)
        
    # show parameters
    if opts.verbose:
        print
        print "********************** PARAMETERS ******************************"
        print 'glob for result files:'; print opts.result_glob;
        print 'output directory:'; print opts.out_dir;
        print
        
    return opts

def main(opts):
    file_list = glob.glob(opts.result_glob)
    for f in file_list:
        if opts.verbose: 
            print "gathering info from %s"%f

        # get info
        data = io.load_dict(f)
        coh = abs(data['coh'])**2
        ff = data['ff']
        df = data['coh'].metadata.df
        Tchunks = data['Tchunks']
        window_length = [int(o.split()[1]) for o in data['coh'].metadata.comments[0].split("--") if o.startswith('window-length-seconds')][0]
        # figure out 1/N level (expectation value for coherence)
        N = Tchunks * window_length * df
        inv_N = 1/N

        # plot coherence
        if opts.verbose: 
            print "plotting..."
        semilogy(ff,coh,'b',ff,coh,'bo',markersize=3,label='_nolegend_')
        
        # plot 1/N line
        axhline(y=inv_N,c='r',lw=3,label='1/N:\n %e'%inv_N)

        ylim(ymax=1)
        if opts.min_ff is not None:
          min_ff = opts.min_ff
        else:
          min_ff = ff[0]
        if opts.max_ff is not None:
          max_ff = opts.max_ff
        else:
          max_ff = ff[-1]

        xlim([min_ff,max_ff])

        plot_name = os.path.basename(f).split(".")[0]
        title(plot_name,fontsize=12)
        xlabel("frequency (Hz)")
        ylabel("coherence")
        legend(loc='best')
        fileName=plot_name+".png"
        if opts.show_plot:
            if opts.verbose:
                print "showing the plot..."
            show()
        if opts.verbose:
            print "saving..."
        savefig(os.path.join(opts.out_dir,fileName))
        close()

if __name__=="__main__":
    # parse commandline
    opts = parse_commandline()
    # do the work
    main(opts)
