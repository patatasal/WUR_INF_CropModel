import numpy as np
import pandas as pd


# a function to convert secondly crop data to hourly crop data
def s_to_h_crop(filename):
    df = pd.read_csv(filename, header=0)
    df_stem = df[["second", "cStem"]]  # select the columns we need
    df_stem_hour = df_stem.iloc[::12]  # select every 12th row
    df_stem_hour["second"] = df_stem_hour["second"] / 3600
    df_stem_hour = df_stem_hour.rename(columns={"second": "hour"})
    return df_stem_hour


# a function to convert secondly climate data to hourly climate data
def s_to_h_clim(filename):
    df = pd.read_csv(filename, header=0)
    df_clim = df[["second", "co2Air", "tAir", "vpAir"]]  # select the columns we need
    df_clim_hour = df_clim.iloc[::12]  # select every 12th row
    df_clim_hour["second"] = df_clim_hour["second"] / 3600
    df_clim_hour = df_clim_hour.rename(columns={"second": "hour"})
    return df_clim_hour


# a function to concat two half-year hourly dataframes to get a one-year dataframe
def concat_dfs(df1, df2):
    df2["hour"] = df2["hour"] + 4320  # set the 1st hour of df2 to 4320h = 180d * 24h
    df = pd.concat(
        [df1, df2], ignore_index=True
    )  # concat by row, ignore original index and set new index
    return df


# a function to convert hourly climate data to daily climate data
def h_to_d_clim(df_h):
    df_d = pd.DataFrame()
    df_d["day"] = np.arange(0, len(df_h) // 24, 1)
    df_d[["co2Air", "tAir", "vpAir"]] = (
        df_h[["co2Air", "tAir", "vpAir"]]
        .groupby(np.arange(len(df_h)) // 24)
        .mean()  # group the rows and get the mean of each day
    )
    return df_d


# a function to combine daily climate data with hourly crop data into one df and write to csv
def combine_h_and_d(df_h, df_d):
    df = pd.DataFrame()
    for n in range(len(df_d)):
        per_day = pd.DataFrame(df_d.iloc[n, :]).transpose().drop(columns="day")
        hour_per_day = (
            pd.DataFrame(df_h.iloc[n * 24 : (n + 1) * 24, 1])
            .reset_index()
            .drop(columns="index")
            .transpose()
            .reset_index()
            .drop(columns="index")
            .set_index([per_day.index])
        )
        per_day = per_day.apply(pd.to_numeric)
        hour_per_day = hour_per_day.apply(pd.to_numeric)
        df_per_day = per_day.join(hour_per_day)
        df = pd.concat([df, df_per_day])
    return df


if __name__ == "__main__":
    df_crop_h = concat_dfs(
        s_to_h_crop("crop_csv_AmsD1-180.csv"), s_to_h_crop("crop_csv_AmsD181-360.csv")
    )
    df_clim_h = concat_dfs(
        s_to_h_clim("indoorClim_csv_AmsD1-180.csv"),
        s_to_h_clim("indoorClim_csv_AmsD181-360.csv"),
    )
    df_clim_d = h_to_d_clim(df_clim_h)
    df_final = combine_h_and_d(df_crop_h, df_clim_d)
    df_final.to_csv("data_3to24.csv")
