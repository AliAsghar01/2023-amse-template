import pandas as pd
import sqlite3

# Read the first XLS file with 6 columns using pandas
data1 = pd.read_excel('/Users/aliasghar/Documents/ASME/2023-amse-template/project/datasets/parking_violations_Bonn.xls')

# Read the second XLS file with 5 columns using pandas
data2 = pd.read_excel('/Users/aliasghar/Documents/ASME/2023-amse-template/project/datasets/Street_directory.xls')

# Read only the desired two columns from the first XLS file
data2_selected = data2[['strasse', 'strassen_bez']] # Replace 'Column1' and 'Column2' with the actual column names


# Connect to the SQLite database
conn = sqlite3.connect('database.db')

# Store the data from the first XLS file in a table called 'table1'
data1.to_sql('table1', conn, if_exists='replace', index=False)

# Store the data from the second XLS file in a table called 'table2'
data2_selected.to_sql('table2', conn, if_exists='replace', index=False)

# Close the database connections
conn.close()

# Display the contents of the tables
conn = sqlite3.connect('database.db')

# Fetch and print the data from 'table1'
cursor = conn.execute('SELECT * FROM table1')
table1_data = cursor.fetchall()
print("Table 1:")
for row in table1_data:
    print(row)

# Fetch and print the data from 'table2'
cursor = conn.execute('SELECT * FROM table2')
table2_data = cursor.fetchall()
print("\nTable 2:")
for row in table2_data:
    print(row)

# Close the database connection
conn.close()
