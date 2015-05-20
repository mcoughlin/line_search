#!/usr/bin/env python
"""Nickolas Fotopoulos (nvf@gravity.phys.uwm.edu)

Library to read and write dictionaries in a variety of formats.  When run
directly, can convert any input type to any output type.
"""

import cPickle
import os.path as p
import sys

__author__ = "Nickolas Fotopoulos <nvf@gravity.phys.uwm.edu>"

def pickle_iterator(file_obj):
    """
    This iterator iterates over objects stored in a pickle file with
    consecutive calls to pickler.dump().
    """
    unpickler = cPickle.Unpickler(file_obj)
    while True:
        try:
            yield unpickler.load()
        except EOFError:
            raise StopIteration

def save_dict(filename, data_dict, file_handle=None):
    """
    Dump a dictionary to file.  Do something intelligent with the filename
    extension.  Supported file extensions are:
    * .pickle - Python pickle file (dictionary serialized unchanged)
    * .pickle.gz - gzipped pickle (dictionary serialized unchanged)
    * .mat - Matlab v4 file (dictionary keys become variable names; requires
             Scipy)
    * .txt - ASCII text (dictionary keys become column headers prefixed by #;
             space-separated rows; non-ndarray dict values will have their
             str() representation written to a # comment)
    * .txt.gz - gzipped ASCII text
    For all formats but .mat, we can write to file_handle directly.
    """
    if filename == '':
        raise ValueError, "Empty filename"
    
    ext = p.splitext(filename)[-1]
    
    ## .mat is a special case, unfortunately
    if ext == '.mat':
        if file_handle is not None:
            print >>sys.stderr, "Cannot write to a given file_handle with",\
                ".mat format.  Attempting to ignore."
        import scipy.io
        scipy.io.savemat(filename, data_dict)
        return
    
    ## Set up file_handle
    if file_handle is None:
        file_handle = file(filename, 'wb')
    
    # For gz files, bind file_handle to a gzip file and find the new extension
    if ext == '.gz':
        import gzip
        file_handle = gzip.GzipFile(fileobj=file_handle, mode='wb')
        ext = p.splitext(filename[:-len(ext)])[-1]
    
    ## Prepare output
    if ext == '.pickle':
        import cPickle
        output = cPickle.dumps(data_dict, -1) # -1 means newest format
    elif ext == '.txt':
        import numpy
        
        # (key, val) list
        array_keys = [key for key,val in data_dict.items() if \
                      type(val)==numpy.ndarray]
        array_vals = [val for key,val in data_dict.items() if \
                      type(val)==numpy.ndarray]
        non_arrays = [(key,val) for key,val in data_dict.items() if \
                      type(val)!=numpy.ndarray]
        
        # Header of non-arrays and array column labels
        lines = []  # string list
        for key,val in non_arrays:
            lines += ['# %s = %s' % (key, val) ]
        lines += ['# ' + ' '.join([str(key) for key in array_keys])]
        
        # Main data
        # Check that all lengths are equal; gracefully handle empty arrays
        array_lengths = [len(a) for a in array_vals]
        assert numpy.alltrue(array_lengths[:-1]==array_lengths[1:])
        
        row_data = zip(*array_vals)  # Do a transpose
        lines += [' '.join(map(str,row)) for row in row_data]
        
        # Remove extra lines
        lines = [x for x in lines if x!=[]]
        
        output = '\n'.join(lines)
    else:
        raise ValueError, "Unrecognized file extension"
    
    ## Write output
    file_handle.write(output)

def load_dict(filename, file_handle=None):
    """
    Read in dictionary from a file or filehandle.  Even if a file handle
    is provided, we will read extension information from filename.  .pickle,
    .pickle.gz, and .mat are supported.
    """
    if filename == '':
        raise ValueError, "Empty filename"
    
    ext = p.splitext(filename)[-1]
    
    ## .mat is a special case, unfortunately
    if ext == '.mat':
        if file_handle is not None:
            print >>sys.stderr, "Cannot read from a given file_handle with",\
                ".mat format.  Attempting to ignore."
        import scipy.io
        return scipy.io.loadmat(filename)
    
    ## Set up file_handle
    if file_handle is None:
        file_handle = file(filename, 'rb')
    
    # For gz files, bind file_handle to a gzip file and find the new extension
    if ext == '.gz':
        import gzip
        file_handle = gzip.GzipFile(fileobj=file_handle, mode='rb')
        ext = p.splitext(filename[:-len(ext)])[-1]
    
    if ext == '.pickle':
        import cPickle
        return cPickle.load(file_handle)
    else:
        raise ValueError, "Unrecognized file extension"

if __name__ == "__main__":
    import glob, optparse
    from pycoh import git_version
    
    parser = optparse.OptionParser(version=git_version.verbose_msg)
    parser.add_option("-i", "--input", dest="input_glob",
                      help="input file(s)")
    parser.add_option("-o", "--output", dest="output_extension",
                      help="extension for the desired output format")
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose",
                      default=False, help="print status messages to stdout")
    
    (options, args) = parser.parse_args()
    
    ## Error checking
    if None in (options.input_glob, options.output_extension):
        print "Both --input and --output options required!"
        sys.exit(2)
    
    if options.verbose and len(args)!=0:
        print "Ignoring arguments."
    
    ## Determine input files
    input_files = glob.glob(options.input_glob)
    
    if options.verbose:
        print "Files matching input glob:", input_files
    
    ## Reformat extension
    if options.output_extension[0:1] != '.':
        options.output_extension = '.' + options.output_extension
    
    ## Go!
    def strip_ext(s):
        return p.splitext(s)[0]
    for infile in input_files:
        outfile = strip_ext(strip_ext(infile)) + options.output_extension
        save_dict(outfile, load_dict(infile))
    
    if options.verbose:
        print "Done!"
