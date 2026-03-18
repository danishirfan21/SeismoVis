import requests
import os

def download_data():
    url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.csv"
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")
    dest_path = os.path.join(data_dir, "earthquakes.csv")

    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    print(f"Downloading latest earthquake data from USGS...")
    response = requests.get(url)
    
    if response.status_code == 200:
        with open(dest_path, "wb") as f:
            f.write(response.content)
        print(f"Successfully saved data to {dest_path}")
    else:
        print(f"Failed to download data. Status code: {response.status_code}")

if __name__ == "__main__":
    download_data()
