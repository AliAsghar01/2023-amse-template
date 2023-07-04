import urllib.request
import zipfile
import pandas as pd
import sqlite3

def download_and_extract_data(url):
    # Step 1: Downloading and Unzipping the Data
    zip_filename = 'mowesta-dataset.zip'
    data_filename = 'data.csv'

    # Download the ZIP file
    urllib.request.urlretrieve(url, zip_filename)

    # Extract the ZIP file
    with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
        zip_ref.extractall()

    return data_filename

def transform_data(filename):
    # Step 2: Reshape the Data
    # Read the CSV file into a DataFrame
    df = pd.read_csv(filename, sep=";", decimal=",", index_col=False,
                     usecols=["Geraet", "Hersteller", "Model", "Monat", "Temperatur in °C (DWD)", "Batterietemperatur in °C", "Geraet aktiv"])

    # Rename columns
    df = df.rename(columns={"Temperatur in °C (DWD)": "Temperatur", "Batterietemperatur in °C": "Batterietemperatur"})

    # Discard columns to the right of "Geraet aktiv"
    columns_to_keep = ["Geraet", "Hersteller", "Model", "Monat", "Temperatur", "Batterietemperatur", "Geraet aktiv"]
    df = df[columns_to_keep]

    return df

def transform_temperatures(df):
    # Transform Temperatur column from Celsius to Fahrenheit
    df['Temperatur'] = (df['Temperatur'] * 9/5) + 32

    # Transform Batterietemperatur column from Celsius to Fahrenheit
    df['Batterietemperatur'] = (df['Batterietemperatur'] * 9/5) + 32

    return df

def validate_data(df):
    # Validate Geraet IDs
    df = df[df['Geraet'] > 0 &(df["Monat"] > 0)]

    return df

def write_to_sqlite(df, database_name, table_name):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    # Create the table
    create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            Geraet BIGINT,
            Hersteller TEXT,
            Model TEXT,
            Monat TEXT,
            Temperatur FLOAT,
            Batterietemperatur FLOAT,
            Geraet_aktiv TEXT
        )
    """
    cursor.execute(create_table_query)

    # Insert the data into the table
    df.to_sql(table_name, conn, if_exists='replace', index=False)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()



# Main
url = 'https://www.mowesta.com/data/measure/mowesta-dataset-20221107.zip'

# Step 1: Download and extract data
data_filename = download_and_extract_data(url)

# Step 2: Transform the data
transformed_data = transform_data(data_filename)

# Step 3: Transform the temperatures
transformed_temperatures = transform_temperatures(transformed_data)

# Step 4: Validate the data
validated_data = validate_data(transformed_temperatures)

# Step 5: Write the data to SQLite database
database_name = 'temperatures.sqlite'
table_name = 'temperatures'
write_to_sqlite(validated_data, database_name, table_name)

print("Data has been written to the SQLite database.")