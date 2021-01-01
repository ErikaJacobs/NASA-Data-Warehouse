from modules.create_tables import Create_tables
from modules.redshift_connection import RedshiftConn
from modules.execute_queries import Execute_Queries
import datetime

def run():
    # Create Tables From API
    tbl = Create_tables()
    tbl.params_dict()
    tbl.get_api_data()
    tbl.nasa_dfs()
    print(f'S3 table creation completed at {datetime.datetime.now()}')
    
    # Create Redshift Connection
    rds = RedshiftConn()
    rds.iam()
    rds.create_cluster()
    rds.endpoint()
    rds.open_port()
    rds.redshift_connection()
    print(f'Redshift cluster running at {datetime.datetime.now()}')
    
    # Send Data to Redshift
    exe = Execute_Queries(tbl, rds)
    exe.table_conf()
    exe.redshift_queries()
    print(f'Data exported to Redshift at {datetime.datetime.now()}')
    
#%%