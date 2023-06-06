import pandas as pd
from sqlalchemy import create_engine

def data_extraction_csv(url):
    print("Data Extraction in progress...")
    try:
        df = pd.read_csv(url, delimiter=';', on_bad_lines='skip')
        print("Finish: Data Extraction")
        return df
    except Exception as e:
        print("Error occurred during file reading:", str(e))
        return None

def data_transformation(df):
    print("Data Transformation in progress...")
    try:
        transformed_df = df.drop("Status", axis=1)
        transformed_df['Laenge'] = transformed_df['Laenge'].str.replace(',', '.').astype(float)
        transformed_df['Breite'] = transformed_df['Breite'].str.replace(',', '.').astype(float)
        valid_verkehr_values = ['FV', 'RV', 'nur DPN']
        transformed_df = transformed_df[transformed_df['Verkehr'].isin(valid_verkehr_values)]
        transformed_df = transformed_df[(transformed_df['Laenge'] >= -90) & (transformed_df['Laenge'] <= 90)]
        transformed_df = transformed_df[(transformed_df['Breite'] >= -90) & (transformed_df['Breite'] <= 90)]
        transformed_df= transformed_df[transformed_df['IFOPT'].str.match(r'^[a-zA-Z]{2}:\d+:?\d*:?(\d+)?$', na=False)]
        transformed_df= transformed_df.dropna()
        transformed_df= transformed_df.reset_index(drop=True)
        print("Finish: Data Transformation")
        return transformed_df
    except Exception as e:
        print("Error occurred during data transformation:", str(e))
        return None


def data_loader(data_frame, table_name):
    print("SQLite DB Operations....")
    engine = create_engine("sqlite:///../trainstops.db")
    with engine.begin() as connection:
        data_frame.to_sql(table_name, connection, if_exists="replace", index=False)
    print("Finish: Data Loading")

# Replace "https://example.com/path/to/file.csv" with the actual URL of your CSV file
csv_url = "https://download-data.deutschebahn.com/static/datasets/haltestellen/D_Bahnhof_2020_alle.CSV"

df = data_extraction_csv(csv_url)

if df is not None:
    # Perform data transformation by dropping the "Status" column
    transformed_df = data_transformation(df)

    if transformed_df is not None:
        # Call data_loader function to load transformed data into the database
        data_loader(transformed_df, "table_name")
