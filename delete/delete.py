#%%

# Delete Cluster

def delete(configs):
    import boto3
    from redshift_cluster import redshift_boto

    iam = boto3.client('iam')
    redshift = redshift_boto()

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

delete(configs)
    
#%%