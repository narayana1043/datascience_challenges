#!/usr/bin/env bash

export SPARK_HOME=/usr/lib/spark/
export PYSPARK_PYTHON=/usr/bin/python3.4
export PYSPARK_DRIVER_PYTHON="jupyter"
export PYSPARK_DRIVER_PYTHON_OPTS="notebook"
pyspark --master yarn &> ~/jupyter_log.txt 2>&1
