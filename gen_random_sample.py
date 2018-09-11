'''
    Script to get a random sample from
    an array of integers

    Usage : python gen_random_script.py <list>
    Example : python gen_random_script.py 1,3,4,6,8,100,12,12,3,4
    Help : python gen_random_script.py -h
'''

import random
import argparse as ag

if __name__ == '__main__':
    parser = ag.ArgumentParser()
    parser.add_argument("listValue", help="Master list ( Enter in comma separated form) ", type=str)
    args = parser.parse_args()

    list_master = []
    list_master = args.listValue.split(",")
    size_master = len(list_master)

    size_rand = random.randint(1, size_master)
    ele_ind = random.sample(list_master, size_rand)
    list_rand = [ int(val) for val in ele_ind ]
    print(list_rand)
    
    
    


