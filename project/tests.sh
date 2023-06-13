#!/bin/bash

echo "pipeline file executed"
# Execute your pipeline
python data/pipline.py

python -m data.pipline -v
# Validate the output file(s)
if [ -f "traffic_violation.sqlite" ]; then
  echo "database file exists."
else
  echo "database file not found."
fi

echo "test file executed"
python -m test -v
