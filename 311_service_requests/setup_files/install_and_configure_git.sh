#!/usr/bin/env bash

# run this file before anything

sudo yum install git
git config --global user.name "Veera Marni"
git config --global user.email narayana1043@gmail.com
git clone https://github.com/narayana1043/datascience_challenges.git
cd datascience_challenges
git remote remove origin
git remote add origin git@github.com:narayana1043/datascience_challenges.git

# follow instructions in get_data.sh if data is not is s3