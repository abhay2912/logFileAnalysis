#!/usr/bin/env python
# coding: utf-8

# In[5]:


import pandas as pd
pd.options.display.max_columns = None
import re
import os
import time
from tqdm import tqdm
import opendatasets as od
import xlsxwriter
import openpyxl
# from dataset_utilities import value_counts_plus

# for dirname, _, filenames in os.walk('C:\\Users\\user\\Documents\\LogfileJuypter\\regressionTree'):
#     for filename in filenames:
#         print(os.path.join(dirname, filename))


# In[6]:


# There is a minor bug in this regex, it misses the last field. I'll fix this soon. 

common_regex = '^(?P<ip>\S+) \S+ (?P<userid>\S+) \[(?P<datetime>[^\]]+)\] "(?P<method>[A-Z]+) (?P<request>[^ "]+)? HTTP/[0-9.]+" (?P<status>[0-9]{3}) (?P<size>[0-9]+|-)'
combined_regex = '^(?P<ip>\S+) \S+ (?P<userid>\S+) \[(?P<datetime>[^\]]+)\] "(?P<method>[A-Z]+) (?P<request>[^ "]+)? HTTP/[0-9.]+" (?P<status>[0-9]{3}) (?P<size>[0-9]+|-) "(?P<referrer>[^"]*)" "(?P<browser>[^"]*)'
columns = ['ip', 'userid', 'datetime', 'method', 'request', 'status', 'size', 'referer', 'browser']


# In[7]:

# print("running the scrip")

def logs_to_df(logfile, output_dir, errors_file):
    print("inside")
    with open(logfile) as source_file:
        linenumber = 0
        parsed_lines = []
        for line in tqdm(source_file):
            try:
                log_line = re.findall(combined_regex, line)[0]
                parsed_lines.append(log_line)
            except Exception as e:
                with open(errors_file, 'at') as errfile:
                    print((line, str(e)), file=errfile)
                continue
            linenumber += 1
            if linenumber % 250_000 == 0:
                df = pd.DataFrame(parsed_lines, columns=columns)
                df.to_parquet(f'{output_dir}/file_{linenumber}.parquet')
                parsed_lines.clear()
        else:
            df = pd.DataFrame(parsed_lines, columns=columns)
            df.to_parquet(f'{output_dir}/file_{linenumber}.parquet')
            parsed_lines.clear()


# In[9]:

# arrtoex = pd.DataFrame()
# %%time
def logs2df():
    logs_to_df(logfile=r'C:\\Users\\user\\Documents\\LogfileJuypter\\regressionTree\\templates\\uploads\\access10.log', output_dir=r'C:\\Users\\user\\Documents\\LogfileJuypter\\regressionTree\\output\\parquet_dir', errors_file=r'C:\\Users\\user\\Documents\\LogfileJuypter\\regressionTree\\output\\error.txt')
    # In[10]:
    # %%time 
    logs_df = pd.read_parquet(r'C:\\Users\\user\\Documents\\LogfileJuypter\\regressionTree\\output\\parquet_dir')
    # %rm -r r'C:\\Users\\user\\Documents\\LogfileJuypter\\regressionTree\\output\\parquet_dir\\'
    # logs_df.info(show_counts=True, verbose=True)
    # In[11]:
    logs_df['ip'] = logs_df['ip'].astype('category')
    del logs_df['userid']
    logs_df['datetime'] = pd.to_datetime(logs_df['datetime'], format='%d/%b/%Y:%H:%M:%S %z')
    logs_df['method'] = logs_df['method'].astype('category')
    logs_df['status'] = logs_df['status'].astype('int16')
    logs_df['size'] = logs_df['size'].astype('int32')
    logs_df['referer'] = logs_df['referer'].astype('category')
    logs_df['browser'] = logs_df['browser'].astype('category')
    # In[12]:
    # %%time 
    logs_df.to_parquet('logs_df.parquet')
    # In[13]:
    # %%time 
    logs_df = pd.read_parquet('logs_df.parquet')
    # In[14]:
    return logs_df
    # arrtoex = pd.DataFrame(logs_df).T
   


# In[16]:


# colarr = ['ip', 'datetime', 'method', 'request', 'status', 'size', 'referer', 'browser']
# import xlsxwriter
# workbook = xlsxwriter.Workbook(r'C:\\Users\\user\\Documents\\LogfileJuypter\\regressionTree\\output\\CSVlogshort.xlsx')
# worksheet = workbook.add_worksheet()
# for i in range(0,8):
#      worksheet.write(0,i,str(colarr[i]))
# workbook.close()


# In[17]:
def creat_xlsx():
    logs_df = logs2df()
    ArrtoExSliced = logs_df.iloc[:10000,0:]
    # ArrtoExSliced.to_excel(excel_writer = r"C:\Users\jayes\OneDrive\Desktop\CSV and Datasets\Output\convaccess.xlsx\\")
    # ArrtoExSliced
    # In[15]:
    arrtoex = pd.DataFrame(ArrtoExSliced).T
    import xlsxwriter
    workbook = xlsxwriter.Workbook(r'C:\\Users\\user\\Documents\\LogfileJuypter\\regressionTree\\output\\CSVlogshort.xlsx')
    row = 0
    colarr = ['ip', 'datetime', 'method', 'request', 'status', 'size', 'referer', 'browser']
    worksheet = workbook.add_worksheet()
    for i in range(0,8):
        worksheet.write(0,i,str(colarr[i]))
    for i in range(1,len(ArrtoExSliced)):
        for j in range(0,8):
            worksheet.write(i,j,str(arrtoex[i][j]))
    workbook.close()
    return "C:\\Users\\user\\Documents\\LogfileJuypter\\regressionTree\\output\\"

    # In[18]:

def excelToCsv(fileName):
    # dff = pd.read_csv('C:\\Users\\user\\Documents\\LogfileJuypter\\regressionTree\\output\\CSVlogshort.csv')
    
    read_file = pd.DataFrame(pd.read_excel("output\\CSVlogshort.xlsx"))

    read_file.to_csv ("C:\\Users\\user\\Documents\\LogfileJuypter\\regressionTree\\prediction\\{}.csv".format(fileName), 
                    index = None,
                    header=True)

    df = pd.DataFrame(pd.read_csv("C:\\Users\\user\\Documents\\LogfileJuypter\\regressionTree\\prediction\\{}.csv".format(fileName)))
    return df