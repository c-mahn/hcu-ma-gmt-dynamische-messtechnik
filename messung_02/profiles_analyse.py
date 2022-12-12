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
        print(f'[ERROR] File "{filename}" not found.')
        terminate()
        

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


def plot_xy(datenreihen, name=["Messwerte"], x="X", y="Y", title=None, diagram="show"):
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
    if(title != None):
        plt.title(title)
    else:
        plt.title(name[0])
    if(diagram == "show"):
        plt.show()
    elif(diagram == "save"):
        plt.savefig(os.path.join("plots", title + ".png"))


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
    print(f'[INFO] Deleting old files in folder "plots"')
    shutil.rmtree("plots", ignore_errors=True)
    print(f'[INFO] Creating new folder "plots"')
    os.mkdir("plots")
    
    # Plotting the profiles in 3D with intensity as color
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
                                c=profile_points["intensity"],
                                cmap='viridis',
                                linewidth=0.5)
        print(f'[INFO][100.0%] Plotting profiles')
        plot.set_xlabel('X')
        plot.set_ylabel('Y')
        plot.set_zlabel('Z')
        plot.set_title('3D-Plot')
        plt.show()   
        plt.clf()
    
    # Plotting the profiles in 2D with intensity as color
    