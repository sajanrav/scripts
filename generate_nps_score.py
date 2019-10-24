'''
    Script to generate NPS score. In case the function
    generate_nps_score() is to be used as a separate
    module, please remove the main() function.

    The input file should have two columns:
    1. id
    2. nps score

    Definitions:
    1. A valid nps score is an integer in the range 0 - 10
    2. Promotor : nps = 9 or 10
    3. Passive : nps = 7 or 8
    4. Detractor : nps = 0 - 6

    NPS = % of promoters - % of detractors
    
    Usage of generate_nps_score():
    Syntax : generate_nps_score(file_name)
    
    Eg. 
        1. nps, e_status = generate_nps_score('test.txt')
    
        2. file_name = 'test.txt'
           nps, e_status = generate_nps_score(file_name)

'''


import pandas as pd
import numpy as np
import argparse as ag

errors = {
          'NO_ERROR': "No error in data or program execution",
          'BAD_FILE': "Bad file or empty file provided as input file",
          'NO_VALID_DATA_AVAILABLE': "No valid data after checks for invalid data"
         }

def generate_nps_score(file_name):
    '''
    Function to generate NPS (Net Promoter Score)
    
    Args:
    file_name(str): Name of Input File
    
    Raises:
    None
    
    Returns:
    nps(float): NPS Score rounded to two decimal
                places
    e_status(str): Error status
    
    '''

    types = {'record_id':'str', 'nps':'str'}

    try:
        test = pd.read_csv(file_name, dtype=types)
    except:
        e_status = 'BAD_FILE'
        return "n/a", e_status

    test['record_id'] = test['record_id'].str.strip()
    test['nps'] = test['nps'].str.strip()
    test = test[(test['nps'].str.isdigit()) & (test['record_id'] != "None") & (test['record_id'] != "")].dropna(axis=0, how='any').reset_index(drop=True)
    test['nps'] = test['nps'].astype(int)
    test = test[(test['nps'] >= 0) & (test['nps'] <= 10)].reset_index(drop=True)
    test['type'] = np.where(((test['nps'] == 9) | (test['nps'] == 10)),'promoter', 
                            np.where(((test['nps'] == 7)|(test['nps'] == 8)),'passive', 'detractor'))

    if test.shape[0] == 0:
        e_status = 'NO_VALID_DATA_AVAILABLE'
        return 'n/a', e_status
    else:
        type_counts = test.groupby(['type'])['record_id'].count()
        print(type_counts)
        nps = (((type_counts['promoter'] / test.shape[0]) - (type_counts['detractor'] / test.shape[0])) * 100).round(2)
        e_status = 'NO_ERROR'
        return nps, e_status


if __name__ == "__main__":
    parser = ag.ArgumentParser()
    parser.add_argument('inputfile', help='Name of input file', type=str)
    args = parser.parse_args()
    
    input_file = args.inputfile
    nps, error_val = generate_nps_score(input_file)

    if error_val == 'NO_ERROR':
        print("NPS Score for data in {} : {}".format(input_file, nps))
    else:
        print(errors[error_val])

