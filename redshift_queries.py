# Create table configurations

def table_configs(df_Dicts):
    import pandas as pd 
    
    table_configs = {}
    
    column_attributes = {  
        'activeRegionNum': 'text',
        'activityID': 'text',
        'allKpIndex': 'text', 
        'associatedCMEID': 'text', 
        'au': 'text', 
        'beginTime': 'text',
        'catalog': 'text', 
        'classType': 'text', 
        'cmeInputs': 'text', 
        'endTime': 'text', 
        'estimatedShockArrivalTime': 'text', 
        'estimatedDuration': 'text', 
        'eventTime': 'text', 
        'flrID': 'text', 
        'gstID': 'text', 
        'halfAngle': 'text', 
        'hssID': 'text', 
        'impactList': 'text', 
        'instruments': 'text', 
        'isEarthGB': 'text', 
        'isMostAccurate': 'text', 
        'kp_18': 'text', 
        'kp_90': 'text', 
        'kp_135': 'text', 
        'kp_180': 'text', 
        'KpAvg': 'text',
        'latitude': 'text', 
        'link': 'text', 
        'linkedEvents': 'text',
        'location': 'text',
        'longitude': 'text', 
        'modelCompletionTime': 'text',
        'mpcID': 'text', 
        'note': 'varchar(700)', 
        'peakTime': 'text', 
        'rbeID': 'text', 
        'rmin_re': 'text', 
        'sepID': 'text', 
        'simulationID': 'text', 
        'source': 'text',
        'sourceLocation': 'text', 
        'speed': 'text', 
        'startTime': 'text', 
        'time21_5': 'text', 
        'type': 'text'
        }
    
    api_list = list(df_Dicts.keys())
    
    for api in api_list:
        df = pd.DataFrame(df_Dicts[api])
        columns = list(df.columns)
    
        statement_details = []
        
        for column in columns:

            string = f'"{column}" {column_attributes[column]}'
            statement_details.append(string)
            
        statement = ', '.join(statement_details)
        print('HERE IS A STATEMENT BELOW')
        print(statement)
        
        table_configs[api] =  statement
    
    return table_configs
    
table_configs = table_configs(df_Dicts)

#%%
def redshift_queries(configs, table_configs):
    print('blah')
    
api_list = ['CME','CMEAnalysis','HSS','WSAEnlilSimulations', 
    'GST', 'IPS', 'SEP', 'MPC', 'RBE','FLR']

drop_queries = []
create_queries = []
copy_queries = []

for api in api_list:
    drop_query = '''DROP TABLE IF EXISTS "{}";'''.format(api)
    
    create_query = '''CREATE TABLE "{}" ({});'''.format(api, table_configs[api])
    
    copy_query = """copy {}
    from 's3://erikatestbucket/NASA/{}.csv'
    credentials 'aws_iam_role={}'
    CSV
    delimiter '~' 
    IGNOREHEADER 1;""".format(api, api, configs['role_arn'])
    
    print('DROP QUERY')
    print(drop_query)
    print('CREATE QUERY')
    print(create_query)
    print('COPY QUERY')
    print(copy_query)
    
    drop_queries.append(drop_query)
    create_queries.append(create_query)
    copy_queries.append(copy_query)
    
queries = [drop_queries, create_queries, copy_queries]
      
#%%

def execute_queries(conn, queries):
    cur = conn.cursor()

    # Execute Drop Table Queries
    for query_set in queries:
        for query in query_set:
            try:
                print(query)
                cur.execute(query)
                conn.commit()
            except Exception as e:
                cur.execute('rollback;')
                print(e)
                break
            
execute_queries(conn, queries)

#%%

print()