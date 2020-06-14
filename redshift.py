#%%

# Import Configs

def config():

    import configparser
    
    Config = configparser.ConfigParser()
    Config.read("C:/Users/cluel/Documents/GitHub/NASA-Redshift/config.ini")
    Config.sections()
    
    config_list = Config.options('Redshift')
    configs = {}
    
    # Create Dictionary of Configurations
    
    for option in config_list:
        if option == 'numberofnodes':
            configs[f'{option}'] = int(Config.get('Redshift', option))
        else:
            configs[f'{option}'] = Config.get('Redshift', option)
    return configs
    
#%% Connect to Redshift via Boto3
    
def redshift_boto():
    import boto3
    
    redshift = boto3.client('redshift')
    return redshift
    
#%%
    
# Create Redshift Cluster

def create_cluster(configs):
    # Connect to Redshift via Boto3
    
    redshift = redshift_boto()
    
    # Get List of ClusterIdentifiers
    
    cluster_list = redshift.describe_clusters()
    cluster_list = cluster_list['Clusters']
    cluster_ids = []
    
    for i in range(len(cluster_list)):
        cluster_ids.append(cluster_list[i]['ClusterIdentifier'])
    
    # Determine if Cluster is Created
    
    if 'nasa-cluster' in cluster_ids:
        print('Cluster Created')
    else:
        redshift.create_cluster(
        DBName = configs['dbname'], 
        ClusterIdentifier = configs['clusteridentifier'],
        NodeType = configs['nodetype'],
        MasterUsername = configs['masterusername'],
        MasterUserPassword = configs['masteruserpassword'],
        NumberOfNodes = configs['numberofnodes'])
    
#%%
        
# Collect Redshift Cluster Endpoint
        
def endpoint(configs):
    
    from time import sleep
    from datetime import datetime
    
    # Connect to Redshift
    
    redshift = redshift_boto()
    
    num_retries = 20

    for x in range(0, num_retries):
        if x == 0:
            print(f'Collecting Redshift endpoint at {datetime.now()}')
        
        try:
            endpoint = 'N/A'
            response = dict(redshift.describe_clusters(ClusterIdentifier = configs['clusteridentifier']))
        except:
            print('ERROR: Redshift cluster does not exist')
            break
        
        if response['Clusters'][0]['ClusterStatus'] == 'deleting':
            print('ERROR: Redshift cluster is being deleted')
            break
        
        if response['Clusters'][0]['ClusterStatus'] == 'creating':
            print('ERROR: Redshift cluster is being created - Recollect endpoint in 30 seconds')
            sleep(30)
            print(f'Retrying Redshift endpoint collection at {datetime.now()}')
            continue
        
        if response['Clusters'][0]['ClusterStatus'] == 'available':
            endpoint = (response['Clusters'][0]['Endpoint']['Address'])
            configs['endpoint'] = endpoint
            print(f'Redshift endpoint collected at {datetime.now()}')
            break
            
        else:
            print(f'{response} Status Invalid')
            sleep(30)

    return configs
            
#%%

# Connect To Redshift

import psycopg2

configs.keys()

#%%

conn_string="postgresql://{}:{}@{}:{}/{}".format(
    configs['masterusername'],
    configs['masteruserpassword'],
    configs['endpoint'],
    configs['port'],
    configs['dbname'])

conn = psycopg2.connect(conn_string)
#%%
try:
    conn = psycopg2.connect(
        dbname = configs['dbname'],
        host = configs['endpoint'],
        port = configs['port'],
        user = configs['masterusername'],
        password = configs['masteruserpassword'])
except:
    print('THIS DID NOT WORK')

#print(AWS_SECRET_KEY)
#%%

# Procedure

configs = config()
create_cluster(configs)
configs = endpoint(configs)

#%%
# Delete Cluster
def delete():
    redshift = redshift_boto()

    redshift.delete_cluster(ClusterIdentifier='nasa-cluster', 
                            SkipFinalClusterSnapshot = True)

delete()
    
#%%