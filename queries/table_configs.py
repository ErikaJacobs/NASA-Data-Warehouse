#%%

# Create table configurations

def table_configs(df_Dicts):
    import pandas as pd 
    
    table_configs = {}
    
    column_attributes = {  
        'activeRegionNum': 'text',
        'activityID': 'text',
        'allKpIndex': 'text', 
        'associatedCMEID': 'text', 
        'au': 'text', 
        'beginTime': 'text',
        'catalog': 'text', 
        'classType': 'text', 
        'cmeInputs': 'text', 
        'endTime': 'text', 
        'estimatedShockArrivalTime': 'text', 
        'estimatedDuration': 'text', 
        'eventTime': 'text', 
        'flrID': 'text', 
        'gstID': 'text', 
        'halfAngle': 'text', 
        'hssID': 'text', 
        'impactList': 'text', 
        'instruments': 'text', 
        'isEarthGB': 'text', 
        'isMostAccurate': 'text', 
        'kp_18': 'text', 
        'kp_90': 'text', 
        'kp_135': 'text', 
        'kp_180': 'text', 
        'KpAvg': 'text',
        'latitude': 'text', 
        'link': 'text', 
        'linkedEvents': 'text',
        'location': 'text',
        'longitude': 'text', 
        'modelCompletionTime': 'text',
        'mpcID': 'text', 
        'note': 'varchar(700)', 
        'peakTime': 'text', 
        'rbeID': 'text', 
        'rmin_re': 'text', 
        'sepID': 'text', 
        'simulationID': 'text', 
        'source': 'text',
        'sourceLocation': 'text', 
        'speed': 'text', 
        'startTime': 'text', 
        'time21_5': 'text', 
        'type': 'text'
        }
    
    api_list = list(df_Dicts.keys())
    
    for api in api_list:
        df = pd.DataFrame(df_Dicts[api])
        columns = list(df.columns)
    
        statement_details = []
        
        for column in columns:

            string = f'"{column}" {column_attributes[column]}'
            statement_details.append(string)
            
        statement = ', '.join(statement_details)
        
        table_configs[api] =  statement
    
    return table_configs

#%%