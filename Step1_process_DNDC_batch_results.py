"""
A script to process the batch run results of DNDC.
Get needed data of all cases by using a function in a loop, clean the data and write to a .csv.
"""

import pandas as pd


# A function to create a dataframe with desired climate and growth data from one of the batch run results
def get_case_data(i):
    # get needed data from different csv files in each case folder

    # 1. CLIMATE: Temperature, Humidity, Radiation and CO2
    climate = pd.read_csv(
        rf"C:\DNDC\Result\Record\Batch\Case{i}-Amsterdam\Day_Climate_1.csv", header=1
    )
    df1 = pd.DataFrame(climate[["Day", "Temp.(C)", "Humidity()", "Radiation(MJ/m2/d)"]])
    # get the constant CO2 value from input files
    with open(rf"C:\DNDC\BatchRunInputs_PythonGenerated\Input{i}.dnd") as input_file:
        input_lines = input_file.readlines()
        for line in input_lines:
            split_line = line.split()
            if split_line:  # if not empty line
                if split_line[0] == "__Air_CO2_concentration":
                    co2 = split_line[1]
    # create a column for CO2 in dataframe and set all rows to that value
    df1["CO2(ppm)"] = co2

    # 2. GROWTH: Photosynthesis and respirations
    growth = pd.read_csv(
        rf"C:\DNDC\Result\Record\Batch\Case{i}-Amsterdam\Day_SoilC_1.csv",
        header=1,
    )
    df2 = pd.DataFrame(
        growth[
            [
                "Day",
                "Photosynthesis",
                "Leaf-respiration",
                " Stem-respiration",  # the extra space is in the original column names
                " Root-respiration",
            ]
        ]
    )

    # 3. CROP LAI
    crop0 = pd.read_csv(
        rf"C:\DNDC\Result\Record\Batch\Case{i}-Amsterdam\Day_FieldCrop_1.csv", header=2
    )
    crop = crop0.iloc[1:]  # drop row 1 which contains all the units
    crop = crop.rename(columns={"Unnamed: 0": "Day"})
    df3 = pd.DataFrame(crop[["Day", "LAI"]])

    # merge them into one dataframe
    df12 = pd.merge(df1, df2, on="Day")
    df = pd.merge(df12, df3, on="Day")

    # change the type from object to float/int for the whole dataframe
    df = df.apply(pd.to_numeric)

    # combine Shoot respiration = Leaf respiration + Stem respiration
    df["Shoot-respiration"] = df["Leaf-respiration"] + df[" Stem-respiration"]
    df = df.drop(columns=["Leaf-respiration", " Stem-respiration"])

    # rename column names
    df = df.rename(
        columns={
            "Temp.(C)": "Temperature(C)",
            "Humidity()": "Humidity(percent)",
            "Photosynthesis": "Photosynthesis rate(kg C/ha/day)",
            "Shoot-respiration": "Shoot respiration rate(kg C/ha/day)",
            " Root-respiration": "Root respiration rate(kg C/ha/day)",
        }
    )
    # select only the period when crop is growing
    df = df.iloc[59:183, :]  # day 60-183

    return df


if __name__ == "__main__":
    # get total file number
    with open(r"C:\DNDC\BatchRunInputs_PythonGenerated\Batch_inputs.txt") as batch:
        # get the total file number from the first line
        file_number = batch.readline().strip()
    file_number = int(file_number)

    # A while-loop to get needed data from multiple .csv files in all case folders
    n = 1
    data = pd.DataFrame()
    while n <= file_number:
        data = pd.concat([data, get_case_data(n)])
        n += 1
    data.reset_index(drop=True, inplace=True)  # reset index for the whole df

    # write df into a .csv file
    data.to_csv("data_tomato_95cases.csv")
