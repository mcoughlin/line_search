cd ~/pycoh
source install_pycoh.sh

cd ~
source ~/pycoh_runs/setup_paths.sh

python ~/gitrepo/line_search/daily_run --ifo H1

python ~/gitrepo/line_search/daily_run_1 --ifo H1

python ~/gitrepo/line_search/daily_run_10 --ifo H1

python ~/gitrepo/line_search/daily_run_100 --ifo H1
