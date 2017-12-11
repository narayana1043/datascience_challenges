#!/usr/bin/env bash

# run this file before anything

sudo yum install git
git config --global user.name "Veera Marni"
git config --global user.email narayana1043@gmail.com
git clone https://github.com/narayana1043/datascience_challenges.git
cd datascience_challenges

# run the commands in ./setup_file/install_and_configure_git.sh

sudo yum install screen
sudo pip-3.4 install jupyter
sudo pip-3.4 install pandas

# configure jupyter
jupyter notebook --generate-config
echo "c.NotebookApp.port = 8889" >> /home/hadoop/.jupyter/jupyter_notebook_config.py
echo "c.NotebookApp.open_browser = False" >> /home/hadoop/.jupyter/jupyter_notebook_config.py
