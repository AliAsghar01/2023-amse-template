#testing project workflows
#!/bin/bash

echo "pipeline fle executed"
# Execute your pipeline
python pipline.py

# Validate the output file(s)
if [ -f "database.db" ]; then
  echo "database file exist."
else
  echo "database file not found."
fi

echo " test file excuted"
python test.py

