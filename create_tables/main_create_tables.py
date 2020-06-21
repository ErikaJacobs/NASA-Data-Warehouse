#%%

# S3 TABLE CREATION - MAIN FILE
 
def main_create_tables():
    
    # Inputs
    
    api_key = 'oXd16S7iyStpHG1br0c1yTq9B5kFftCoqx9lfUoE'
    
    from create_tables import params_dict as m1
    from create_tables import get_api_data as m2
    from create_tables import nasa_dfs as m3
    
    from datetime import datetime
    
    # Procedure
    
    print(f'S3 table creation started at {datetime.now()}')
    ParamsDict = m1.params_dict(api_key)
    responseDict = m2.get_api_data(ParamsDict)
    df_Dicts = m3.nasa_dfs(responseDict)
    print(f'S3 table creation completed at {datetime.now()}')

#%%
