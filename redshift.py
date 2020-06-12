#%%

# Import Configs

import configparser
Config = configparser.ConfigParser()
Config.read("C:/Users/cluel/Documents/GitHub/NASA-Redshift/config.ini")
Config.sections()

config_list = Config.options('Redshift')
configs = {}

for option in config_list:
    if option == 'numberofnodes':
        configs[f'{option}'] = int(Config.get('Redshift', option))
    else:
        configs[f'{option}'] = Config.get('Redshift', option)
    
print(configs)
    
#%%

# Connect to Redshift

import boto3
redshift = boto3.client('redshift')

# Get List of ClusterIdentifiers

cluster_list = redshift.describe_clusters()
cluster_list = cluster_list['Clusters']
cluster_ids = []

for i in range(len(cluster_list)):
    cluster_ids.append(cluster_list[i]['ClusterIdentifier'])

# Determine if Cluster is Created

if 'nasa-cluster' in cluster_ids:
    print('Cluster Already Exists')
else:
    redshift.create_cluster(
    DBName = configs['dbname'], 
    ClusterIdentifier = configs['clusteridentifier'],
    NodeType = configs['nodetype'],
    MasterUsername = configs['masterusername'],
    MasterUserPassword = configs['masteruserpassword'],
    NumberOfNodes = configs['numberofnodes'])

#%%
# Delete Cluster
redshift.delete_cluster(ClusterIdentifier='nasa-cluster', 
                        SkipFinalClusterSnapshot = True)


#%%