import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import datetime
import sys


def data_query():
    #import common ownership lot table as a dataframe
    df_COL = pd.read_csv('https://opendata.arcgis.com/datasets/1f6708b1f3774306bef2fa81e612a725_40.csv', usecols = ['SSL','ADDRESS1','ADDRESS2','CITYSTZIP','OWNERNAME','OWNNAME2','CAREOFNAME','PROPTYPE','PREMISEADD'], low_memory = True)

    #condo relate table has no unit num, create column to make concat easier
    df_COL['PREMISE_UNIT']=np.NaN

    #import condo relate table as a dataframe
    df_CRT = pd.read_csv('https://opendata.arcgis.com/datasets/f46a9917163d4cc8a892c05049983627_52.csv',usecols = ['UNITNUM','NAME','SSL','OWNERNAME','OWNNAME2','CAREOFNAME','ADDRESS1','ADDRESS2','CITYSTZIP'],low_memory=False)

    #create column with property type
    df_CRT['PROPTYPE']='CONDO'
    df_CRT.rename(columns={'NAME': 'PREMISEADD'}, inplace=True)

    df_CRT.rename(columns={'UNITNUM': 'PREMISE_UNIT'}, inplace=True)

    # reorder columns for concat
    df_CRT = df_CRT[['SSL', 'PROPTYPE', 'PREMISEADD', 'PREMISE_UNIT',  'OWNERNAME', 'OWNNAME2', 'CAREOFNAME', 'ADDRESS1', 'ADDRESS2', 'CITYSTZIP']]
    df_COL = df_COL[['SSL', 'PROPTYPE', 'PREMISEADD', 'PREMISE_UNIT', 'OWNERNAME', 'OWNNAME2', 'CAREOFNAME', 'ADDRESS1', 'ADDRESS2', 'CITYSTZIP']]

    #combine the two dataframes
    df_combined = pd.concat([df_COL, df_CRT], ignore_index=True)

    #make headings lower case for postgresql
    df_combined.columns = map(str.lower, df_combined.columns)

    #create full premise address column
    df_combined['fullpremise']= df_combined['premiseadd'] + ' ' + df_combined['premise_unit']

    #create engine to connect to database
    engine = create_engine('xxxxxxxxxxxxxxxxx', echo=False)

    #send to database
    df_combined.to_sql(name = 'address_owner_table', con = engine, if_exists = 'replace', index = True)
    #set primary key of database
    with engine.connect() as con:
        con.execute('ALTER TABLE address_owner_table ADD PRIMARY KEY (index);')

    #engine.execute("SELECT * FROM address_owner_table").fetchall()

    return

weekday = datetime.datetime.today().isoweekday()
# Sunday = 0 Saturday = 7
# If its sat or sun exit the program, else text
if weekday == 0:
    data_query()
else:
    sys.exit()
