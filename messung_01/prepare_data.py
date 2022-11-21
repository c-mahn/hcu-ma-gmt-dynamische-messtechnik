# This script is used to convert the time series data into standardised .csv-files.

# Import of libraries
import os
import main as settings

# -----------------------------------------------------------------------------

# Functions

def convert_file(filename, delimiter, skiprows=[0]):
    """
    This function converts a file into a .csv-file.
    """
    print(f'[INFO] Converting "{filename}"\r', end="")
    with open(os.path.join("data_raw", filename)) as file:  # Open the file
        data = file.readlines()  # Read the file
    for i, line in enumerate(data):  # Iterate over the lines
        print(f'[INFO][{int(50*((i+1)/len(data))):02d}%] Converting "{filename}"\r', end="")
        if(i not in skiprows):  # Check if the line should be skipped
            line = line.split(delimiter)  # Split the line
            for j, e in enumerate(line):  # Iterate over the elements
                line[j] = e.strip()  # Remove the whitespaces
            data[i] = line  # Replace the line
    with open(os.path.join("data_converted", f'{filename.split(".")[0]}.csv'), "w") as file:  # Open the file
        for i, line in enumerate(data):  # Iterate over the lines
            print(f'[INFO][{int(50*((i+1)/len(data))+50):02d}%] Converting "{filename}"\r', end="")
            if(i not in skiprows):  # Check if the line should be skipped
                for j, entry in enumerate(line):  # Iterate over the elements
                    if(entry != ""):  # Check if the entry is empty
                        entry = float(entry.strip().replace(",","."))
                        if(j == 0):  # Check if the entry is the first entry
                            file.write(f'{entry}')  # Write the entry
                        else:  # Check if the entry is not the first entry
                            file.write(f';{entry}')  # Write the element
                    else:
                        pass
                        # print(f'[WARN] Empty entry in line {data.index(line) + 1} in file "{filename}".')
                file.write("\n")  # Write a new line
    print(f'[INFO] The file {filename} has been converted successfully.')
    return(f'{filename.split(".")[0]}.csv')


# -----------------------------------------------------------------------------

# Classes

# -----------------------------------------------------------------------------

# Beginning of main program

if(__name__=='__main__'):
    for dataset in settings.datasets:  # Iterate over the datasets
        convert_file(dataset[0], dataset[1])  # Convert the file