"""
A script to generate a complete template .dnd file,
a number of .dnd files with desired input parameters from config.py file,
and a .txt file as the input file of DNDC's batch run.
"""

import numpy as np
import itertools
from datetime import date, timedelta
from config import config, start_date, end_date


# 1. Generate a complete template .dnd file


# A function takes start_date and end_date from config as input, and returns a string of desired irrigation plan
def irrigation(start_date: date, end_date: date):
    delta = timedelta(days=1)
    days = (end_date - start_date).days + 1
    i = 1
    current = start_date
    output = f"""____Irrigation_applications                                          {days}
____Irrigation_control                                                0
____Irrigation_index                                             0.0000
____Irrigation_method                                                 1"""
    while current <= end_date:
        output += f"""
______Irrigation#                                                     {i}
______Irri_month                                                      {current.month}
______Irri_day                                                        {current.day}
______Water_amount                                                    0
______Irri_method                                                     1
______None                                                            0
______None                                                            0
______None                                                            0
______None                                                            0
______None                                                            0"""
        i += 1
        current += delta
    return output


# Write a template .dnd file with configured irrigation plan
file = open("dnd_template_from_py.dnd", "w")
content = """DNDC_Input_Parameters
----------------------------------------
Site_infomation
                        
__Site_name                                                   Amsterdam
__Simulated_years                                                     1
__Latitude                                                      52.4000
__Daily_record                                                        0
__Unit_system                                                         0
__None                                                                0
__None                                                                0
__None                                                                0
__None                                                                0
__None                                                                0
----------------------------------------
Climate_data                            

__Climate_data_type                                                   1
__N_in_rainfall                                                  0.0000
__Air_NH3_concentration                                          0.0600
__Air_CO2_concentration                                        350.0000
__Climate_files                                                       1
1                                        C:\DNDC\Result\Myinputs\Amsterdam2022climate.txt
__Climate_file_mode                                                   0
__CO2_increase_rate                                              0.0000
__None                                                                0
__None                                                                0
__None                                                                0
__None                                                                0
__None                                                                0
----------------------------------------
Soil_data                               

__Land_use_ID                                                         1
__Soil_texture_ID                                                     3
__Bulk_density                                                   1.1768
__pH                                                             6.4000
__Clay_fraction                                                  0.0900
__Porosity                                                       0.4350
__Bypass_flow                                                    0.0000
__Field_capacity                                                 0.3200
__Wilting_point                                                  0.1500
__Hydro_conductivity                                             0.1248
__Top_layer_SOC                                                  0.0200
__Litter_fraction                                                0.0100
__Humads_fraction                                                0.0230
__Humus_fraction                                                 0.9670
__Adjusted_litter_factor                                         1.0000
__Adjusted_humads_factor                                         1.0000
__Adjusted_humus_factor                                          1.0000
__Humads_C/N                                                    10.0000
__Humus_C/N                                                     10.0000
__Black_C                                                        0.0000
__Black_C_C/N                                                    0.0000
__SOC_profile_A                                                  0.2000
__SOC_profile_B                                                  2.0000
__Initial_nitrate_ppm                                            0.5000
__Initial_ammonium_ppm                                           0.0500
__Soil_microbial_index                                           1.0000
__Soil_slope                                                     0.0000
__Lateral_influx_index                                           1.0000
__Watertable_depth                                               1.0000
__Water_retension_layer_depth                                    9.9900
__Soil_salinity                                                  0.0000
__SCS_curve_use                                                       0
__None                                                                0
__None                                                                0
__None                                                                0
__None                                                                0
__None                                                                0
----------------------------------------
Crop_data                               

Cropping_systems                                                      1

__Cropping_system                                                     1
__Total_years                                                         1
__Years_of_a_cycle                                                    1

____Year                                                              1
____Crops                                                             1
______Crop#                                                           1
______Crop_ID                                                        45
______Planting_month                                                  3
______Planting_day                                                    1
______Harvest_month                                                   8
______Harvest_day                                                     1
______Harvest_year                                                    1
______Residue_left_in_field                                      0.0000
______Maximum_yield                                           1660.6801
______Leaf_fraction                                              0.2200
______Stem_fraction                                              0.2200
______Root_fraction                                              0.2000
______Grain_fraction                                             0.3600
______Leaf_C/N                                                  26.0000
______Stem_C/N                                                  26.0000
______Root_C/N                                                  45.0000
______Grain_C/N                                                 26.0000
______Accumulative_temperature                                1400.0000
______Optimum_temperature                                       25.0000
______Water_requirement                                        900.0000
______N_fixation_index                                           1.0000
______Vascularity                                                0.0000
______If_cover_crop                                                   0
______If_perennial_crop                                               0
______If_transplanted                                                 0
______Tree_maturity_age                                 -107374000.0000
______Tree_current_age                                           0.0000
______Tree_max_leaf                                              0.0000
______Tree_min_leaf                                              0.0000
______None                                                            0
______None                                                            0
______None                                                            0
______None                                                            0
______None                                                            0
______None                                                            0
______None                                                            0

----------------------------------------
____Till_applications                                                 0
----------------------------------------
____Fertilizer_applications                                          -3
____Fertilization_option                                              0
----------------------------------------
____Manure_applications                                               0
----------------------------------------
____Film_applications                                                 0
____Method                                                            2
----------------------------------------
____Flood_applications                                                0
____Water_control                                                     0
____Flood_water_N                                                0.0000
____Leak_rate                                                    0.0000
____Water_gather_index                                           1.0000
____Watertable_file                                                None
____Empirical_para_1                                             0.0000
____Empirical_para_2                                             0.0000
____Empirical_para_3                                             0.0000
____Empirical_para_4                                             0.0000
____Empirical_para_5                                             0.0000
____Empirical_para_6                                             0.0000
----------------------------------------
"""
content += irrigation(start_date, end_date)
file.write(content)
file.close()


