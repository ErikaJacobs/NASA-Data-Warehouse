#%%

# S3 TABLE CREATION - MAIN FILE
 
def run(api_key):
    
    # Import Packages
    
    from create_tables import params_dict as m1
    from create_tables import get_api_data as m2
    from create_tables import nasa_dfs as m3 
    
    from redshift_cluster import config as c1
    from redshift_cluster import iam as c2
    from redshift_cluster import create_cluster as c3
    from redshift_cluster import endpoint as c4
    from redshift_cluster import open_port as c5
    from redshift_cluster import redshift_connection as c6
    
    from queries import table_configs as q1
    from queries import redshift_queries as q2
    from queries import execute_queries as q3 
    
    from datetime import datetime
    
    # Procedure
    
    # Create Tables
    print(f'S3 table creation started at {datetime.now()}')
    ParamsDict = m1.params_dict(api_key)
    responseDict = m2.get_api_data(ParamsDict)
    df_Dicts = m3.nasa_dfs(responseDict)
    print(f'S3 table creation completed at {datetime.now()}')
    

    # Create Redshift Connection
    configs = c1.config()
    configs = c2.iam(configs)
    c3.create_cluster(configs)
    configs = c4.endpoint(configs)
    configs = c5.open_port(configs)
    conn = c6.redshift_connection(configs)
    
    # Create and Execute Queries
    table_configs = q1.table_configs(df_Dicts)
    queries = q2.redshift_queries(configs, table_configs)
    q3.execute_queries(conn, queries)

#%%