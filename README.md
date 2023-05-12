## About
This repository contains code for creating a static graph and a temporal graph for a set of 800+ sensors detecting 2000+ lanes on three traffic parameters, speed, flow and occupancy, located along the I-15 highway in Nevada. The static graph is generated using a weighted adjacency list based on the distance between the sensors. The temporal graph, is created based on the traffic policies defined. 

### file description:
plotter: plots the positions of the sensors in an interactive Google map like style
static_graph: creates the static graph
temporal_grpah: creates the temporal graph
calc_adjacency_26x: the code for creating 26 sensor adjjacency list
raw_weight_adjacency_list: adjacency list for the static I15 sensor

### directory:
detector: sensor data stored as csv
viz: stores the visualizations 