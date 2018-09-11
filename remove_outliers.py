'''
    Script to remove outliers from a series and print
    output on console

    Usage : python remove_outliers.py <series>
    Help  : python remove_outliers.py -h
'''


import pandas as pd
import re
import argparse as ag

if __name__ == "__main__":
    parser = ag.ArgumentParser()
    parser.add_argument('series', help='Enter values seperated by comma', type=str)
    args = parser.parse_args()

    values = args.series
    list_values = [ int(val) for val in values.split(",") ]

    ds = pd.Series(list_values)
    mean = ds.mean()
    std = ds.std()
    ds = ds[(ds>(mean-(2*std))) & (ds<(mean+(2*std)))]
    print("With outliers : {}".format(list_values))
    print("Without outliers : {}".format(ds.tolist()))
