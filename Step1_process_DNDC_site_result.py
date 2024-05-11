"""
A script to process the site run results of DNDC.
Get needed data and clean the data using a function, and write to a .csv.
"""

import pandas as pd


def get_site_data(input_filename):
    # get needed data from different .csv files in each case folder

    # 1. CLIMATE: Temperature, Humidity, Radiation and CO2
    climate = pd.read_csv(rf"C:\DNDC\Result\Record\Site\Day_Climate_1.csv", header=1)
    df1 = pd.DataFrame(climate[["Day", "Temp.(C)", "Humidity()", "Radiation(MJ/m2/d)"]])
    # get the constant CO2 value from input files
    with open(input_filename) as input_file:
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
        rf"C:\DNDC\Result\Record\Site\Day_SoilC_1.csv",
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
    crop0 = pd.read_csv(rf"C:\DNDC\Result\Record\Site\Day_FieldCrop_1.csv", header=2)
    crop = crop0.iloc[1:]  # drop row 1 which contains all the units
    crop = crop.rename(columns={"Unnamed: 0": "Day"})
    df3 = pd.DataFrame(crop[["Day", "LAI"]])

    # merge all dfs into one df
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
    data = get_site_data(
        rf"C:\DNDC\Myinputs\Tomato1_Amsterdam2023_test_all_parameters.dnd"
    )
    data.reset_index(drop=True, inplace=True)
    print(data.head())
    data.to_csv("data_tomato_test.csv")
