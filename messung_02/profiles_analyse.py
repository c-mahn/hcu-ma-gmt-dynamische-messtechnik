# This script is used to plot the data in different ways.

# Authors:
# Christopher Mahn
# Silas Teske
# Joshua Wolf
# Maria Riegel

# Import of libraries
import os
import main as settings
import matplotlib.pyplot as plt
import numpy as np
import shutil
from scipy.fft import fft, fftfreq
from scipy import signal
from profiles_split import terminate

# -----------------------------------------------------------------------------
# Functions

def import_profile(filename):
    """
    This function imports a profile from a .csv-file.
    """
    try:
        with open(os.path.join("data_split", filename), "r") as f:
            data = f.readlines()
        points = {"number": [], "x": [], "y": [], "z": [], "intensity": [], "time": []}
        for line in data:
            line = line.split(";")
            points["number"].append(int(line[1]))
            points["x"].append(float(line[2]))
            points["y"].append(float(line[3]))
            points["z"].append(float(line[4]))
            points["intensity"].append(float(line[5]))
            points["time"].append(float(line[6]))
        return(points)
    except FileNotFoundError:
        print(f'[ERROR] File "{filename}" not found in the folder "data_split". Execute the script "profiles_split.py" first.')
        terminate()


def fast_fourier_transform(datenreihe, sample_rate):
    """
    Diese Funktion macht eine Fast-Fourier-Transformation und gibt die Frequenz-
    und Amplitudengraphen zurück.
    """
    N = len(datenreihe)
    T = 1.0 / sample_rate
    yf = fft(datenreihe)
    xf = fftfreq(N, T)[:N//2]
    return(xf, 2.0/N * np.abs(yf[0:N//2]))
        

def plot_werte(datenreihen, name=["Messwerte"], title=None, diagram="show"):
    """
    Diese Funktion nimmt Datenreihen und plottet diese in ein Diagramm.
    """
    plt.cla()
    for i, datenreihe in enumerate(datenreihen):
        zeit = range(len(datenreihe))
        plt.plot(zeit, datenreihe)
    plt.legend(name)
    plt.grid()
    plt.xlabel("")
    plt.ylabel("")
    if(title != None):
        plt.title(title)
    else:
        plt.title(name[0])
    if(diagram == "show"):
        plt.show()
    elif(diagram == "save"):
        plt.savefig(os.path.join("plots", title + ".png"))


def plot_xy(datenreihen, name=["Messwerte"], x="X", y="Y", title=None, diagram="show", size={'x_min': 0, 'x_max': 0, 'y_min': 0, 'y_max': 0}, fixed_size=False):
    """
    Diese Funktion nimmt je zwei Datenreihen und plottet diese in Abhängigkeit
    zueinander in ein Diagramm.
    """
    plt.clf()
    for datenreihe in datenreihen:
        plt.plot(datenreihe[0], datenreihe[1])
    plt.legend(name)
    plt.grid()
    plt.xlabel(x)
    plt.ylabel(y)
    if(fixed_size):
        plt.xlim(size['x_min'], size['x_max'])
        plt.ylim(size['y_min'], size['y_max'])
    if(title != None):
        plt.title(title)
    else:
        plt.title(name[0])
    if(diagram == "show"):
        plt.show()
    elif(diagram == "save"):
        plt.savefig(os.path.join("plots", title + ".png"))


# -----------------------------------------------------------------------------
# Classes

# -----------------------------------------------------------------------------
# Beginning of main program

if(__name__=='__main__'):
    print(f'[INFO] Deleting old files in folder "plots"')
    shutil.rmtree("plots", ignore_errors=True)
    print(f'[INFO] Creating new folder "plots"')
    os.mkdir("plots")

    '''
    # Plotting the profiles in 3D with intensity as color (X, Y, Z)
    offset = 0.002  # Offset for each profile
    subsample = 20  # Only plot every n-th profile
    for dataset in settings.datasets:
        plot = plt.figure().add_subplot(projection='3d')
        for profile in range(dataset["profiles"]):
            if(profile % subsample == 0):
                print(f'[INFO][{profile/dataset["profiles"]*100:5.1f}%] Plotting profiles', end='\r')
                # Plot in 3D with an offset for each profile
                profile_points = import_profile(f'{dataset["filename"].split(".")[0]}_{profile+1:05d}.csv')
                plot.scatter(np.array(profile_points["x"])+(profile*offset),
                                profile_points["y"],
                                profile_points["z"],
                                cmap='viridis',
                                linewidth=0.5)
        print(f'[INFO][100.0%] Plotting profiles')
        plot.set_xlabel('X')
        plot.set_ylabel('Y')
        plot.set_zlabel('Z')
        plot.set_title('3D-Plot')
        plot.set_ylim3d(-1.5, 1.5)
        plot.set_zlim3d(-2.0, 1.0)
        plt.show()   
        plt.clf()
    '''
    
    # Plotting all profiles in 2D (Y, Z)
    for dataset in settings.datasets:
        for profile in range(dataset["profiles"]):
            if(profile % 25 == 0):
                print(f'[INFO][{profile/dataset["profiles"]*100:5.1f}%] Plotting profiles', end='\r')
            profile_points = import_profile(f'{dataset["filename"].split(".")[0]}_{profile+1:05d}.csv')
            plot_xy([[profile_points["y"], profile_points["z"]]], x="Y", y="Z",
                    title=f'slice_{dataset["filename"].split(".")[0]}_profile{profile+1:05d}', diagram="save",
                    size={'x_min': -1.5, 'x_max': 1.5, 'y_min': -1.5, 'y_max': 0.8}, fixed_size=True)
        print(f'[INFO][100.0%] Plotting profiles')
        plt.clf()
        
    # Plotting all profiles in 2D as Spectrum (value, index)
    for dataset in settings.datasets:
        for profile in range(dataset["profiles"]):
            if(profile % 25 == 0):
                print(f'[INFO][{profile/dataset["profiles"]*100:5.1f}%] Plotting spectrums', end='\r')
            profile_points = import_profile(f'{dataset["filename"].split(".")[0]}_{profile+1:05d}.csv')
            indices = range(len(profile_points["intensity"]))
            plot_xy([[indices, profile_points["intensity"]],
                     [indices, profile_points["x"]],
                     [indices, profile_points["y"]],
                     [indices, profile_points["z"]]],
                    name=["Intensity", "X", "Y", "Z"], x="index [1]", y="Koord. [m] / Intensity [1]",
                    size={'x_min': 0, 'x_max': len(indices), 'y_min': -1.5, 'y_max': 1.5}, fixed_size=True,
                    title=f'spectrum_{dataset["filename"].split(".")[0]}_profile{profile+1:05d}', diagram="save")
        print(f'[INFO][100.0%] Plotting spectrums')
        plt.clf()
    
    # Getting timeseries of horizontal and vertical movement
    for dataset in settings.datasets:
        timeseries = {"left": [], "right": [], "top": []}
        for profile in range(dataset["profiles"]):
            if(profile % 25 == 0):
                print(f'[INFO][{profile/dataset["profiles"]*100:5.1f}%] Getting timeseries', end='\r')
            profile_points = import_profile(f'{dataset["filename"].split(".")[0]}_{profile+1:05d}.csv')
            left_0 = int(dataset["left"][0])
            left_1 = int(dataset["left"][1])
            right_0 = int(dataset["right"][0])
            right_1 = int(dataset["right"][1])
            top_0 = int(dataset["top"][0])
            top_1 = int(dataset["top"][1])
            left = np.array(profile_points["y"])[left_0:left_1].mean()
            right = np.array(profile_points["y"])[right_0:right_1].mean()
            top = np.array(profile_points["z"])[top_0:top_1].mean()
            timeseries["left"].append(left)
            timeseries["right"].append(right)
            timeseries["top"].append(top)
        plot_xy([[range(len(timeseries["left"])), timeseries["left"]],
                 [range(len(timeseries["right"])), timeseries["right"]],
                 [range(len(timeseries["top"])), timeseries["top"]]],
                name=["left", "right", "top"], x="index [1]", y="Koord. [m]",
                title=f'timeseries_{dataset["filename"].split(".")[0]}', diagram="save")
        print(f'[INFO][100.0%] Getting timeseries')
        print(f'[INFO] Generating FFT-plots')
    
        # Plotting frequency spectrum of horizontal and vertical movement
        # left
        fft_x, fft_y = fast_fourier_transform(timeseries["left"], dataset["sample_rate"])
        plot_xy([[fft_x, fft_y]], x="Frequency [Hz]", y="Amplitude [1]", title=f'fft_{dataset["filename"].split(".")[0]}_left', diagram="save",
                size={'x_min': 0, 'x_max': 10, 'y_min': 0, 'y_max': 0.05}, fixed_size=True)
        
        # right
        fft_x, fft_y = fast_fourier_transform(timeseries["right"], dataset["sample_rate"])
        plot_xy([[fft_x, fft_y]], x="Frequency [Hz]", y="Amplitude [1]", title=f'fft_{dataset["filename"].split(".")[0]}_right', diagram="save",
                size={'x_min': 0, 'x_max': 10, 'y_min': 0, 'y_max': 0.05}, fixed_size=True)
        
        # top
        fft_x, fft_y = fast_fourier_transform(timeseries["top"], dataset["sample_rate"])
        plot_xy([[fft_x, fft_y]], x="Frequency [Hz]", y="Amplitude [1]", title=f'fft_{dataset["filename"].split(".")[0]}_top', diagram="save",
                size={'x_min': 0, 'x_max': 10, 'y_min': 0, 'y_max': 0.05}, fixed_size=True)
