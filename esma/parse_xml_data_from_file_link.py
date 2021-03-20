'''
    Script to: 
    1. identify first file link from the ESMA publication link
    2. download and extract XML file from zip file in the link 
       identified in Step 1
    3. parse zip file to extract data for specific attributes
    4. write the data extracted into a csv file 
    5. push the csv file to S3
    
    Usage:
    python parse_xml_data_from_file_link.py <output-file> <s3-bucket>
    
    Note: 
    1. The output file passed as argument will be created in 
       current working directory. 
    2. push_data_to_s3() has not been tested. 
    
'''


import zipfile
import re
import pandas as pd
import boto3
import argparse as ag
import xmltodict
import requests
import sys
import urllib.request

URL = 'https://registers.esma.europa.eu/solr/esma_registers_firds_files/select?q=*&fq=publication_date:%5B2021-01-17T00:00:00Z+TO+2021-01-19T23:59:59Z%5D&wt=xml&indent=true&start=0&rows=100'

def push_data_to_s3(local_file_name, bucket, s3_file_name):
    '''
    Function to push output file to s3 bucket. It is assumed 
    that the s3 bucket already exists and aws config has been 
    configured. 

    Note: This function has not been tested. 

    args:
    local_file_name(str): Local output file name
    bucket(str): S3 bucket name
    s3_file_name(str): Output file name in S3

    except:
    None

    returns:
    True/None: Returns True if file write was successful
               and None if unsuccessful 

    '''

    print("In function push_data_to_s3")
    try:
        s3_client = boto3.client('s3')
        s3_client.upload_file(
            local_file_name, bucket, s3_file_name)
    except:
        return None
       
    return True 

def parse_finattr_attrib(finattr):
    '''
    Function to parse out subtags from the tag
    <FinInstrmGnlAttrbts> and create list of texts from
    them.

    args:
    finattr(list): Text content present in each <FinInstrmGnlAttrbts>
                   tag

    except:
    None

    returns:
    finattr_parsed(list): List of lists where each sublist is the
                          parsed content of <FinInstrmGnlAttrbts> 
                          tag
    '''

    print("In function parse_finattr_attrib")

    finattr_parsed = []
    try:
        for val in finattr:
            try:
                attr_id = re.findall(r"<Id>(.*?)</Id>", val)[0]
            except:
                attr_id = 'n/a'

            try:
                full_name = re.findall(r"<FullNm>(.*?)</FullNm>", val)[0]
            except:
                full_name = 'n/a'

            try:
                class_fctn_tp = re.findall(
                    r"<ClssfctnTp>(.*?)</ClssfctnTp>", val)[0]
            except:
                class_fctn_tp = 'n/a'

            try:
                com_derived = re.findall(
                    r"<CmmdtyDerivInd>(.*?)</CmmdtyDerivInd>", val)[0]
            except:
                com_derived = 'n/a'

            try:
                nat_curr = re.findall(r"<NtnlCcy>(.*?)</NtnlCcy>", val)[0]
            except:
                nat_curr = 'n/a'

            finattr_parsed.append(
                [attr_id, full_name, class_fctn_tp, com_derived, nat_curr])
    except:
        return None
   
    print("Successfully cleaned and formatted all attribute groups from XML file")
    
    return finattr_parsed


def get_xml_text(fn):
    '''
    Function to get XML text from file

    args:
    fn(str): Name of file

    except:
    Exception to handle incorrect or errorenous 
    read of XML file from zip file

    returns:
    data(str): Text in XML format read from
               file
    len_data(int): Length of data returned

    '''
    print("In function get_xml_text()")

    try:
        zf = zipfile.ZipFile(fn, 'r')
        fn_comp = zf.namelist()[0]
        fn_p = zf.open(fn_comp)
        data = fn_p.read().decode('utf-8')
        len_data = len(data)
    except:
        return None, None

    print("Successfully read {}: , No. of characters : {}".format(fn, len_data))
    
    return data, len_data


