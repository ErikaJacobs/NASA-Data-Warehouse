#%%

# Delete Cluster

def delete():
    
    # Set Working Directory
    
    file =  'C:/Users/cluel/Documents/GitHub/NASA-Redshift'
    
    import os
    os.chdir(file)

    import boto3
    from redshift_cluster import redshift_boto as d1
    from redshift_cluster import config as d2

    iam = boto3.client('iam')
    redshift = d1.redshift_boto()

    # Bringing in Configs
    
    configs = d2.config()

    # Delete Cluster and IAM Role 
    try:
        redshift.delete_cluster(ClusterIdentifier=configs['clusteridentifier'], 
                            SkipFinalClusterSnapshot = True)
        print('Redshift cluster deleted!')
    except:
        print('ERROR: redshift.delete_cluster did not process')
        
    try:
        iam.detach_role_policy(
            RoleName = configs['rolename'], 
            PolicyArn = "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess")
        iam.delete_role(RoleName=configs['rolename'])
        print('IAM role deleted!')
    except:
        print('ERROR: iam.delete_role did not process')

delete()
    
#%%