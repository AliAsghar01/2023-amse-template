#testing project workflow run
#!/bin/bash
echo "pipeline fle executed"
# Execute your pipeline

# Install the requirements
pip install -r project/data/pipeline.py

# Validate the output file(s)
if [ -f "traffic_violation.sqlite" ]; then
  echo "database file exist."
else
  echo "database file not found."
fi

# Run the pytest script
echo " test file excuted"
python -m project/test.py -v




