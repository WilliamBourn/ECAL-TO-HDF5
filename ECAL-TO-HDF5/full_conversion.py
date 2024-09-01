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

from master_convert_streamline import master_convert as convert

import json             # JSON for reading JSON files
import shutil
import sys
import os
import argparse

#--------------------------------------------------------------------------------------------------

# Main function
def full_conversion(dir,ecal,hdf5,metadata,username,overwrite):

    # Check if base directory exists
    if os.path.exists(dir) == False:
        print("Error: Directory " + dir + " not found.")
        sys.exit(1)
    else:
        print("Directory " + dir + " found.")

    # Check if the metadata file exists
    metadata_path = os.path.join(dir,metadata)
    if os.path.exists(metadata_path) == False:
        print("Error: File " + metadata + " not found.")
        sys.exit(1)
    else:
        print("File " + metadata + " found.")

        # Read the metadata file
        # Open the radar configuration file
        with open(metadata_path) as file:
            meta = json.load(file)

    # Check if the ECAL directory exists
    ecal_dir = os.path.join(dir, ecal)
    if os.path.exists(ecal_dir) == False:
        print("Error: Directory " + ecal_dir + " not found.")
        sys.exit(1)
    else:
        print("Directory " + ecal_dir + " found.")

    # Check if the HDF5 directory exists. If not, create it
    hdf5_dir = os.path.join(dir, hdf5)
    if os.path.exists(hdf5_dir) == False:
        try:
            print("Directory " + hdf5_dir + " not found. Attempting to create directory.")
            os.mkdir(hdf5_dir)
            print("Directory " + hdf5_dir + " created successfully.")
        except:
            print("Error: Failed to create directory " + hdf5_dir + ".")
            sys.exit(1)
    else:
        print("Directory " + hdf5_dir + " found.")

    # Iterate through subdirectories in the ECAL directory. Each will contain a set of data recordings and a radar config file
    for subdir in meta.keys():
        
        # Check if subdirectory exists
        subdir_path = os.path.join(ecal_dir, subdir)
        if os.path.exists(subdir_path) == False:
            print("Error: " + subdir_path + "does not exist.")
            exit(1)
        
        print('Current working directory: ' + subdir)

        # Get the radar config file for the subdirectory
        radar_config = meta[subdir]["radarconfig"]
        
        # Check if radar config file exists
        radar_config_path = os.path.join(subdir_path, radar_config)
        if os.path.exists(radar_config_path) == False:
            print("Error: " + radar_config + " does not exist.")
            exit(1)

        # Check if the output subdirectory exists. If not, create it
        subdir_out = meta[subdir]["out"]
        subdir_out_path = os.path.join(hdf5_dir, subdir_out)
        if os.path.exists(subdir_out_path) == False:
            try:
                print("Directory " + subdir_out_path + " not found. Attempting to create directory.")
                os.mkdir(subdir_out_path)
                print("Directory " + subdir_out_path + " created successfully.")
            except:
                print("Error: Failed to create directory " + subdir_out_path + ".")
                sys.exit(1)
        else:
            print('Current output directory: ' + subdir_out)

        # Check if radar config exists in output subdirectory
        radar_config_out_path = os.path.join(subdir_out_path, radar_config)
        if os.path.exists(radar_config_out_path) == False:

            # Copy radar config file to output subdirectory
            shutil.copyfile(radar_config_path, radar_config_out_path)

        else:
            if overwrite == True:
                
                # Copy radar config file to output subdirectory
                shutil.copyfile(radar_config_path, radar_config_out_path)

            else:

                print("Radar config file already exists in " + subdir_out + ". Continuing")
        

        # Iterate through measurements in subdirectory
        measurements = meta[subdir]["measurements"]
        for measurement in measurements.keys():
            
            print(measurement)
            print(meta[subdir]["measurements"][measurement])

            # Check if measurement exists
            measurement_path = os.path.join(subdir_path, measurement)
            if os.path.exists(measurement_path) == False:
                print("Error: " + measurement + " does not exist.")
                exit(1)
            else:
                
                # Get the measurement type and create directory if it does not exist
                measurement_type = meta[subdir]["measurements"][measurement]["type"]
                measurement_type_path = os.path.join(subdir_out_path, measurement_type)
                if os.path.exists(measurement_type_path) == False:
                    # Create directory
                    print("Creating " + measurement_type + " directory.")
                    os.mkdir(measurement_type_path)
                
                # Convert ECAL to HDF5
                measurement_path_relative = os.path.join(ecal, subdir, measurement)
                file_path_relative = os.path.join(hdf5, subdir_out, measurement_type, measurement + ".hdf5")
                radar_config_path_relative = os.path.join(ecal, subdir, radar_config)
                convert(dir, measurement_path_relative, username, file_path_relative, radar_config_path_relative, overwrite)

            

    # Iterate through subdirectories in the ECAL directory

    '''
    # Remove config data from the recordings list
    if os.path.exists(os.path.join(dir, "config_data")) == False:
        print("Error: No config directory present.")
        sys.exit(1)
    
    recordings_list.remove("config_data")

    # Convert each recording into an hdf5 file in the output directory
    for recording in recordings_list:      
        
        filename = recording + '.hdf5'
        convert(dir, recording, username, hdf5_dir, filename)

    '''

def main():
    '''
    Main function call
    '''

    # Command line argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dir', 
                        type=str, required=False, default='/home/william/MastersProject/Data/',
                        help='Path to the base directory')
    parser.add_argument('-e', '--ecal',
                        type=str, required=False, default='ECAL/',
                        help='Path to the ECAL data directory')
    parser.add_argument('-f', '--hdf5',
                        type=str, required=False, default='HDF5/',
                        help='Path to the HDF5 data directory')
    parser.add_argument('-m', '--metadata',
                        type=str, required=False, default='metadata.json',
                        help='Path to the directory metadata file')
    parser.add_argument('-u','--username',
                        type=str, required=False, default='mmwave',
                        help='The username of the host that captured the data')
    parser.add_argument('-o', '--overwrite',
                        action='store_true', required=False,
                        help='Flag for allowing output files to overwrite existing files')
    args = parser.parse_args()

    #Call main function with command line arguments
    dir = args.dir
    ecal = args.ecal
    hdf5 = args.hdf5
    metadata = args.metadata
    username = args.username
    overwrite = args.overwrite

    full_conversion(dir,ecal,hdf5,metadata,username,overwrite)

if __name__ == "__main__":
    main()
    
#--------------------------------------------------------------------------------------------------