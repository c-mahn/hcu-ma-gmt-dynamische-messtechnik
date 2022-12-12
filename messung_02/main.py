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
datasets = [{"filename": "rps25_synch.txt","delimiter": ";","split_column": 0, "profiles": 1143},
            {"filename": "rps50_synch.txt","delimiter": ";","split_column": 0, "profiles": 2124}]

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
    os.makedirs("data_raw", exist_ok=True)
    # __run_script("profiles_split.py")
    __run_script("profiles_analyse.py")
