import pandas as pd
from sqlalchemy import create_engine

def data_extraction_csv(url):
    print("### Data Extraction Started ###")
    try:
        df = pd.read_csv(url, delimiter=';', on_bad_lines='skip')
        print("### Data Extraction Finished ###")
        return df
    except Exception as e:
        print("### Error occurred during data extraction ###", str(e))
        return None

def data_transformation(df):
    print("Data Transformation Started")
    try:
        #First, drop the "Status" column
        transformed_df = df.drop("Status", axis=1)

        #Then, drop all rows with invalid values: 
        #Valid "Verkehr" values are "FV", "RV", "nur DPN"
        transformed_df['Laenge'] = transformed_df['Laenge'].str.replace(',', '.').astype(float)
        transformed_df['Breite'] = transformed_df['Breite'].str.replace(',', '.').astype(float)
        valid_verkehr_values = ['FV', 'RV', 'nur DPN']
        transformed_df = transformed_df[transformed_df['Verkehr'].isin(valid_verkehr_values)]

        #Valid "Laenge", "Breite" values are geographic coordinate system values between -90 and 90
        transformed_df = transformed_df[(transformed_df['Laenge'] >= -90) & (transformed_df['Laenge'] <= 90)]
        transformed_df = transformed_df[(transformed_df['Breite'] >= -90) & (transformed_df['Breite'] <= 90)]

        #Valid "IFOPT" values follow this pattern:
        transformed_df= transformed_df[transformed_df['IFOPT'].str.match(r'^[a-zA-Z]{2}:\d+:?\d*:?(\d+)?$', na=False)]
        
        #Empty cells are considered invalid
        transformed_df= transformed_df.dropna()
        dtype = {
            "EVA_NR": int,
            "DS100": str,
            "IFOPT": str,
            "NAME": str,
            "Verkehr": str,
            "Laenge": float,
            "Breite": float,
            "Betreiber_Name": str,
            "Betreiber_Nr": int
        }
        transformed_df = transformed_df.astype(dtype)
        transformed_df= transformed_df.reset_index(drop=True)
        print("### Data Transformation Finished ###")
        return transformed_df
    except Exception as e:
        print("Error occurred during data transformation ", str(e))
        return None


def data_into_database(transformed_df, table_name):
    print("### SQLite loading data into database Started ###")
    engine = create_engine("sqlite:///trainstops.sqlite")
    with engine.begin() as connection:
        transformed_df.to_sql(table_name, connection, if_exists="replace", index=False)
    print("### Data Loading Finished ###")

    

# Replace "https://example.com/path/to/file.csv" with the actual URL of your CSV file
csv_url = "https://download-data.deutschebahn.com/static/datasets/haltestellen/D_Bahnhof_2020_alle.CSV"

df = data_extraction_csv(csv_url)

if df is not None:
    # Perform data transformation by dropping the "Status" column
    transformed_df = data_transformation(df)

    if transformed_df is not None:
        # Call data_loader function to load transformed data into the database
        data_into_database(transformed_df, "trainstops")
