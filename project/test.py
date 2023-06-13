import pandas as pd
from sqlalchemy import create_engine, inspect
from data.pipline import Extract_Data

def test_data_extract(path):
    df = Extract_Data(path)
    assert not df.empty, "Data Extraction Failed"
    print("test_data_extract: Test Passed")
    return df


def test_load_data(table_name, db_file):
    engine = create_engine(f"sqlite:///{db_file}")

    # Create an inspector object
    inspector = inspect(engine)

    # Check if a table exists in the database
    exists = inspector.has_table(table_name)
    assert exists, f"The table '{table_name}' does not exist in the database."
    print("test_load_data: Table exists, Test Passed")

def test_pipeline():
    parking_violation_url = 'https://docs.google.com/spreadsheets/d/1nqo4LbJBF1dzHT5P4iel2Mr3Z7bqUcBE/export?format=xlsx'
    test_data_extract(parking_violation_url)
    street_directory_url = 'https://docs.google.com/spreadsheets/d/1r1trwsD2uwpC5U_xxO5iNzNl_Re_vE_g/export?format=xlsx'
    test_data_extract(street_directory_url)
    db_file = 'traffic_violation.sqlite'
    test_load_data('parking_violations', db_file)
    test_load_data('Street_directory', db_file)

if __name__ == "__main__":
    test_pipeline()
