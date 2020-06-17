# NASA Redshift - Data Warehouse Project

#%%
def params_dict(api_key):
    
    # Import Packages - Set Dates
    import datetime
    from dateutil.relativedelta import relativedelta
    
    ParamsDict=dict()
    now = str(datetime.datetime.now().date())
    then = str(datetime.datetime.now().date() - relativedelta(years=5))
    
    # application/json;charset=UTF-8
    paramsjson = {
          'api_key':api_key,
          'startDate':then,
          'endDate':now
          }
    
    # text/plain; charset=UTF-8
    paramstext = {
          'api_key':api_key,
          'startDate':then,
          'endDate':now,
          'feedtype':'json'
          }
    
    # Append to Dict
    
    textlist = ['GST', 'IPS', 'SEP', 'MPC', 'RBE', 'FLR']
    jsonlist = ['CME', 'CMEAnalysis', 'HSS', 'WSAEnlilSimulations']
    
    for item in textlist:
        ParamsDict[item]=paramstext
    
    for item in jsonlist:
        ParamsDict[item]=paramsjson
    
    return ParamsDict

#%%

#DONKI REQUESTS
    
def get_api_data(ParamsDict):
    import requests
    
    responseDict = {}
    
    api_list = ['CME','CMEAnalysis','HSS','WSAEnlilSimulations', 
    'GST', 'IPS', 'SEP', 'MPC', 'RBE','FLR']
    
    def donki_json(API, ParamsDict):
      url = f"https://api.nasa.gov/DONKI/{API}"
      params = ParamsDict[API]
      r = requests.get(url,params=params)
      r.encoding = 'utf-8'
      #print(r.status_code)
      #print(r.headers.get('Content-Type'))
      #print(r.encoding)
      #print(limit_remaining)
      
      try:
          response = r.json()
    
      except:
          print(f"{API} was not successfully requested.")
          response = 'N/A'
      
      responseDict[API] = response
    
    for API in api_list:
        donki_json(API, ParamsDict)
    
    return responseDict

#%%

# One Combined User-Defined Function to create ALL tables

def nasa_dfs(responseDict):
    import pandas as pd

    nasa_api = ['CME','CMEAnalysis','HSS','WSAEnlilSimulations', 
    'GST', 'IPS', 'SEP', 'MPC', 'RBE','FLR']

    df_Dicts = {}

    for api in nasa_api:

        # Set-Up
        api_list = responseDict[f'{api}']
        columnDict = {}
        df_Dicts = {}
        df_Dicts[f'{api}'] = columnDict

        # Extract Data from Dictionary
        api_range = list(range(len(api_list)))

        columns = ['activeRegionNum', 'activityID', 'allKpIndex', 'associatedCMEID', 'au', 'beginTime',
        'catalog', 'classType', 'cmeInputs', 'endTime', 'estimatedShockArrivalTime', 
        'estimatedDuration', 'eventTime', 'flrID', 'gstID', 'halfAngle', 'hssID', 'impactList', 
        'instruments', 'isEarthGB', 'isMostAccurate', 'kp_18', 'kp_90', 'kp_135', 'kp_180', 
        'latitude', 'link', 'linkedEvents', 'location', 'longitude', 'modelCompletionTime',
        'mpcID', 'note', 'peakTime', 'rbeID', 'rmin_re', 'sepID', 'simulationID', 'sourceLocation', 
        'startTime', 'time21_5', 'type']

        for column in columns:
            column_list = []
            
            for i in api_range:
                
                if column == 'instruments':
                    try:
                        instrument = len(api_list[i]['instruments'])
                        
                        if instrument ==1:
                            column_list.append(api_list[i]['instruments'][0]['displayName'])
                            continue
                        elif instrument ==0:
                            column_list.append('N/A')
                            continue
                        else:
                            # Add Loop to Concatenate Later
                            column_list.append('Multiple')
                            continue
                    except:
                        continue
                
                if column == 'linkedEvents':
                    try:
                        event = api_list[i]['linkedEvents']

                        if event == 'None':
                            column_list.append('N/A')
                            continue
                        elif event is list:
                            # Add Loop to Concatenate Later
                            column_list.append('Multiple')
                            continue
                        else:
                            column_list.append(api_list[i]['linkedEvents'])
                            continue
                    except:
                        continue

                else:
                    try:
                        col = api_list[i][f'{column}']
                        column_list.append(col)
                        continue
                    except:
                        continue
            
            if len(column_list) > 0:
                columnDict[f'{column}'] = column_list
            else:
                continue
        
        # Add Dictionary of Columns to df Dictionary
            
        # If Column == instruments cmeInputs or AllKpIndex Combine Dicts
            
        # Else
        df_Dicts[f'{api}'] = columnDict

        # Create Dataframe
        df = pd.DataFrame(df_Dicts[f'{api}'])
        
        # Export to S3
        s3_export(df, api)  

#%%
    
## Boto3

def s3_export(df, name):

    import boto3
    from io import StringIO

    path = f'NASA/{name}.csv'
        
    s3 = boto3.resource('s3')
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index = False)
    s3.Object('erikatestbucket', path).put(Body=csv_buffer.getvalue())
    
#%%
    
# Inputs

api_key = 'oXd16S7iyStpHG1br0c1yTq9B5kFftCoqx9lfUoE'

# Procedure

ParamsDict = params_dict(api_key)
responseDict = get_api_data(ParamsDict)
nasa_dfs(responseDict)
