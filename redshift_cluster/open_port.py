#%%
    
# Open Port for Redshift

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