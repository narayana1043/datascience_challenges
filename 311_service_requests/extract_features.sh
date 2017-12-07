#!/usr/bin/env bash

head -n 1 ./data/311_service_requests.csv | sed 's/,/\n/g' > ./data/features.txt