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
    parking_violation_file = '/Users/aliasghar/Documents/ASME/2023-amse-template/project/datasets/parking_violations_Bonn.xls'
    test_data_extract(parking_violation_file)
    street_directory_file = '/Users/aliasghar/Documents/ASME/2023-amse-template/project/datasets/Street_directory.xls'
    test_data_extract(street_directory_file)
    db_file = 'traffic_violation.sqlite'
    test_load_data('parking_violations', db_file)
    test_load_data('Street_directory', db_file)

if __name__ == "__main__":
    test_pipeline()
