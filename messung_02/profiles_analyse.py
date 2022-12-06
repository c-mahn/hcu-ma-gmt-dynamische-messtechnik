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
    for dataset in settings.datasets:
        for profile in range(dataset["profiles"]):
            print(f'[INFO] Importing profile {profile+1} from {dataset["filename"]}')
            profile_data = import_profile(f'{dataset["filename"].split(".")[0]}_{profile+1:05d}.csv')
            plot_xy([[profile_data["y"], profile_data["x"]]],
                    x="Y", y="X", diagram="save",
                    name=[f'Profil {profile+1:05d}'],
                    title=f'{dataset["filename"].split(".")[0]}_Profil_{profile+1:05d}')
            plot_werte([profile_data["x"], profile_data["y"], profile_data["z"], profile_data["intensity"]],
                       name=["X", "Y", "Z", "Intensity"], title=f'werte_{dataset["filename"].split(".")[0]}_Profil_{profile+1:05d}', diagram="save")
