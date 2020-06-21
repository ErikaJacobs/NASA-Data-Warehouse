#%%

# CREATE AND EXECUTE QUERIES - MAIN PROCEDURE

def main_queries():
    table_configs = table_configs(df_Dicts)
    queries = redshift_queries(configs, table_configs)
    execute_queries(conn, queries)

#%%