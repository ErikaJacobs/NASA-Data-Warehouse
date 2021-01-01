import configparser
import os
import boto3
import json
from time import sleep
from datetime import datetime
import psycopg2

class RedshiftConn:
    
    def __init__(self):
        self.path = os.path.dirname(os.path.realpath(__file__)).replace('modules', '')
        Config = configparser.ConfigParser()
        Config.read(self.path + '/config.ini')
        Config.sections()
        
        config_list = Config.options('Redshift')
        self.configs = {}
        
        # Create Dictionary of Configurations
        
        for option in config_list:
            if option == 'numberofnodes' or option == 'port':
                self.configs[f'{option}'] = int(Config.get('Redshift', option))
            else:
                self.configs[f'{option}'] = Config.get('Redshift', option)
                
    def iam(self):
            configs = self.configs
            
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
            
            except Exception as e:
                print(e)
                role_arn = iam.get_role(RoleName=configs['rolename'])['Role']['Arn']
                configs['role_arn']=role_arn       
            
            return configs
    
    def create_cluster(self):
        # Connect to Redshift via Boto3
        redshift = boto3.client('redshift')
        
        # Get List of ClusterIdentifiers
        cluster_list = redshift.describe_clusters()
        cluster_list = cluster_list['Clusters']
        cluster_ids = []
        
        # Bring In Configs
        configs = self.configs
        
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
                
    def endpoint(self):
        configs = self.configs
        
        # Connect to Redshift
        
        redshift = boto3.client('redshift')
        
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

    # Open Port
    def open_port(self):
        
        configs = self.configs
        
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
    
    # Connect To Redshift
    def redshift_connection(self):
        
        configs = self.configs
        
        try:
            self.conn = psycopg2.connect(
                dbname = configs['dbname'],
                host = configs['endpoint'],
                port = configs['port'],
                user = configs['masterusername'],
                password = configs['masteruserpassword'])
            print('Success! Redshift connected.')
        except Exception as e:
            print('ERROR: Connection not successful')
            print(e)
            exit()

    def delete(self):
        iam = boto3.client('iam')
        redshift = boto3.client('redshift')
    
        # Bringing in Configs
        configs = self.configs
    
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