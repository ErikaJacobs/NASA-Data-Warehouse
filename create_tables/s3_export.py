#%%
    
## Export df to S3

def s3_export(df, name):

    import boto3
    from io import StringIO

    path = f'NASA/{name}.csv'
        
    s3 = boto3.resource('s3')
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index = False, sep="~")
    s3.Object('erikatestbucket', path).put(Body=csv_buffer.getvalue())
    
#%%