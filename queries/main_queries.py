#%%

# CREATE AND EXECUTE QUERIES - MAIN PROCEDURE

from queries import table_configs as q1
from queries import redshift_queries as q2
from queries import execute_queries as q3

def run():
    table_configs = q1.table_configs(df_Dicts)
    queries = q2.redshift_queries(configs, table_configs)
    q3.execute_queries(conn, queries)

#%%