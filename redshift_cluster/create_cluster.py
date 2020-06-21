#%%
    
# Create Redshift Cluster

from redshift_cluster import redshift_boto

def create_cluster(configs):
    # Connect to Redshift via Boto3
    
    redshift = redshift_boto.redshift_boto()
    
    # Get List of ClusterIdentifiers
    
    cluster_list = redshift.describe_clusters()
    cluster_list = cluster_list['Clusters']
    cluster_ids = []
    
    for i in range(len(cluster_list)):
        cluster_ids.append(cluster_list[i]['ClusterIdentifier'])
    
    # Determine if Cluster is Created
    
    if 'nasa-cluster' in cluster_ids:
        print('Cluster Already Created')
    else:
        print('Creating cluster...')
        redshift.create_cluster(
        DBName = configs['dbname'], 
        ClusterIdentifier = configs['clusteridentifier'],
        NodeType = configs['nodetype'],
        MasterUsername = configs['masterusername'],
        MasterUserPassword = configs['masteruserpassword'],
        NumberOfNodes = configs['numberofnodes'],
        IamRoles=[configs['role_arn']])
        
#%%