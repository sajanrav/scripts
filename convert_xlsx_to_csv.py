'''
    Script to read an XLSX file with single sheet
    and convert into CSV

    Usage: python convert_xlsx_to_csv.py <xlsx file> <csv file>
    Help : python convert_xlsx_to_csv.py -h

'''

import pandas as pd
import csv
import argparse as ag

if __name__ == '__main__':
    parser = ag.ArgumentParser()
    parser.add_argument('inputfile', help='Input xlsx file', type=str)
    parser.add_argument('outputfile', help='Output csv file', type=str)
    args = parser.parse_args()
    
    xlsx_name = args.inputfile
    csv_name = args.outputfile
    df = pd.read_excel(xlsx_name, sheet=None)
    df.to_csv(csv_name, index=None, quoting=csv.QUOTE_ALL)
