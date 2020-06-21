#%%

# Connect to Redshift via boto3

def redshift_boto():
    import boto3
    
    redshift = boto3.client('redshift')
    return redshift

#%%