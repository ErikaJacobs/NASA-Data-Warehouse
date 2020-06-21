#%%
        
# Collect Redshift Cluster Endpoint
        
def endpoint(configs):
    
    from time import sleep
    from datetime import datetime
    from redshift_cluster import redshift_boto
    
    # Connect to Redshift
    
    redshift = redshift_boto.redshift_boto()
    
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
            
            # Get and vpc Into Configs
            endpoint = (response['Clusters'][0]['Endpoint']['Address'])
            configs['endpoint'] = endpoint
            vpcid = (response['Clusters'][0]['VpcId'])
            configs['vpcid']=vpcid
            print(f'Redshift endpoint collected at {datetime.now()}')
            
            break
            
        else:
            print(f'{response} Status Invalid')
            break

    return configs
            
#%%