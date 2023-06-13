#testing project workflows
#!/bin/bash

echo "pipeline fle executed"
# Execute your pipeline
python -m project/data/pipline -v

# Validate the output file(s)
if [ -f "traffic_violation.sqlite" ]; then
  echo "database file exist."
else
  echo "database file not found."
fi

echo " test file excuted"
python -m project/test -v