def fetch_data_from_xml_text(data):
    '''
    Function to return final list of text content
    from <FinInstrmGnlAttrbts> and <Issr> tag

    args:
    data(str): XML data in text format

    except:
    None

    returns:
    final(list): List with contents from <FinInstrmGnlAttrbts>
                 and <Issr> tag
    len_final(int): Length of data list returned
    
    '''

    print("In function fetch_data_from_xml_text")
    
    try:
        finattr = re.findall(
            r"<FinInstrmGnlAttrbts>(.*?)</FinInstrmGnlAttrbts>", data)
        finattr_parsed = parse_finattr_attrib(finattr)
        issr = re.findall(r"<Issr>(.*?)</Issr>", data)
        final = [val1 + [val2] for val1, val2 in list(zip(finattr_parsed, issr))]
        len_final = len(final)
    except:
        return None, None

    print("No. of attribute group obtained from XML file : {}".format(len(final)))
    
    return final, len_final


def write_to_file(final, out_file):
    '''
    Function to write final data to output file

    args:
    final(list): List with final data to be written
                 to file
    out_file(str): Name of output file

    except:
    None

    returns:
    True/None: Returns True if file write was successful 
               and None if unsuccessful.

    '''
    
    print("In function write_to_file()")
    
    try:
        cols = ['FinInstrmGnlAttrbts.Id', 'FinInstrmGnlAttrbts.FullNm', 'FinInstrmGnlAttrbts.ClssfctnTp',
                'FinInstrmGnlAttrbts.CmmdtyDerivInd', 'FinInstrmGnlAttrbts.NtnlCcy', 'Issr']
        df = pd.DataFrame(final, columns=cols)
        df.to_csv(out_file, index=False)
        print("Output file {} written".format(out_file))
    except:
        return None
        
    return True

def get_file_url():
    '''
    Function to get file url of first file of type
    DLTINS

    args:
    None

    except:
    None

    returns:
    file_url(str): File url of first file of type DLTINS
    '''

    print("In function get_file_url()")

    response = requests.get(URL)
    data = xmltodict.parse(response.content)
    file_url = ''
    for item in data['response']['result']['doc']:
        file_type = [val['#text']
                     for val in item['str'] if val['@name'] == 'file_type'][0]
        if file_type == 'DLTINS':
            file_url = [val['#text'] for val in item['str']
                        if val['@name'] == 'download_link'][0]
            break

    print("File URL from seed link : {}".format(file_url))
    
    return file_url


def download_file(file_url):
    '''
    Function to download file from a file url

    args:
    file_url(str): Url of file to be downloaded

    except:
    Exception to deal with incorrect execution 
    of urlretrieve command

    returns:
    fn(str): Name of file download 
    '''

    print("In function download_file()")

    try:
        fn = file_url.split('/')[-1]
        urllib.request.urlretrieve(file_url, fn)
    except:
        return None

    print("Name of downloaded file : {}".format(fn))
    
    return fn

if __name__ == "__main__":
    parser = ag.ArgumentParser()
    parser.add_argument('outfile', help='Output file name', type=str)
    parser.add_argument('s3bucket', help='S3 bucket name', type=str)
    args = parser.parse_args()

    out_file = args.outfile
    bucket = args.s3bucket
    print("Output file : {}, S3 Bucket Name : {}".format(out_file, bucket))

    file_url = get_file_url()
    if file_url == '':
        print("File url does not exist. Please enter a different seed url")
        sys.exit(0)

    fn = download_file(file_url)
    if fn is None:
        print("Unable to download file from url: {}".format(file_url))
        sys.exit(0)

    data, len_data = get_xml_text(fn)
    if data is None:
        print("Unable to read XML file from zip file obtained from zip file: {}".format(fn))
        sys.exit(0)

    final, len_final = fetch_data_from_xml_text(data)
    if final is None:
        print("Error in cleaning data for file {}".format(fn))
        sys.exit(0)
    
    write_to_flag = write_to_file(final, out_file)
    if write_to_flag is None:
        print("Error in writing to file: {}".format(out_file))
        sys.exit(0)
         
    push_data_flag = push_data_to_s3(out_file, bucket, out_file)
    if push_data_flag is None:
        print("Unable to push output file {} to S3 bucket {}".format(
            local_file_name, bucket)) 
