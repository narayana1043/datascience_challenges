#!/usr/bin/env bash

curl "https://nycopendata.socrata.com/api/views/erm2-nwe9/rows.csv?accessType=DOWNLOAD" \
> ./data/311_service_requests.csv
