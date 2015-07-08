# Source this file to access PYCOH
setenv PYCOH_PREFIX =/home/eric.coughlin/opt_pycoh
setenv PATH =/home/eric.coughlin/opt_pycoh/bin:${PATH}
if ( $?PYTHONPATH ) then
  setenv PYTHONPATH =/home/eric.coughlin/opt_pycoh/lib64/python2.6/site-packages:=/home/eric.coughlin/opt_pycoh/lib/python2.6/site-packages:${PYTHONPATH}
else
  setenv PYTHONPATH =/home/eric.coughlin/opt_pycoh/lib64/python2.6/site-packages:=/home/eric.coughlin/opt_pycoh/lib/python2.6/site-packages
endif
if ( $?LD_LIBRARY_PATH ) then
  setenv LD_LIBRARY_PATH =/home/eric.coughlin/opt_pycoh/lib64/python2.6/site-packages:${LD_LIBRARY_PATH}
else
  setenv LD_LIBRARY_PATH =/home/eric.coughlin/opt_pycoh/lib64/python2.6/site-packages
endif
if ( $?DYLD_LIBRARY_PATH ) then
  setenv DYLD_LIBRARY_PATH =/home/eric.coughlin/opt_pycoh/lib64/python2.6/site-packages:${DYLD_LIBRARY_PATH}
else
  setenv DYLD_LIBRARY_PATH =/home/eric.coughlin/opt_pycoh/lib64/python2.6/site-packages
endif
setenv _CONDOR_DAGMAN_LOG_ON_NFS_IS_ERROR FALSE
