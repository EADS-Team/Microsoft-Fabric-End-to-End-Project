Fabric End to end Project - Bronze Notebook

***
import requests
import json
from datetime import date, timedelta

***
# Remove this before running Data Factory Pipeline
start_date = date.today() - timedelta(7) # 7 days
end_date = date.today() - timedelta(1)

***
# Construct the API URL with start and end dates provided by Data Factory, formatted for geojson output.
url = f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={start_date}&endtime={end_date}"

***
try:
    # Make the GET request to fetch data
    response = requests.get(url)

    # Check if the request was successful
    response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
    data = response.json().get('features', [])

    if not data:
        print("No data returned for the specified date range.")
    else:
        # Specify the file name (and path if needed)
        file_path = f'/lakehouse/default/Files/{start_date}_earthquake_data.json'

        # Save the JSON data
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"Data successfully saved to {file_path}")
except requests.exceptions.RequestException as e:
    print(f"Error fetching data from API: {e}")
