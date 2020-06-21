#

# MAIB PROCEDURE FOR CONNECTING TO REDSHIFT CLUSTER

def run():

    from redshift_cluster import config as c1
    from redshift_cluster import iam as c2
    from redshift_cluster import create_cluster as c3
    from redshift_cluster import endpoint as c4
    from redshift_cluster import open_port as c5
    from redshift_cluster import redshift_connection as c6
    
    configs = c1.config()
    configs = c2.iam(configs)
    c3.create_cluster(configs)
    configs = c4.endpoint(configs)
    configs = c5.open_port(configs)
    conn = c6.redshift_connection(configs)

#%%