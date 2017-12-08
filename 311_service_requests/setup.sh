#!/usr/bin/env bash

sudo yum install git
sudo yum install screen
sudo pip-3.4 install jupyter
jupyter notebook --generate-config
echo "c.NotebookApp.port = 8889" >> /home/hadoop/.jupyter/jupyter_notebook_config.py
echo "c.NotebookApp.open_browser = False" >> /home/hadoop/.jupyter/jupyter_notebook_config.py

./setup_files/start_jupyter_screen.sh

# change the cluster-id
aws emr add-steps --cluster-id j-2HFJJ4JQQ5OVG --steps file://./setup_files/s32hdfs.json


