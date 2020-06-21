#%%

# Create IAM role - append ARN to configs dict

def iam(configs):

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