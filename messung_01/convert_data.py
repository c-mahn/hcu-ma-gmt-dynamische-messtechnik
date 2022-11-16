# This script is used to convert the time series data into standardised .csv-files.

# Import of libraries
import os

# -----------------------------------------------------------------------------

# Functions

def convert_file(filename, delimiter, skiprows=[0]):
    """
    This function converts a file into a .csv-file.
    """
    sum_of_entries = 0
    sum_of_rows = 0
    with open(os.path.join("data_raw", filename)) as file:  # Open the file
        data = file.readlines()  # Read the file
    for i, line in enumerate(data):  # Iterate over the lines
        if(i not in skiprows):  # Check if the line should be skipped
            line = line.split(delimiter)  # Split the line
            for j, e in enumerate(line):  # Iterate over the elements
                line[j] = e.strip()  # Remove the whitespaces
            data[i] = line  # Replace the line
    with open(os.path.join("data_converted", filename.split(".")[0] + ".csv"), "w") as file:  # Open the file
        for line in data:  # Iterate over the lines
            if(data.index(line) not in skiprows):  # Check if the line should be skipped
                sum_of_rows += 1  # Increase the sum of rows
                for j, entry in enumerate(line):  # Iterate over the elements
                    sum_of_entries += 1  # Increase the sum of entries
                    if(entry != ""):  # Check if the entry is empty
                        if(j == 0):  # Check if the entry is the first entry
                            file.write(entry)
                        else:  # Check if the entry is not the first entry
                            file.write(f';{entry}')  # Write the element
                    else:
                        pass
                        # print(f'[WARN] Empty entry in line {data.index(line) + 1} in file "{filename}".')
                file.write("\n")  # Write a new line
    print(f'[INFO] The file {filename} has been converted.')
    print(f'[INFO] The average number of entries per row is {sum_of_entries / sum_of_rows}.')


# -----------------------------------------------------------------------------

# Classes

# -----------------------------------------------------------------------------

# Beginning of main program

if(__name__=='__main__'):
    convert_file("Aramis_Belasten_Entlasten_1.ASC", "\t")
    convert_file("Aramis_Belasten_Entlasten_2.csv", ",")
    convert_file("Belastung_Entlastung_7000N.txt", "\t")
    convert_file("Kabelkompensation_aus_Magnet_Heissluft.ASC", "\t")
    convert_file("Netzkabel neben Messleitung.ASC", "\t")
    convert_file("Schwingung.ASC", "\t")