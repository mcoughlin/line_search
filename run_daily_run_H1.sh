#cd ~/pycoh
#source install_pycoh.sh

source ~/.bashrc

cd ~/gitrepo/line_search

kinit coherencetool_lho/robot/ldas-pcdev2.ligo-wa.caltech.edu@LIGO.ORG -k -t certs/coherencetool.lho
ligo-proxy-init -k

source ~/pycoh/etc/pycoh-user-env.sh

python ~/gitrepo/line_search/daily_run_32 --ifo H1

