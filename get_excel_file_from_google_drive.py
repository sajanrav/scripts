'''
   Script to download Excel file from Google Drive
   and write to CSV file. Each sheet in the Excel
   file will be written into individual CSV files.

   Before running the script, the necessary permissions
   need to granted on Google Drive so that the script
   could create a connection object and download the
   file.

'''

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from xlrd import open_workbook
import sys
import argparse as ag
import csv


def createConnection():
    '''
    Function to create a Google drive connection
    object

    args:
    None

    except:
    None

    returns:
    gDriveConn(object): Google Drive connection object

    '''

    gAuth = GoogleAuth()
    gAuth.LocalWebserverAuth()
    gDriveConn = GoogleDrive(gAuth)
    print("Created Google Drive Service")

    return gDriveConn


def downloadExcel(conn, fileToDownload, downloadedFile):
    '''
    Function to download Excel (xlsx) file from
    Google Drive to local machine

    args:
    conn(object): Google Drive connection object
    fileToDownload(str): File to download
    downloadedFile(str): Output File

    except:
    None

    returns:
    None

    '''

    fileList = conn.ListFile().GetList()

    for fileN in fileList:
        if fileN['title'] == fileToDownload and fileN['labels']['trashed'] == False:
            id_file = fileN['id']

            outputFile = conn.CreateFile({'id': id_file})
            outputFile['downloadUrl'] = fileN['exportLinks'][
                'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']
            outputFile.GetContentFile(downloadedFile)
            break

    print("Downloaded Excel File")


def writeExcelToCSV(downloadedFile):
    '''
    Function to write downloaded Excel (xlsx) file
    to CSV file. Each sheet in the downloaded file
    will be written into a seperate CSV file

    args:
    downloadedFile(str): Downloaded Excel (xlsx) file

    except:
    None

    returns:
    None

    '''

    print("Begin Converting Excel File to CSV")

    wbObj = open_workbook(downloadedFile)

    for sheetObj in wbObj.sheets():
        header = []

        with open('./data/' + sheetObj.name + '.csv', 'wbObj') as csvfile:
            wr = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
            for rownum in xrange(sheetObj.nrows):
                wr.writerow([unicode(val).encode('utf8')
                             for val in sheetObj.row_values(rownum)])

    print("Completed pushing data to CSV")

if __name__ == '__main__':
    parser = ag.ArgumentParser()
    parser.add_argument(
        "filename", help="Excel File to be downloaded from Google Drive", type=str)
    args = parser.parse_args()
    fileToDownload = args.filename

    if fileToDownload[-5:] == ".xlsx":
        downloadedFile = fileToDownload
    else:
        downloadedFile = fileToDownload + ".xlsx"

    conn = createConnection()
    downloadExcel(conn, fileToDownload, downloadedFile)
    writeExcelToCSV(downloadedFile)
