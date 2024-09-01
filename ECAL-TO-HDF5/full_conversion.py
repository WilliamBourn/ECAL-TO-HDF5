#--------------------------------------------------------------------------------------------------
#   Filename:       full_conversion.py
#   Author:         William Bourn
#   Version:        v1.0
#   Edit Date:      08/04/24
#   
#   Description:    
#   Converts all ECAL file structures in a given directory into a set of HDF5 file structures in
#   the given output directory. Special thanks to Nick Bowden for providing the backbone code.
#
#--------------------------------------------------------------------------------------------------

from cl_convert import main as ecalconvert

import sys
import os
import argparse

#--------------------------------------------------------------------------------------------------

# Main function
def main(input_directory, output_directory, host_username):

    # Check if input directory exists
    if os.path.exists(input_directory) == False:
        print("Error: Directory " + input_directory + " not found.")
        sys.exit(1)
    else:
        print("Directory " + input_directory + " found.")

    # Check if output directory exists. If not, create it
    if os.path.exists(output_directory) == False:
        try:
            print("Directory " + output_directory + " not found. Attempting to create directory.")
            os.mkdir(output_directory)
            print("Directory " + output_directory + " created successfully.")
        except:
            print("Error: Failed to create directory " + output_directory + ".")
            sys.exit(1)
    else:
        print("Directory " + output_directory + " found.")

    # Get a list of subdirectories in the input directory. Each will contain a data recording
    recordings_list = os.listdir(input_directory)

    # Remove config data from the recordings list
    if os.path.exists(os.path.join(input_directory, "config_data")) == False:
        print("Error: No config directory present.")
        sys.exit(1)
    
    recordings_list.remove("config_data")

    # Convert each recording into an hdf5 file in the output directory
    for recording in recordings_list:      
        
        filename = recording + '.hdf5'
        ecalconvert(input_directory, recording, host_username, output_directory, filename)

if __name__ == "__main__":
    
    # Command line argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--input_directory', type=str, required=True, help='Full path to the conversion directory')
    parser.add_argument('-o', '--output_directory', type=str, required=True, help='Full path to the output directory')
    parser.add_argument('-u', '--username', type=str, required=False, default='mmwave', help='The username of the host')
    args = parser.parse_args()

    #Call main function with command line arguments
    input_directory = args.input_directory
    output_directory = args.output_directory
    host_username = args.username

    main(input_directory, output_directory, host_username)

#--------------------------------------------------------------------------------------------------