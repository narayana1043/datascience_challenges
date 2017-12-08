#!/usr/bin/env bash

# run the commands in ./setup_file/install_and_configure_git.sh

sudo yum install screen
sudo pip-3.4 install jupyter
jupyter notebook --generate-config
echo "c.NotebookApp.port = 8889" >> /home/hadoop/.jupyter/jupyter_notebook_config.py
echo "c.NotebookApp.open_browser = False" >> /home/hadoop/.jupyter/jupyter_notebook_config.py

./setup_files/start_jupyter_screen.sh

# change the cluster-id
aws emr add-steps --cluster-id j-2VZU4P5595EGK --steps file://./setup_files/s32hdfs.json


