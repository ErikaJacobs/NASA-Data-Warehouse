# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 09:41:57 2020

@author: Erika
"""

def table_configs(df_Dicts):
    import pandas as pd 
    
    table_configs = {}
    
    column attributes = {  
        'activeRegionNum': 'nvarchar',
        'activityID': 'nvarchar',
        'allKpIndex': 'nvarchar', 
        'associatedCMEID': 'nvarchar', 
        'au': 'nvarchar', 
        'beginTime': 'nvarchar',
        'catalog': 'nvarchar', 
        'classType': 'nvarchar', 
        'cmeInputs': 'nvarchar', 
        'endTime': 'nvarchar', 
        'estimatedShockArrivalTime': 'nvarchar', 
        'estimatedDuration': 'nvarchar', 
        'eventTime', 'flrID': 'nvarchar', 
        'gstID', 'halfAngle': 'nvarchar', 
        'hssID', 'impactList': 'nvarchar', 
        'instruments': 'nvarchar', 
        'isEarthGB': 'nvarchar', 
        'isMostAccurate': 'nvarchar', 
        'kp_18': 'nvarchar', 
        'kp_90': 'nvarchar', 
        'kp_135': 'nvarchar', 
        'kp_180': 'nvarchar', 
        'KpAvg': 'nvarchar',
        'latitude': 'nvarchar', 
        'link': 'nvarchar', 
        'linkedEvents': 'nvarchar',
        'location': 'nvarchar',
        'longitude': 'nvarchar', 
        'modelCompletionTime': 'nvarchar',
        'mpcID': 'nvarchar', 
        'note': 'nvarchar', 
        'peakTime': 'nvarchar', 
        'rbeID': 'nvarchar', 
        'rmin_re': 'nvarchar', 
        'sepID': 'nvarchar', 
        'simulationID': 'nvarchar', 
        'source': 'nvarchar',
        'sourceLocation': 'nvarchar', 
        'speed': 'nvarchar', 
        'startTime': 'nvarchar', 
        'time21_5': 'nvarchar', 
        'type': 'nvarchar'
        }
    
    api_list = list(df_Dicts.keys())
    print(api_list)
    
    for api in api_list:
        df = pd.DataFrame(df_Dicts[api])
        columns = list(df.columns)
        print(columns) 
        
        table_configs[api] =  df
    
    

table_configs(df_Dicts)

#%%
def redshift_queries(configs, conn):
    print('blah')
    
api_list = ['CME','CMEAnalysis','HSS','WSAEnlilSimulations', 
    'GST', 'IPS', 'SEP', 'MPC', 'RBE','FLR']

for api in api_list:
    drop_query = '''DROP TABLE IF EXISTS {};'''.format('Blah')
    
    create_query = '''CREATE TABLE {} ({});'''.format(api, 'blah')
    
    copy_query = """
        copy {} 
        from 's3://erikatestbucket/NASA/{}'
        credentials 'aws_iam_role={}'
        CSV
        INGOREHEADER 1;""".format(api, 'blah', 'blah')
    
    