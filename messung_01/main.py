# Main-Script
# #############################################################################

# This python script automatically launches all other python scripts in the
# right order and computes the entire task.

# Authors:
# Christopher Mahn
# Silas Teske
# Joshua Wolf
# Maria Riegel

# #############################################################################

# Import of Libraries
# -----------------------------------------------------------------------------

import math as m
# import string as st
# import random as r
# import re
import os
import platform

from sklearn import datasets


# -----------------------------------------------------------------------------
# Debugging-Settings

verbose = True  # Shows more debugging information


# -----------------------------------------------------------------------------
# Project-Settings

# These settings affect how the executed scripts below will compute the data.
# Changing these values may increase execution-time significantly or allowes to
# change the computed input or output.

# These are the datasets that will be used for the computation.
datasets = [["Aramis_Belasten_Entlasten_1.ASC", "\t"],
            ["Aramis_Belasten_Entlasten_2.csv", ","],
            ["Belastung_Entlastung_7000N.txt", "\t"],
            ["Kabelkompensation_aus_Magnet_Heissluft.ASC", "\t"],
            ["Netzkabel neben Messleitung.ASC", "\t"],
            ["Schwingung.ASC", "\t"]]

# This variable stores the converted datasets. It is populated automatically
datasets_converted = []
for dataset in datasets:
    datasets_converted.append(f'{dataset[0].split(".")[0]}.csv')

# These are all measurements with their corresponding titles.
measurements = []

# Functions
# -----------------------------------------------------------------------------

def __run_script(script_name):
    """
    This function executes python scripts via the command line.

    Args:
        script_name (str): name of the python script (eg: "demo.py")
    """
    if(platform.system() == "Linux"):
        if(verbose):
            print(f'[INFO] Executing "{script_name}" as Linux-User')
        os.system(f'python3 {script_name}')  # Run on Linux
    elif(platform.system() == "Windows"):
        if(verbose):
            print(f'[INFO] Executing "{script_name}" as Windows-User')
        user = os.environ.get('USERNAME')
        os.system(f'C:/Users/{user}/anaconda3/python.exe {script_name}')  # Run on Windows


# Classes
# -----------------------------------------------------------------------------


# Beginning of the Programm
# -----------------------------------------------------------------------------

if __name__ == '__main__':
    __run_script("prepare_data.py")
    __run_script("plot_data.py")
