# This script is used to plot the data in different ways.

# Authors:
# Christopher Mahn
# Silas Teske
# Joshua Wolf
# Maria Riegel

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
            entry = float(entry.strip())
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


def terminate():
    """
    This function terminates the program.
    """
    print("[INFO] The program has been terminated.")
    exit()


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
            timeserieses.append(np.array(sensor_stream))
    
    if(len(timeserieses) == 23):
        print("[INFO] The data has been imported successfully.")
    else:
        print("[ERROR] The data has not been imported successfully.")
        terminate()
    
    aramis_belasten_entlasten_1 = {'zeit':timeserieses[0], 'kraft':timeserieses[1], 'dms_hinten':timeserieses[2], 'dms_vorn':timeserieses[3]}
    aramis_belasten_entlasten_2 = {'index':timeserieses[4], 'dehnung':timeserieses[5], 'kraft':timeserieses[6]}
    belastung_entlastung_7000n = {'zeit':timeserieses[7], 'kraft':timeserieses[8], 'dms_hinten':timeserieses[9], 'dms_vorn':timeserieses[10]}
    kabelkompensation_aus_magnet_heissluft = {'zeit':timeserieses[11], 'kraft':timeserieses[12], 'dms_hinten':timeserieses[13], 'dms_vorn':timeserieses[14]}
    netzkabel_neben_messleitung = {'zeit':timeserieses[15], 'kraft':timeserieses[16], 'dms_hinten':timeserieses[17], 'dms_vorn':timeserieses[18]}
    schwingung = {'zeit':timeserieses[19], 'kraft':timeserieses[20], 'dms_hinten':timeserieses[21], 'dms_vorn':timeserieses[22]}

    # Plot the data
    analysis.plot_xy([[1000*aramis_belasten_entlasten_1['kraft'], aramis_belasten_entlasten_1['dms_hinten']/1000],
                      [1000*aramis_belasten_entlasten_1['kraft'], aramis_belasten_entlasten_1['dms_vorn']/1000]],
                     ["Aramis Belasten Entlasten 1 (hinten)",
                      "Aramis Belasten Entlasten 1 (vorn)"],
                     "Kraft [N]", "Dehnung [mm]", "Aramis Belasten Entlasten 1")
    analysis.plot_xy([[1000*aramis_belasten_entlasten_1['kraft'], (aramis_belasten_entlasten_1['dms_hinten']-aramis_belasten_entlasten_1['dms_vorn'])/1000]],
                     ["Aramis Belasten Entlasten 1 (hinten-vorn)"],
                     "Kraft [N]", "Dehnung [mm]", "Aramis Belasten Entlasten 1")
    analysis.plot_xy([[1000*aramis_belasten_entlasten_2['kraft'], aramis_belasten_entlasten_2['dehnung']*100]],
                     ["Aramis Belasten Entlasten 2"],
                     "Kraft [N]", "Dehnung [%]", "Aramis Belasten Entlasten 2")
    analysis.plot_xy([[1000*belastung_entlastung_7000n['kraft'], belastung_entlastung_7000n['dms_hinten']/1000],
                      [1000*belastung_entlastung_7000n['kraft'], belastung_entlastung_7000n['dms_vorn']/1000]],
                     ["Belastung Entlastung 7000N (hinten)",
                      "Belastung Entlastung 7000N (vorn)"],
                     "Kraft [N]", "Dehnung [mm]", "Belastung Entlastung 7000N")
    analysis.plot_xy([[1000*belastung_entlastung_7000n['kraft'], (belastung_entlastung_7000n['dms_hinten']-belastung_entlastung_7000n['dms_vorn'])/1000]],
                     ["Belastung Entlastung 7000N (hinten-vorn)"],
                     "Kraft [N]", "Dehnung [mm]", "Belastung Entlastung 7000N")

