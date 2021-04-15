import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zerodha_assignment.settings')
import django
django.setup()
from zerodha_app.models import Item
from datetime import datetime,timedelta
import requests
from zipfile import ZipFile
from io import StringIO, BytesIO
import gzip
import csv
from django.core.cache import cache
import pandas as pd
import glob

def clean_folder():
    curr=os.getcwd()
    print("current path:",curr)
    save_path=curr+'\\temp_csv'
    print("temp path:",save_path)
    files = os.listdir(save_path)
    print(files)
    for f in files:
        filepath=save_path+'\\'+f
        print("file path:",f)
        os.chmod(filepath, 0o777)
        os.remove(filepath)


def get_url():
    url='https://www.bseindia.com/download/BhavCopy/Equity/EQ'
    date=datetime.today()-timedelta(1)
    date_str=date.strftime('%d%m%y')
    end='_CSV.ZIP'
    url_link=url+date_str+end
    print(url_link)
    return url_link

def get_filename():
    date=datetime.today()-timedelta(1)
    date_str=date.strftime('%d%m%y')
    end='.CSV'
    name='EQ'+date_str+end
    return name

def download_zip(url, chunk_size=128):
    curr=os.getcwd()
    print(curr)
    save_path=curr+'\\file.zip'
    hd = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers = hd, stream=True)
    print(r)
    with open(save_path, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            fd.write(chunk)

def get_csv():
    curr=os.getcwd()
    print(curr)
    save_path=curr+'\\temp_csv'
    with ZipFile('file.zip', 'r') as zipObj:
        zipObj.extractall(save_path)
       # listOfFileNames = zipObj.namelist()
       # print(listOfFileNames)
       # for fileName in listOfFileNames:
       #     if fileName.endswith('.csv'):
       #         print(fileName)
       #         zipObj.extract(fileName)
    print('Done!')

def populatedb():
    file_name=get_filename()
    path='temp_csv/'+file_name
    with open(path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                print(f'\tCode:{row[0]}  \tName:{row[1]} \topen:{row[4]} \thigh:{row[5]}')
                item=Item()
                item.code=row[0]
                item.name=row[1]
                item.open=row[4]
                item.high=row[5]
                item.low=row[6]
                item.close=row[7]
                line_count += 1
                item.save()


def populate_cache():
    print("populated cache")
    file_name=get_filename()
    path='temp_csv/'+file_name
    with open(path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                print('populating cache')
                date=datetime.today()
                date_str=date.strftime('%d%m%y')
                date_s=date.strftime('%d-%m-%y')
                row[1]=row[1].strip()
                key=row[1]+date_str
                cache.set(key, {

                             'name': row[1],
                             'code': row[0],
                             'date': date_s,
                             'open': row[4],
                             'high': row[5],
                             'low': row[6],
                             'close': row[7],
                        },timeout=None)
url=get_url()
download_zip(url)
clean_folder()
get_csv()
populatedb()
populate_cache()
