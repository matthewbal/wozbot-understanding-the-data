#########################
# generate-reports.py
# Author: Matt Balshaw
##########################
# Use a library to fast track data analysis
# Generate HTML reports for data set
#########################

import pandas as pd
from pandas_profiling import ProfileReport

if __name__ == "__main__":

    #####
    # Read the Kaggle Data Frame in with pandas
    kagglePath = "rawdata/weatherAUS.csv"
    kDF = pd.read_csv(kagglePath, parse_dates=["Date"])

    #####
    # Change yes/no values to 1/0 so that we can see correlations
    kDF.RainToday.map(dict(yes=1, no=0))
    kDF.RainTomorrow.map(dict(yes=1, no=0))

    #####
    # Use subset of data to start with
    melbkDF = kDF[kDF['Location'] == "Melbourne"]

    #####
    # Generate pandas profiling report
    profile = ProfileReport(
        melbkDF, title='Melbourne Data', explorative=True)
    profile.to_file("rawdata/Melbourne.html")

    #####
    # Generate pandas profiling report for two interesting locations
    mntkDF = kDF[kDF['Location'] == "MountGinini"]
    pthkDF = kDF[kDF['Location'] == "Perth"]

    profile = ProfileReport(
        mntkDF, title='MountGinini Data', explorative=True)
    profile.to_file("rawdata/MountGinini.html")
    profile = ProfileReport(
        pthkDF, title='Perth Data', explorative=True)
    profile.to_file("rawdata/Perth.html")

    #####
    # Generate pandas profiling report for All Data

    profile = ProfileReport(
        kDF, title='All Kaggle Data', explorative=True)
    profile.to_file("rawdata/allKaggle.html")

    #####
    # Notes:
    #####
    # Risk_MM is a cheating variable as it is based on rain tomorrow somehow.
    #####
    # Missing lots of data in 2013
    # Overall more data from 2014 onwards
    # should therefore only use 2014 onwards
    # Should remove locations with high missing data
    # Then use forward fill
    # EM algorithm looks great, but complex
    #####
    # Mount Ginnini completely missing Evap, sunshine, pressure, clouds
    # Means some locations will be missing some fields alltogether.
    #####
    # Nothing seems to correlate with rainfall,
    # except risk_MM which is a cheat variable
    # With Phik correlation, RainTomorrow correlates well with several values!
    # In order (just by sight):
    # Humidity 3pm,
    # Sunshine,
    # Clouds 3pm,
    # RainToday,
    # cloud 9am,
    # humid 0am,
    # temp 3pm,
    # windgustspeed
    #####
    # Evaporation is 42% missing in total dataset
    # Sunshine is 48% missing in total dataset (Big shame!)
    # Clouds 9am and 3pm 37.7% missing values
    # We should truncate locations and see if we can improve this.
    #####
