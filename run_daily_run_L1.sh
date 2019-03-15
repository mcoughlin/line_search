#cd ~/pycoh
#source install_pycoh.sh


cd ~/gitrepo/line_search

kinit coherencetool_llo/robot/ldas-pcdev2.ligo-la.caltech.edu@LIGO.ORG -k -t certs/coherencetool.llo
ligo-proxy-init -k

source ~/pycoh/etc/pycoh-user-env.sh

python ~/gitrepo/line_search/daily_run_32 --ifo L1

