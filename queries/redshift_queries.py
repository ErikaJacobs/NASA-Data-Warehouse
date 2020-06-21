#%%

# Create All Redshift Queries

def redshift_queries(configs, table_configs):
        
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
    
    return queries

#%%