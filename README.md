# line_search
Line Search for gravitational-wave analysis





Pycoh Installation and User's Guide

Nathaniel Strauss




Some General Comments

For the purpose of these instructions, your name is Albert Einstein and your username is albert.einstein.
You should be able to copy and paste the commands I have written below, with the above exception. Probably only execute one “paragraph” of commands at a time.
Contact me at straussn@carleton.edu if you have trouble.

Connecting to the Clusters

In order to connect to the clusters, you need to use 'ligo-proxy-init albert.einstein' and 'gsissh (cluster name)', which you can install here: https://wiki.ligo.org/viewauth/LDG/GettingStarted

Installing Pycoh

Downloading the Source Code

git config --global user.name "Albert Einstein"
git config --global user.email albert.einstein@ligo.org
export GIT_SSH=gsissh
git clone git+ssh://albert.einstein@ligo-vcs.phys.uwm.edu/usr/local/git/pycoh.git
mkdir opt_pycoh
python setup.py install –prefix=/home/albert.einstein/opt_pycoh

cd ~
mkdir gitrepo
cd gitrepo
git clone git@lisa.physics.carleton.edu:/mnt/gitrepo/line_search/ #get the password from Nelson

repository has been moved to github: git clone https://github.com/mcoughlin/line_search.git


cd ~
LSCSOFT_SRCDIR=/usr1/${USER}/src/lscsoft/

mkdir -p ${LSCSOFT_SRCDIR}

cd ${LSCSOFT_SRCDIR}
git clone albert.einstein@ligo-vcs.phys.uwm.edu:/usr/local/git/lalsuite.git

LSCSOFT_SRCDIR=${LSCSOFT_SRCDIR:-"${HOME}/src/lscsoft/"} 
LSCSOFT_ROOTDIR=${LSCSOFT_ROOTDIR:-"${HOME}/master"} 
LAL_PREFIX=${LAL_PREFIX:-"${LSCSOFT_ROOTDIR}/opt/lscsoft/lal"}

cd ${LSCSOFT_SRCDIR}/lalsuite/lal
./00boot
./configure --prefix=${LAL_PREFIX}
make
make install

mkdir -p ${LSCSOFT_ROOTDIR}/etc
echo "export LSCSOFT_LOCATION=${LSCSOFT_ROOTDIR}/opt/lscsoft" > ${LSCSOFT_ROOTDIR}/etc/lscsoftrc
echo "# setup LAL for development:  " >> ${LSCSOFT_ROOTDIR}/etc/lscsoftrc
echo "export LAL_LOCATION=\$LSCSOFT_LOCATION/lal" >> ${LSCSOFT_ROOTDIR}/etc/lscsoftrc
echo "if [ -f "\$LAL_LOCATION/etc/lal-user-env.sh" ]; then" >> ${LSCSOFT_ROOTDIR}/etc/lscsoftrc
echo "  source \$LAL_LOCATION/etc/lal-user-env.sh" >> ${LSCSOFT_ROOTDIR}/etc/lscsoftrc
echo "fi" >> ${LSCSOFT_ROOTDIR}/etc/lscsoftrc

PYLAL_PREFIX=${LSCSOFT_ROOTDIR}/opt/lscsoft/pylal
cd ${LSCSOFT_SRCDIR}/lalsuite/pylal

python setup.py install –prefix=${PYLAL_PREFIX}

echo "# setup PyLAL for development:  " >> ${LSCSOFT_ROOTDIR}/etc/lscsoftrc
echo "export PYLAL_LOCATION=\$LSCSOFT_LOCATION/pylal" >> ${LSCSOFT_ROOTDIR}/etc/lscsoftrc
echo "if [ -f "\$PYLAL_LOCATION/etc/pylal-user-env.sh" ]; then" >> ${LSCSOFT_ROOTDIR}/etc/lscsoftrc
echo "  source \$PYLAL_LOCATION/etc/pylal-user-env.sh" >> ${LSCSOFT_ROOTDIR}/etc/lscsoftrc
echo "fi" >> ${LSCSOFT_ROOTDIR}/etc/lscsoftrc

source ${LSCSOFT_ROOTDIR}/etc/lscsoftrc

GLUE_PREFIX=${LSCSOFT_ROOTDIR}/opt/lscsoft/glue # change as appropriate
cd ${LSCSOFT_SRCDIR}/lalsuite/glue
python setup.py install --prefix=${GLUE_PREFIX}

echo "# setup GLUE for development:  " >> ${LSCSOFT_ROOTDIR}/etc/lscsoftrc
echo "export GLUE_LOCATION=\$LSCSOFT_LOCATION/glue" >> ${LSCSOFT_ROOTDIR}/etc/lscsoftrc
echo "if [ -f "\$GLUE_LOCATION/etc/glue-user-env.sh" ]; then" >> ${LSCSOFT_ROOTDIR}/etc/lscsoftrc
echo "  source \$GLUE_LOCATION/etc/glue-user-env.sh" >> ${LSCSOFT_ROOTDIR}/etc/lscsoftrc
echo "fi" >> ${LSCSOFT_ROOTDIR}/etc/lscsoftrc

source ${LSCSOFT_ROOTDIR}/etc/lscsoftrc

I had a bear of a time getting this to work my first time through, but hopefully I've saved you the trouble. Let me know if you encounter issues, and I'll do my best to help.

Setting Up Directory Structure

