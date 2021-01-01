#%%
from modules.redshift_connection import RedshiftConn

# Delete Cluster

def delete():
    rds = RedshiftConn()
    rds.delete()

delete()
#%%