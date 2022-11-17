# This script is used to plot the data in different ways.

# Import of libraries
import os
import main as settings
import lib_analysis as analysis
import matplotlib.pyplot as plt
import numpy as np

# -----------------------------------------------------------------------------

# Functions

def import_csv(filename):
    """
    This function imports the csv-files and returns them as sensor-streams".
    """
    with open(os.path.join("data_converted", filename), "r") as file:
        data = file.readlines()
    converted_data = []
    num_of_entries = 0
    sensor_streams = []
    for line in data:
        line = line.split(";")
        converted_line = []
        for entry in line:
            entry = entry.strip()
            converted_line.append(entry)
        converted_data.append(converted_line)
        if(len(converted_line) > num_of_entries):
            num_of_entries = len(converted_line)
        del converted_line
    for i in range(num_of_entries):
        sensor_streams.append([])
    for line in converted_data:
        for i, entry in enumerate(line):
            sensor_streams[i].append(entry)
    return(sensor_streams)


# -----------------------------------------------------------------------------

# Classes

# -----------------------------------------------------------------------------

# Beginning of main program

if(__name__=='__main__'):
    # Import the data
    timeserieses = []
    for dataset in settings.datasets_converted:
        sensor_streams = (import_csv(dataset))
        for sensor_stream in sensor_streams:
            timeserieses.append(sensor_stream)
    
    # Plot the data
    for timeseries in timeserieses:
        analysis.plot_werte([timeseries])