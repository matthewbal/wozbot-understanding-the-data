#########################
# clean-data.py
# Author: Matt Balshaw
##########################
# After analysis, clean the data
#########################

import pandas as pd
from pandas_profiling import ProfileReport


def cleanbyColumn(df, colName):

    # Get a pandas series with date, location and the column we care about
    newDF = df.copy()
    newDF = newDF[['Location', colName]]

    # We need to ignore any "Nan" values
    newDF.dropna(inplace=True)

    # Determine how many values for the col each location has
    locs = newDF[['Location']].groupby(['Location'])['Location'].count()
    # Helps us to visualise
    locs = locs.sort_values()
    # print(locs)

    # Find locations that have 1 standard deviation less values
    mean = locs.mean()
    std = locs.std()
    minVal = mean - std
    locs = locs[locs < minVal]
    # turn this into a list of invalid locations
    invalidLocs = locs.index.tolist()
    # print(invalidLocs)

    # Return the invalid locations
    return invalidLocs

if __name__ == "__main__":

    #####
    # Read the Kaggle Data Frame in with pandas
    kagglePath = "rawdata/weatherAUS.csv"
    kDF = pd.read_csv(kagglePath, parse_dates=["Date"])
    kDF.set_index('Date', inplace=True)
    kDF = kDF[kDF.index > "2014-01-01"]

    # Remove locations that are missing a lot of the values we want
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

    # We have a list of critical column names
    # For each column name, we will remove any locations that
    # have one standard deviation less values for that column.

    # EG, if one location is missing "Rainfall" data, but the rest have
    # a few thousand values, that location will be removed from the DF
    # If none of the others had that much data, we wouldn't remove anything

    criticalCols = [
        "Rainfall",
        "MinTemp",
        "MaxTemp",
        "Humidity9am",
        "Humidity3pm",
        "Temp9am",
        "Temp3pm",
        "WindGustSpeed",
        "Sunshine",
        "Evaporation",
        "Cloud9am",
        "Cloud3pm"
    ]

    # criticalCols = [
    #     "Evaporation",
    # ]

    invalidLocs = []

    for criticalCol in criticalCols:
        print("Invalid locations before %s: %s" %
              (criticalCol, len(invalidLocs)))
        newInvalids = cleanbyColumn(kDF, criticalCol)

        for loc in newInvalids:
            if loc not in invalidLocs:
                invalidLocs.append(loc)

        print("Invalid locations after %s: %s" %
              (criticalCol, len(invalidLocs)))

    print("We will filter out the following locations:")
    print(invalidLocs)
    # Results:
    # many locations are missing various data
    # If we need evaporation and clouds, we need to remove 17 locations
    # That leaves us with 32 locations. (40133 rows)
    # If we can ignore them, then we can remove only 10 locations
    # That leaves us with 39 locations. (48919 rows)
    # Since we want to use these factors, we will deal with having
    # less data for now.

    # Filter out these locations from the original dataframe passed in
    kDF = kDF[~kDF.Location.isin(invalidLocs)]

    print(kDF)
    print("Remaining valid locations: %s" %
          (len(kDF.groupby(['Location']))))

    # Now we want to fill all the empty values.
    # if we drop all rows that are missing at least one critical value
    # We find we have only 17762 rows will all their data
    # print(kDF.dropna(subset=criticalCols))
    # If we run into problems later, we will come back and drop those.

    # We need to interpolate the nan values
    # This only works on numerical values

    # Note: Pandas interpolation defaults to forward filling
    # https://github.com/pandas-dev/pandas/pull/10691
    # We have to set "Both" to ensure that interpolation happens
    # For columns with NAN's at the start of the data

    for col in criticalCols:
        kDF[col] = kDF[col].interpolate(limit_direction='both')

    print(kDF)

    # Lets filter out some of the columns we won't use
    # We'll also transform the "no"/"yes" cols into 1/0 cols

    # Change yes/no values to 1/0 so that we can see correlations
    kDF['RainToday'] = kDF['RainToday'].map({'Yes': 1., 'No': 0.})
    kDF['RainTomorrow'] = kDF['RainTomorrow'].map({'Yes': 1., 'No': 0.})

    wantedCols = [
        "Location",
        "RainToday",
        "RainTomorrow",
    ]

    for col in criticalCols:
        wantedCols.append(col)

    kDF = kDF[wantedCols]

    # Now we want to add some data.
    # We might want to try predict if it will rain in the next 7 days...
    # Or if it will rain in in the next week...
    # We add the columns below by iterating through the days
    # We check if it will rain the following day
    # NOTE!
    # This assumes that dates are uniform and we aren't missing any
    # days at all

    # We need the old index to proceed
    kDF = kDF.reset_index(drop=False)
    print(kDF)

    for i in range(0, len(kDF)):
        rain4day = False
        rain7day = False
        rain14day = False
        RainNextweek = False
        for j in range(1, 15):
            if i + j >= len(kDF):
                continue
            if kDF.loc[i + j, 'RainToday'] == 1.:
                if j < 5:
                    rain4day = True
                if j < 8:
                    rain7day = True
                if j < 15:
                    rain14day = True
                if j > 6 and j < 15:
                    RainNextweek = True
        if rain4day:
            kDF.loc[i, 'RainNext4days'] = 1.
        else:
            kDF.loc[i, 'RainNext4days'] = 0.
        if rain7day:
            kDF.loc[i, 'RainNext7days'] = 1.
        else:
            kDF.loc[i, 'RainNext7days'] = 0.
        if rain14day:
            kDF.loc[i, 'RainNext14days'] = 1.
        else:
            kDF.loc[i, 'RainNext14days'] = 0.
        if RainNextweek:
            kDF.loc[i, 'RainNextWeek'] = 1.
        else:
            kDF.loc[i, 'RainNextWeek'] = 0.

    # We'll also generate a report on this dataset.
    profile = ProfileReport(
        kDF, title='Cleaned Kaggle Data', explorative=True)
    profile.to_file("rawdata/cleanKaggle.html")

    # Finally, we'll save this cleaned dataset to a csv for later
    print("Saving cleaned data...")

    kDF.to_csv("rawdata/cleanAUSData.csv")
