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
        if option == 'numberofnodes' or option == 'port':
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

def iam(configs):

# Create IAM role - append ARN to configs dict
        import boto3
        import json
        
        iam = boto3.client('iam')
        
        try:  
            iam.create_role(
                RoleName= configs['rolename'], 
                AssumeRolePolicyDocument=json.dumps(
                    {'Statement': [{'Action': 'sts:AssumeRole',
                                    'Effect': 'Allow',
                                    'Principal': {'Service': 'redshift.amazonaws.com'}}],
                     'Version': '2012-10-17'})
                )
            
            
            iam.attach_role_policy(RoleName=configs['rolename'], 
                                   PolicyArn="arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
                                   )['ResponseMetadata']['HTTPStatusCode']
            
            role_arn = iam.get_role(RoleName=configs['rolename'])['Role']['Arn']
            
            configs['role_arn']=role_arn
        
        except:
            role_arn = iam.get_role(RoleName=configs['rolename'])['Role']['Arn']
            configs['role_arn']=role_arn       
        
        return configs
        
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
    
# Open Port

def open_port(configs):
    
    import boto3
    
    try:
        ec2 = boto3.resource('ec2')
        
        vpc = ec2.Vpc(id=configs['vpcid'])
        sec_group = list(vpc.security_groups.all())[0]
        sec_group.authorize_ingress(GroupName=sec_group.group_name,
                                    CidrIp='0.0.0.0/0',
                                    IpProtocol='TCP',
                                    FromPort=configs['port'],
                                    ToPort=configs['port']
                                    )
        
        print('Port Opened')
    except:
        print('Port Already Opened')
    return configs

#%%

# Connect To Redshift

def redshift_connection(configs):

    import psycopg2
    
    try:
        conn = psycopg2.connect(
            dbname = configs['dbname'],
            host = configs['endpoint'],
            port = configs['port'],
            user = configs['masterusername'],
            password = configs['masteruserpassword'])
        print('Success! Redshift connected.')
    except:
        print('ERROR: Connection not successful')
        
    return conn

#%%

# Procedure

configs = config()
configs = iam(configs)
create_cluster(configs)
configs = endpoint(configs)
configs = open_port(configs)
conn = redshift_connection(configs)

#%%
# Delete Cluster
def delete(configs):
    import boto3
    
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