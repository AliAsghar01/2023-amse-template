import sqlite3
from geopy.geocoders import Nominatim

# Connect to the database
conn = sqlite3.connect('traffic_violation.sqlite')
cursor = conn.cursor()

# Add columns to the street_directory table if they don't exist
cursor.execute("ALTER TABLE street_directory ADD COLUMN latitude REAL")
cursor.execute("ALTER TABLE street_directory ADD COLUMN longitude REAL")

# Query the database and retrieve the results
query = "SELECT Street_Number, Street_Name FROM street_directory"
cursor.execute(query)
results = cursor.fetchall()

# Create a geolocator instance
geolocator = Nominatim(user_agent="my_app")

# Iterate through the results
for row in results:
    zip_code = row[0]
    street_name = row[1]

    # Construct the address string
    address = f"{zip_code} {street_name},Bonn, Germany"

    # Geocode the address to obtain latitude and longitude
    location = geolocator.geocode(address)

    if location:
        latitude = location.latitude
        longitude = location.longitude
        print(address, "::", latitude, longitude)

        # Update the database with latitude and longitude values
        update_query = "UPDATE street_directory SET latitude = ?, longitude = ? WHERE Street_Number = ? AND Street_Name = ?"
        cursor.execute(update_query, (latitude, longitude, zip_code, street_name))
    else:
        latitude = None
        longitude = None

# Commit the changes to the database
conn.commit()

# Close the database connection
conn.close()
