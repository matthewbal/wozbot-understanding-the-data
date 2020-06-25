#########################
# kaggle-analysis.py
# Author: Matt Balshaw
##########################
# Loads the dataset from kaggle csv
# Explore the data with pandas
# Determine which data to ignore, which to fix
#########################

import pandas as pd

if __name__ == "__main__":

    #####
    # Read the CSV in with pandas
    kagglePath = "rawdata/weatherAUS.csv"
    k = pd.read_csv(kagglePath, parse_dates=["Date"])

    #####
    # See data
    print(k)
    print(k.columns.tolist())
    print(k.dtypes)
    print(k.ndim)
    print(k.info())
    print(k.describe())
    print(k.count())
    print("total length: %s" % len(k))

    #####
    # We have some missing values, lets see how bad it is
    sunMissPct = k['Sunshine'].isnull().sum() / k.shape[0] * 100
    print("Missing %s Percent Sunshine data" % sunMissPct)

    #####
    # See number of locations
    locs = k[['Location']].groupby(['Location'])['Location'].count()
    locs = locs.sort_values()
    print(locs)

    #####
    # We have some missing data.
    # Ensure we account for all missing dates
    # print(k)
    k.set_index('Date', inplace=True)
    # print(k)
    # k.resample("D").sum().fillna(None)

    print(k)
    locs = k[['Location']].groupby(['Location'])['Location'].count()
    locs = locs.sort_values()
    print(locs)

    #####
    # We aren't missing data in the middle of each set
    # Seems like we only have limited time periods for some locations
    print(k[k['Location'] == "Canberra"])
    print(k[k['Location'] == "Uluru"])
    print(k[k['Location'] == "MountGinini"])
    print(k[k['Location'] == "Perth"])

    # Canberra starts from 2007
    # Uluruu starts from 2013
    # MountGinini starts from 2008

    #####
    # Truncate data so that we trim all data before 2008
    # Also truncate any data after 2017-01 to check
    # We want to see all locations have equal lengths

    k = k[k.index > "2008-12-01"]
    k = k[k.index < "2017-01-01"]

    print(k)
    locs = k[['Location']].groupby(['Location'])['Location'].count()
    locs = locs.sort_values()
    print(locs)

    print(k[k['Location'] == "MountGinini"])
    print(k[k['Location'] == "Perth"])

    # Mount Ginini & perth still have different # of records
    # They start and end on same date.
    # Must be missing some records.
    # Lets explore deeper with some profile reports.
