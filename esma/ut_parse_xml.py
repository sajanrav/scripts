'''
    Unit test cases for testing functions of
    parse_xml_data_from_file_link.py script. 
    
    Note: The function to push output file to S3 
    has not been tested. 
    
    usage: python ut_parse_xml.py 
    
'''

import unittest
import parse_xml_data_from_file_link as parse_xml
from random import choice

def get_test_data():
    '''
    Function to generate a random set of test parameters
    
    args:
    None
    
    except:
    None
    
    returns:
    test_chosen(list): Test parameter chosen
    
    '''
    
    test_data = [['http://firds.esma.europa.eu/firds/DLTINS_20210117_01of01.zip', 'DLTINS_20210117_01of01.zip', 143275125, 141381, True, True],
                 ['', None, None, None, None, None]]
    index_arr = list(range(len(test_data)))
    index_chosen = choice(index_arr)
    test_chosen = test_data[1] 
    
    return test_chosen
    
class Testing(unittest.TestCase):
    '''
    Unit testing class definition
    
    '''
    
    file_url            = parse_xml.get_file_url()
    fn                  = parse_xml.download_file(file_url)
    data, len_data      = parse_xml.get_xml_text(fn)
    final, len_final    = parse_xml.fetch_data_from_xml_text(data)
    write_flag          = parse_xml.write_to_file(final, 'ut_output_file.csv')
    push_data_flag      = parse_xml.push_data_to_s3('ut_output_file.csv', 's3-test', 'ut_output_file.csv')
      
    test_data = get_test_data()
    ut_file_url       = test_data[0]
    ut_fn             = test_data[1]
    ut_len_data       = test_data[2]
    ut_len_final      = test_data[3] 
    ut_write_flag     = test_data[4]
    ut_push_data_flag = test_data[5]
        
    print("Setting up test values\n-------------------------")
    print("UT File Url : {}".format(ut_file_url))
    print("UT File Name : {}".format(ut_fn))
    print("UT Length of file data : {}".format(ut_len_data))
    print("UT No. of attribute sets : {}".format(ut_len_final))
    print("UT Write flag : {}".format(ut_write_flag))
    print("UT S3 Push flag : {}".format(ut_push_data_flag))
    
    def test_func_get_file_url(self):
        '''
        Function to test get_file_url()
        
        '''
        
        self.assertEqual(self.file_url, self.ut_file_url)

    def test_func_download_file(self):
        '''
        Function to test download_file()
        
        '''
        
        self.assertEqual(self.fn, self.ut_fn)

    def test_func_get_xml_text(self):
        '''
        Function to test get_xml_text()
        
        '''
        
        self.assertEqual(self.len_data, self.ut_len_data)

    def test_func_fetch_data_from_xml_text(self):
        '''
        Function to test fetch_data_from_xml_text()
        
        '''
        
        self.assertEqual(self.len_final, self.ut_len_final)
        
    def test_func_write_to_file(self):
        '''
        Function to test write_to_file()
        
        '''
        
        self.assertEqual(self.write_flag, self.ut_write_flag)
    
    def test_func_push_data_to_s3(self):
        '''
        Function to test push_data_to_s3()
        
        '''
        
        self.assertEqual(self.push_data_flag, self.ut_push_data_flag)
        

if __name__ == '__main__':
    unittest.main()
    