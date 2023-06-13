import pandas as pd
import sqlite3

def Extract_Data(file_path):
    # Read the XLS file using pandass
    data = pd.read_excel(file_path)
    return data

def Transform_Data1(data, selected_columns=None):
    if selected_columns:
        # Select the desired columns
        data_selected = data[selected_columns]
        # Rename the columns
        data_selected.rename(columns={
            'TATZEIT': 'Crime_Str_No',
            'TATORT': 'Crime_location',
            'TATBESTANDBE_TBNR': 'Crime_Violation_No',
            'GELDBUSSE': 'Total_Fine',
            'BEZEICHNUNG': 'Vehicle_Description'
        }, inplace=True)
        return data_selected
    else:
        return data

def Transform_Data2(data, selected_columns=None):
    if selected_columns:
        # Select the desired columns
        data_selected = data[selected_columns]
        # Rename the columns
        data_selected.rename(columns={'strassen_bez': 'Street Name', 'strasse': 'Street Number'}, inplace=True)
        return data_selected
    else:
        return data

def load_data(data, table_name, db_file):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)

    # Store the data in the specified table
    data.to_sql(table_name, conn, if_exists='replace', index=False)

    # Close the database connection
    conn.close()

def driver():
    # Extract data from the first XLS file
    parking_violation_url = 'https://docs.google.com/spreadsheets/d/1nqo4LbJBF1dzHT5P4iel2Mr3Z7bqUcBE/export?format=xlsx'
    data1 = Extract_Data(parking_violation_url)

    # Transform data from the first XLS file by selecting desired columns
    selected_columns = ['TATZEIT', 'TATORT', 'TATBESTANDBE_TBNR', 'GELDBUSSE', 'BEZEICHNUNG']
    data1_selected = Transform_Data1(data1, selected_columns)

    # Extract data from the second XLS file
    street_directory_url = 'https://docs.google.com/spreadsheets/d/1r1trwsD2uwpC5U_xxO5iNzNl_Re_vE_g/export?format=xlsx'
    data2 = Extract_Data(street_directory_url)

    # Transform data from the second XLS file by selecting desired columns
    selected_columns = ['strasse', 'strassen_bez']
    data2_selected = Transform_Data2(data2, selected_columns)

    # Load data into the SQLite database
    db_file = 'traffic_violation.sqlite'
    load_data(data1_selected, 'parking_violations', db_file)
    load_data(data2_selected, 'Street_directory', db_file)

    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)

    # Fetch and print the data from 'parking_violations'
    cursor = conn.execute('SELECT * FROM parking_violations')
    parking_violations_data = cursor.fetchall()
    print("Table 1:")
    for row in parking_violations_data:
        print(row)

    # Fetch and print the data from 'Street_directory'
    cursor = conn.execute('SELECT * FROM Street_directory')
    Street_directory_data = cursor.fetchall()
    print("\nTable 2:")
    for row in Street_directory_data:
        print(row)

    # Close the database connection
    conn.close()

# Run the driver function
driver()
