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
git clone https://git.ligo.org/michael-coughlin/pycoh
mkdir opt_pycoh
python setup.py install –prefix=/home/albert.einstein/opt_pycoh

cd ~
mkdir gitrepo
cd gitrepo
git clone https://github.com/mcoughlin/line_search.git


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

Running Pycoh

source ~/pycoh_runs/setup_paths.sh

Now it should be as simple as:
python daily_run_1 -i H (or L)

