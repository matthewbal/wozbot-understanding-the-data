#########################
# clean-data.py
# Author: Matt Balshaw
##########################
# After analysis, clean the data
#########################

import pandas as pd

if __name__ == "__main__":

    #####
    # Read the Kaggle Data Frame in with pandas
    kagglePath = "rawdata/weatherAUS.csv"
    kDF = pd.read_csv(kagglePath, parse_dates=["Date"])
