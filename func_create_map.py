import folium
import pandas as pd

def create_map(csv_file_path):
    # Load the data from the CSV file
    data = pd.read_csv(csv_file_path, header=None)

    # Extract latitude, longitude, and detector lanes from the data
    latitude = data.iloc[:, 5].astype(str).apply(lambda x: float(x[:2] + '.' + x[2:]))
    longitude = data.iloc[:, 6].astype(str).apply(lambda x: float(x[:4] + '.' + x[4:]))
    detector_lanes = data.iloc[:, 1]

    # Create a map centered at the mean latitude and longitude, with zoom level 10
    map = folium.Map(location=[latitude.mean(), longitude.mean()], zoom_start=10)

    # Group the data by unique latitude and longitude, and create a list of detector lanes for each group
    unique_locations = data.groupby([latitude, longitude])[1].apply(list)

    # Add a blue circle for each unique location, with a tooltip showing the latitude, longitude, and list of detector lanes
    for loc, lanes in unique_locations.iteritems():
        lat, lon = loc
        lanes_str = ', '.join(sorted(set(lanes)))
        tooltip_text = f"Latitude: {lat}, Longitude: {lon}, Detector Lanes: {lanes_str}"
        folium.Circle(location=[lat, lon], radius=20, color='blue', fill=True, fill_color='blue',
                      tooltip=tooltip_text, sticky=True).add_to(map)

    return map
