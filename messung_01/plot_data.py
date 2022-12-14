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

    # Plotting of data
    
    # Dehnung im Verh??ltnis zur Kraft f??r Aramis Belasten Entlasten 1
    analysis.plot_xy([[1000*aramis_belasten_entlasten_1['kraft'], aramis_belasten_entlasten_1['dms_hinten']/1000],
                      [1000*aramis_belasten_entlasten_1['kraft'], aramis_belasten_entlasten_1['dms_vorn']/1000]],
                     ["Aramis Belasten Entlasten 1 (hinten)",
                      "Aramis Belasten Entlasten 1 (vorn)"],
                     "Kraft [N]", "Dehnung [mm]", "Aramis Belasten Entlasten 1")

    # Torsion im Verh??ltnis zur Kraft f??r Aramis Belasten Entlasten 1
    analysis.plot_xy([[1000*aramis_belasten_entlasten_1['kraft'], (aramis_belasten_entlasten_1['dms_hinten']-aramis_belasten_entlasten_1['dms_vorn'])/1000]],
                     ["Aramis Belasten Entlasten 1 (hinten-vorn)"],
                     "Kraft [N]", "Dehnung [mm]", "Aramis Belasten Entlasten 1")

    # Dehnung im Verh??ltnis zur Kraft f??r Aramis Belasten Entlasten 2
    analysis.plot_xy([[aramis_belasten_entlasten_2['kraft'], aramis_belasten_entlasten_2['dehnung']]],
                     ["Aramis Belasten Entlasten 2"],
                     "Kraft [N]", "Dehnung [%]", "Aramis Belasten Entlasten 2")

    # Dehnung im Verh??ltnis zur Kraft f??r Belastung Entlastung 7000N
    analysis.plot_xy([[1000*belastung_entlastung_7000n['kraft'], belastung_entlastung_7000n['dms_hinten']/1000],
                      [1000*belastung_entlastung_7000n['kraft'], belastung_entlastung_7000n['dms_vorn']/1000]],
                     ["Belastung Entlastung 7000N (hinten)",
                      "Belastung Entlastung 7000N (vorn)"],
                     "Kraft [N]", "Dehnung [mm]", "Belastung Entlastung 7000N")

    # Torsion im Verh??ltnis zur Kraft f??r Belastung Entlastung 7000N
    analysis.plot_xy([[1000*belastung_entlastung_7000n['kraft'], (belastung_entlastung_7000n['dms_hinten']-belastung_entlastung_7000n['dms_vorn'])/1000]],
                     ["Belastung Entlastung 7000N (hinten-vorn)"],
                     "Kraft [N]", "Dehnung [mm]", "Belastung Entlastung 7000N")
    
    # Dehnung im Verh??ltnis zur Kraft f??r Kabelkompensation Aus Magnet Heissluft
    analysis.plot_xy([[kabelkompensation_aus_magnet_heissluft['zeit'], kabelkompensation_aus_magnet_heissluft['dms_hinten']/1000],
                      [kabelkompensation_aus_magnet_heissluft['zeit'], kabelkompensation_aus_magnet_heissluft['dms_vorn']/1000]],
                     ["Kabelkompensation Aus Magnet Heissluft (hinten)","Kabelkompensation Aus Magnet Heissluft (vorn)"],
                     "Zeit [s]", "Dehnung [mm]", "Kabelkompensation Aus Magnet Heissluft")
    
    # Torsion im Verh??ltnis zur Kraft f??r Kabelkompensation Aus Magnet Heissluft
    analysis.plot_xy([[kabelkompensation_aus_magnet_heissluft['zeit'], (kabelkompensation_aus_magnet_heissluft['dms_hinten']-kabelkompensation_aus_magnet_heissluft['dms_vorn'])/1000]],
                     ["Kabelkompensation Aus Magnet Heissluft (hinten-vorn)"],
                     "Zeit [s]", "Dehnung [mm]", "Kabelkompensation Aus Magnet Heissluft")
    
    # Dehnung im Verh??ltnis zur Kraft f??r Netzkabel Neben Messleitung
    analysis.plot_xy([[netzkabel_neben_messleitung['zeit'], netzkabel_neben_messleitung['dms_hinten']/1000],
                      [netzkabel_neben_messleitung['zeit'], netzkabel_neben_messleitung['dms_vorn']/1000]],
                     ["Netzkabel Neben Messleitung (hinten)","Netzkabel Neben Messleitung (vorn)"],
                     "Zeit [s]", "Dehnung [mm]", "Netzkabel Neben Messleitung")
    
    # Torsion im Verh??ltnis zur Kraft f??r Netzkabel Neben Messleitung
    analysis.plot_xy([[netzkabel_neben_messleitung['zeit'], (netzkabel_neben_messleitung['dms_hinten']-netzkabel_neben_messleitung['dms_vorn'])/1000]],
                     ["Netzkabel Neben Messleitung (hinten-vorn)"],
                     "Zeit [s]", "Dehnung [mm]", "Netzkabel Neben Messleitung")

    # Dehnung im Verh??ltnis zur Kraft f??r Schwingung
    analysis.plot_xy([[schwingung['zeit'], schwingung['dms_hinten']/1000],
                      [schwingung['zeit'], schwingung['dms_vorn']/1000]],
                     ["Schwingung (hinten)","Schwingung (vorn)"],
                     "Zeit [s]", "Dehnung [mm]", "Schwingung")
    
    # Torsion im Verh??ltnis zur Kraft f??r Schwingung
    analysis.plot_xy([[schwingung['zeit'], (schwingung['dms_hinten']-schwingung['dms_vorn'])/1000]],
                     ["Schwingung (hinten-vorn)"],
                     "Zeit [s]", "Dehnung [mm]", "Schwingung")
    
    # Amplitude von Frequenzen bei Schwingung
    fft_x, fft_y = analysis.fast_fourier_transform(schwingung['dms_vorn']-schwingung['dms_hinten'], 2400)
    analysis.plot_xy([[fft_x, fft_y]],
                     ["Schwingung (hinten-vorn)"],
                     "Frequenz [Hz]", "Amplitude", "Schwingung")
    
    # Amplidute von Frequenzen bei Netzkabel Neben Messleitung
    fft_x, fft_y = analysis.fast_fourier_transform(netzkabel_neben_messleitung['dms_vorn']-netzkabel_neben_messleitung['dms_hinten'], 2400)
    analysis.plot_xy([[fft_x, fft_y]],
                     ["Netzkabel Neben Messleitung (hinten-vorn)"],
                     "Frequenz [Hz]", "Amplitude", "Netzkabel Neben Messleitung")

    """
    # Low-Pass-Filter f??r Netzkabel Neben Messleitung
    analysis.plot_xy([[netzkabel_neben_messleitung['zeit'], analysis.low_pass_filter(netzkabel_neben_messleitung['dms_vorn']-netzkabel_neben_messleitung['dms_hinten'], int(2400))]],
                      ["Netzkabel Neben Messleitung (hinten-vorn)"],
                      "Zeit [s]", "Dehnung [mm]", "Netzkabel Neben Messleitung")
    
    # Amplitude von Low-Pass-Filter f??r Netzkabel Neben Messleitung
    fft_x, fft_y = analysis.fast_fourier_transform(analysis.low_pass_filter(netzkabel_neben_messleitung['dms_vorn']-netzkabel_neben_messleitung['dms_hinten'], int(2400)), 2400)
    analysis.plot_xy([[fft_x, fft_y]],
                     ["Netzkabel Neben Messleitung (hinten-vorn)"],
                     "Frequenz [Hz]", "Amplitude", "Netzkabel Neben Messleitung")
    """
    
    # Kraftverlauf bei Arammis Belasten Entlasten 1 Aramis Belasten Entlasten 2
    analysis.plot_xy([[((aramis_belasten_entlasten_1['zeit'])), aramis_belasten_entlasten_1['kraft']*1000],
                      [(aramis_belasten_entlasten_2['index']*0.5)+33, aramis_belasten_entlasten_2['kraft']]],
                      ["Aramis Belasten Entlasten 1", "Aramis Belasten Entlasten 2"],
                     "Zeit [s]", "Kraft [N]", "Aramis Belasten Entlasten")
    
    # Dehnung von Messdatei 2 in Zeitbezug von Messdatei 1 umrechnen
    # index*0.5+33=Zeit
    aramis = {'zeit': aramis_belasten_entlasten_1['zeit'], 'dms_vorn': aramis_belasten_entlasten_1['dms_vorn'], 'dms_hinten': aramis_belasten_entlasten_1['dms_hinten'], 'kraft': aramis_belasten_entlasten_1['kraft']*1000, 'kraft_alt': np.zeros(len(aramis_belasten_entlasten_1['zeit'])).tolist(), 'dehnung': np.zeros(len(aramis_belasten_entlasten_1['zeit'])).tolist()}
    for index, i_zeit in enumerate(aramis_belasten_entlasten_1['zeit']):
        index_neu = int(i_zeit*2-66)
        if(index_neu >= 0 and index_neu < len(aramis_belasten_entlasten_2['index'])):
            aramis['dehnung'][index] = aramis_belasten_entlasten_2['dehnung'][index_neu]
            aramis['kraft_alt'][index] = aramis_belasten_entlasten_2['kraft'][index_neu]
        else:
            aramis['dehnung'][index] = np.nan
            aramis['kraft_alt'][index] = np.nan
        
        
    # Dehnung im Verh??ltnis zur Kraft f??r Aramis Belasten Entlasten
    analysis.plot_xy([[aramis['kraft'], aramis['dehnung']]],
                     ["Aramis Belasten Entlasten"],
                     "Kraft [N]", "Dehnung [%]", "Aramis Belasten Entlasten")
        
    # Dehnung im Verh??ltnis zur Kraft f??r Aramis Belasten Entlasten
    analysis.plot_xy([[aramis['kraft'], aramis['dehnung']],
                      [aramis['kraft_alt'], aramis['dehnung']]],
                     ["Aramis Belasten Entlasten", "Aramis Belasten Entlasten (nicht korrigiert)"],
                     "Kraft [N]", "Dehnung [%]", "Aramis Belasten Entlasten")
    
    # Dehnung im Verh??ltnis zur Kraft f??r Aramis und beide DMS
    analysis.plot_xy([[aramis['kraft'], aramis['dehnung']],
                      [aramis['kraft'], aramis['dms_vorn']/1000],
                      [aramis['kraft'], aramis['dms_hinten']/1000]],
                     ["Aramis", "DMS Vorn", "DMS Hinten"],
                     "Kraft [N]", "Dehnung [%]", "Aramis und DMS")
    
    # Bestimmung von Steigung und y-Achsenabschnitt
    kraft_no_nan = []
    dehnung_no_nan = []
    for i, e in enumerate(aramis['kraft']):
        if(not np.isnan(e) and not np.isnan(aramis['dehnung'][i])):
            kraft_no_nan.append(e/1000)
            dehnung_no_nan.append(aramis['dehnung'][i])
    steigung, offset = analysis.linear_regression(kraft_no_nan, dehnung_no_nan)
    print(f'Steigung: {steigung:.3f} prozentuale Dehnung pro kN\nOffset: {offset:.6f} Prozent')