Now that you have the code, you need to let bash know where it is. You need to add stuff to the hidden file in your home directory .bash_profile so that you have a section that looks like this:

fi

# User specific environment and startup programs

PATH=$PATH:$HOME/bin

source /home/albert.einstein/master/opt/lscsoft/lal/etc/lal-user-env.sh
source /home/albert.einstein/master/opt/lscsoft/pylal/etc/pylal-user-env.sh
source /home/albert.einstein/master/opt/lscsoft/glue/etc/glue-user-env.sh
source /home/albert.einstein/master/etc/lscsoftrc

export PATH 

Now you'll need a couple ini files. From here on out, you can decide where to put your files yourself, as long as you have the program pointing to the correct files in the correct places, but in the code here I'm gonna just assume you want the same directory structure I have.

cd ~
mkdir -p LineSearch/day_run/
cd LineSearch/day_run/
cp /home/nathaniel.strauss/LineSearch/day_run/H1_pycoh_10.ini .

I also keep some channel lists in that directory. At this point you should edit the H1_pycoh_10.ini file so that it points to the files you downloaded above. This means in the [condor] section, you should put your username in place of mine. 

Now you should create the directory from which you'll run pycoh, and the rest of your files will go there.

cd ~
mkdir pycoh_runs
cd pycoh_runs
cp /home/nathaniel.strauss/pycoh_runs_test/HIFOX_10.ini .

I also usually keep the channel list and segment list for my runs in that directory. In the [general] section, you name your run (You'll probably want something that includes the date and length of the lock). You'll also need to edit the [condor] section of this ini file so that it points to your version of the code instead of mine. In the [input] section, you need to make sure it's pointing to the correct interferometer (L1 or H1), your version of the H1_pycoh_10.ini file instead of mine, and your channel and segment text files, wherever you decide to put them.

Running Pycoh

Now you finally get to run on some data! First you need to make sure your ini files have the correct settings.

HIFOX_10.ini

In the [general] section, you should tag your run with something that specifies the interferometer, date, and duration of the lock you're running on.

In [input], put in the correct interferometer under ifo (H1 or L1). The pycoh_ini should be the path to your other ini file, H1_pycoh_10.ini. The analyzed_seg_files should be the path to your segment text file.
The channel_list_file should be the path to your segment list file. I usually keep my segment and channel list files in the same directory where I run the code (pycoh_runs).

H1_pycoh_10.ini

Once again, BEWARE: Some of the specifications in this ini file are overwritten in ~/gitrepo/line_search/line_setup, so you'll have to edit the hard code in order to change some of these settings. Notice how I tested this by putting gibberish as the frametypes in the [channels] section.

Basically the only thing you can edit in here is is under [output]. The inverse-freq-resolution should be set to powers of 2. 16 for 10 mHz resolution, 128 for 100 mHz resolution, and 1024 for 1 mHz resolution. The name of this file has the 10 because it's set with an inverse frequency of about 10.

In both of these ini files, I'd recommend making a few versions of them with different settings and saving them under appropriate names.

/home/albert.einstein/gitrepo/line_search/line_setup

Here's where you have to edit hard-coded settings. At about line 239, you should see the write_pycoh_ini function, which re-writes H1_pycoh_10.ini. You want chanlist1 to be the main channel you're analyzing. Your frametypes should be either %s_C or %s_R, but probably %s_R. That just has to do with whether the program looks for data in temporary or archived locations.

Creating and Submitting a Condor DAG

To create the DAG you run run line_setup. Make sure you only do this inside of pycoh_runs or a similar directory, or you'll get a ton of junk files where you don't want them.

Remember to target the pycoh module before running the ini file.

source ~/pycoh_runs/setup_paths.sh

Running the ini file for condor submission

cd ~/pycoh_runs
~/gitrepo/line_search/line_setup –ini_file ./HIFOX_10.ini –verbose

Once the output says that the jobs are ready for submitting to Condor move on, if error: check for any mistakes in previous lines.

Submitting jobs to Condor
condor_submit_dag -maxjobs 750 ./dags/(enter the tag of your run here).dag
Then you can monitor the DAG's progress in real time:
tail -f dags/(enter the tag of your run here).dag.dagman.out
Then you're all set!
Dealing with Errors

The first time you run line_search you are guaranteed to get errors. Take a look at the traceback and examine the corresponding programs in my directory to see how I dealt with the bug. You'll find the diff command useful for this. You may also want to simply copy some of my versions of the programs over to your directory structure directly, but be careful with that and change what you need to. Always create a back-up file before you mess with stuff. You also might want to add more specific instructions for fixing those bugs to this guide as you fix them.

When you actually submit the DAG to the cluster, it will still crash at first (EXITING WITH STATUS 1). You need to do a bunch of ls -ltr commands inside your pycoh_runs directory in order to track down the most recent error log. Then look at the traceback and use the same method as in debugging line_search. Once again, you may want to document the changes you have to make in this guide.

It took me several months to debug this code the first time, so don't feel bad, and let me know if you have questions.

Some Final Suggestions

Once you get everything up and running, you may want to automate much of this process. I've written some programs that search data for significant lines, compare different data runs, and run on a segment list on several different frequency resolutions. If you want to take a look, they're in /home/nathaniel.strauss/scripts/ at Livingston and /home/nathaniel.strauss/bin/ at Hanford. They're terribly documented, but it may give you some ideas.