# 2. Generate all .dnd files and batch input file from the template and config files

# read template file as list of lines, save to memory and close file
file = open("dnd_template_from_py_with_irrigation.dnd")
template = file.readlines()
file.close()

# make all combinations from given parameter ranges
values = []
for key, value in config.items():  # loop over the parameters in config file
    dict_list = []
    if type(value) is list:
        for num in np.arange(value[0], value[1], value[2]):
            dict_list.append({key: num})
    else:  # value is a number or string
        dict_list.append({key: value})
    values.append(dict_list)
    # e.g. values = [[{"__Latitude": 52.4}],[{"______Water_amount": 1},...],[{"__pH":5},{"__pH": 6},...],...]
all_combi_list = list(
    itertools.product(*values)
)  # a list containing Cartesian product of input iterables

# generate dnd files with given parameter ranges
file_number = 0
filenames = ""
for combi in all_combi_list:  # each combi is a tuple of dictionaries for each new file
    file_number += 1
    filename = rf"C:\DNDC\BatchRunInputs_PythonGenerated\Input{file_number}.dnd"
    with open(filename, "w") as new_file:
        lines = ""
        for line in template:
            split_line = (
                line.split()
            )  # remove spaces and '\n', output is list of string
            if split_line:  # if not empty line
                for elem in combi:  # find each target parameter and replace the number
                    if split_line[0] in elem:
                        line = line.replace(
                            split_line[-1], f"{elem[split_line[0]]:.4f}"
                        )
            lines += line
        new_file.write(lines)
    filenames += (
        "\n" + filename
    )  # write a text file for batch run, containing total file number and all filenames
filenames = str(file_number) + filenames
with open(
    r"C:\DNDC\BatchRunInputs_PythonGenerated\Batch_inputs.txt", "w"
) as batch_file:
    batch_file.write(filenames)
