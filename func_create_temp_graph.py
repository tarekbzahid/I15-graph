# This is a working code for creating a temporal grpah based on the distance based graph 
# The scaling is done by defining peak, off peak and normal hours of the day 

import pandas as pd
from geopy.distance import distance
import numpy as np
from scipy.spatial import distance_matrix
from heapq import nsmallest
import datetime

def create_graph(data):
    # Set the number of closest node each node will be connected to:
    num_connections = 9

    # The nodes which will be ignored during graph making. Each nodes are represented as (Lat1, Long1)
    ignore_list = [(36.068619, -115.211891),(35.759998,-115.760002),(35.650002,-115.650002), (41.2345, -112.6789), (42.3456, -113.7890)]

    #data = data.dropna(subset=['latitude', 'longitude'])  # Drop rows with missing values in lat/long
    latitude = data.iloc[:, 5].astype(str).apply(lambda x: float(x[:2] + '.' + x[2:]))
    longitude = data.iloc[:, 6].astype(str).apply(lambda x: float(x[:4] + '.' + x[4:]))
    ids = data.iloc[:, 1]

    locations, index = np.unique(np.column_stack((latitude, longitude)), axis=0, return_index=True)
    ids = ids[index]

    # Check if each location is in the ignore list and remove it if it is
    mask = [tuple(loc) not in ignore_list for loc in locations]
    locations = locations[mask]
    ids = ids[mask]

    # Calculate the distance matrix between all remaining locations
    dist_matrix = distance_matrix(locations, locations)

    graph = {}

    for i in range(len(locations)):
        graph[i] = []

    # Set the weight factor depending on the current time
    current_time = datetime.datetime.now().time()
    if current_time >= datetime.time(7, 0,0,0) and current_time <= datetime.time(9, 0,0,0):
        weight_factor = 1.5
        time_status = "Peak hours"
    elif current_time >= datetime.time(16, 0,0,0) and current_time <= datetime.time(18, 0,0,0):
        weight_factor = 1.5
        time_status = "Peak hours"
    elif current_time >= datetime.time(23, 0,0,0) or current_time <= datetime.time(6, 59,0,0):
        weight_factor = 0.5
        time_status = "Off-peak hours"
    else:
        weight_factor = 1
        time_status = "Normal hours"

    # Connect each node to the closest num_connections nodes
    for i in range(len(locations)):
        closest = nsmallest(num_connections+1, range(len(dist_matrix[i])), key=lambda x: dist_matrix[i][x])
        closest.remove(i)
        for j in closest:
            distance_km = float(distance(locations[i], locations[j]).kilometers)* weight_factor
            graph[i].append((j, distance_km))

    
    return graph



