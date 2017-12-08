#!/usr/bin/env bash

aws emr add-steps --cluster-id j-2HFJJ4JQQ5OVG --steps file://./s32hdfs.json
