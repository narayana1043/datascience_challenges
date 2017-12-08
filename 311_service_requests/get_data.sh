#!/usr/bin/env bash

mkdir ./data

curl "https://nycopendata.socrata.com/api/views/erm2-nwe9/rows.csv?accessType=DOWNLOAD" \
> ./data/311_service_requests.csv

curl "https://data.cityofnewyork.us/Health/DOHMH-New-York-City-Restaurant-Inspection-Results/43nn-pn8j" \
> ./data/restaurant_grades.xlsx

head -n 1 ./data/311_service_requests.csv | sed 's/,/\n/g' > ./data/features.txt

# upload the data into s3 after the download is complete
