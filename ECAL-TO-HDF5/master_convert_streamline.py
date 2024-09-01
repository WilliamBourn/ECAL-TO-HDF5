
# realsense
from convert_realsense_depth import convert as convert_realsense_depth
from convert_realsense_colour import convert as convert_realsense_colour

## other sensors
from convert_radar import convert as convert_radar

from ecal.measurement.hdf5 import Meas

import os
import glob
import h5py

import argparse

def get_channel_names(path_to_folder):
    
    measurements = Meas(path_to_folder)
    channel_names = measurements.get_channel_names()
    return channel_names

def master_convert(dir, measurement, username, file, config, overwrite):

    print("ECAL TO HDF5 CONVERSION:")
    print()
    
    # use this map to enable sensors 
    sensor_list = {
        "Realsense_Colour"  :   True,
        "Realsense_Depth"   :   True,
        "TI_Radar"          :   True,
    }

    # Only thing that might need to be changed after this point is channel name used 
    # which is an argument to each convert function. Check default against channels 
    # listed in terminal when this script is run 
    
    ecal_folder = os.path.join(dir,measurement,username)
    
    # notes source 
    print("Loading experiment notes file.")
    with open(os.path.join(dir,measurement,"doc/description.txt"), 'r') as file:
        data = file.read()  

    print("Creating output file")
    try:
        if overwrite == True:
            out_file = h5py.File(os.path.join(dir, file),'w')
        else:
            out_file = h5py.File(os.path.join(dir, file),'x')
    except:
                
        print("Passing " + measurement + " because " + file + " already exists.\n")
        return

    commentGrp = out_file.create_group("Comments")
    setup=[data.encode("ascii")]  
    commentGrp.create_dataset("experiment_setup", shape=(len(setup),1), data=setup) 

    commentGrp.create_dataset("sensor_list", data=[str(sensor_list).encode("ascii")]) 

    channel_names = get_channel_names(ecal_folder)
    
    print("Available Channels: ")
    for name in channel_names:
        print("    |--",name)

    print()

    sensors_grp = out_file.create_group("Sensors")

    # unpack realsense colour
    if sensor_list["Realsense_Colour"]:
        rs_colour_grp = sensors_grp.create_group("Realsense_Colour")
        convert_realsense_colour(ecal_folder,rs_colour_grp,channel_name = "rt/camera/camera/color/image_raw")

    # unpack realsense depth
    if sensor_list["Realsense_Depth"]:
        rs_depth_grp = sensors_grp.create_group("Realsense_Depth")
        convert_realsense_depth(ecal_folder,rs_depth_grp,channel_name="rt/camera/camera/depth/image_rect_raw")

    # unpack radar data
    if sensor_list["TI_Radar"]:
        path_to_config = os.path.join(dir,config)
        radar_grp = sensors_grp.create_group("TI_Radar")
        convert_radar(ecal_folder,path_to_config,radar_grp,channel_name="rt/radar_data")
    

def main():
    '''
    Main function.
    '''

    # Command line argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-d','--dir', 
                        type=str, required=True,
                        help='Path to the base directory')
    parser.add_argument('-m','--measurement',
                        type=str, required=True,
                        help='Path to the directory containing the measurement to convert')
    parser.add_argument('-f','--file',
                        type=str, required=True,
                        help='Path to the file containing the output HDF5 data')
    parser.add_argument('-u','--username',
                        type=str, required=False, default='mmwave',
                        help='The username of the host that captured the data')
    parser.add_argument('-c','--config',
                        type=str, required=False, default='config.json',
                        help='Path to the radar configuration file')
    parser.add_argument('-o', '--overwrite',
                        action='store_true', required=False,
                        help='Flag for allowing output files to overwrite existing files')
    args = parser.parse_args()
    
    # Specify data path and output names
    #dir = "Test_Data"
    #measurement = "corner_3m_statiionary"
    #username = "mmwave" # it found as a sub dir of ecal meas folder 
    #file = "mmwave.hdf5"

    dir = args.dir
    measurement = args.measurement
    username = args.username
    file = args.file
    config = args.config
    overwrite = args.overwrite

    master_convert(dir, measurement, username, file, config, overwrite)

# Command line main function call
if __name__ == "__main__":
    main()
