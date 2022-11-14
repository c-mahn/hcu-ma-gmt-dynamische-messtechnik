# This script is used to convert the time series data into standardised .csv-files.

# Import of libraries
import os

# -----------------------------------------------------------------------------

# Functions

def convert_file(filename, delimiter, columns, skiprows=[0]):
    """
    This function converts a file into a .csv-file.
    """
    with open(os.path.join("data_raw", filename)) as file:  # Open the file
        data = file.readlines()  # Read the file
    for line in data:  # Iterate over the lines
        if(data.index(line) not in skiprows):  # Check if the line should be skipped
            line = line.split(delimiter)  # Split the line
            for i, e in enumerate(line):  # Iterate over the elements
                line[i] = e.strip()  # Remove the whitespaces
            data[data.index(line)] = line  # Replace the line
    with open(os.path.join("data", filename.split(".")[0] + ".csv"), "w") as file:  # Open the file
        for line in data:  # Iterate over the lines
            if(data.index(line) not in skiprows):  # Check if the line should be skipped
                for i, e in enumerate(line):  # Iterate over the elements
                    if(i in columns):  # Check if the element should be written
                        file.write(e + ";")  # Write the element
                file.write("\n")  # Write a new line


# -----------------------------------------------------------------------------

# Classes

# -----------------------------------------------------------------------------

# Beginning of main program

if(__name__=='__main__'):