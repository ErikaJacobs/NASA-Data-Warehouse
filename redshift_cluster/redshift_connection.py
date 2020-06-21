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
