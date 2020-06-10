# NASA Redshift - Data Warehouse Project

#%%
api_key = api_key
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
                'notifications', 'GST', 'IPS', 'SEP', 'MPC', 'RBE','FLR']
    
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

# CME df - Dynamodb
    
def CME(responseDict):
    
    import pandas as pd
    
    # Set-Up
    name = 'CME'
    api_list = responseDict[f'{name}']
    
    # Create Lists
    activityID = []
    catalog = []
    startTime = []
    sourceLocation = []
    activeRegionNum = []
    note = []
    instruments = []
    linkedEvents = []
    
    # Extract Data from Dictionary
    
    api_range = list(range(len(api_list)))
    
    for i in api_range:
        activityID.append(api_list[i]['activityID'])
        catalog.append(api_list[i]['catalog'])
        startTime.append(api_list[i]['startTime'])
        sourceLocation.append(api_list[i]['sourceLocation'])
        activeRegionNum.append(api_list[i]['activeRegionNum'])
        note.append(api_list[i]['note'])
        
        # Instruments
        if len(api_list[i]['instruments']) ==1:
            instruments.append(api_list[i]['instruments'][0]['displayName'])
        elif len(api_list[i]['instruments']) ==0:
            instruments.append('N/A')
        else:
            # Add Loop to Concatenate Later
            instruments.append('Multiple')
        
        # linkedEvents'
        if api_list[i]['linkedEvents'] == 'None':
            linkedEvents.append('N/A')
        elif type(api_list[i]['linkedEvents']) is list:
            # Add Loop to Concatenate Later
            linkedEvents.append('Multiple')
        else:
            linkedEvents.append(api_list[i]['linkedEvents'])
    
    # Create Dataframe
        
    df = pd.DataFrame({
    'activityID': activityID,   
    'catalog': catalog,
    'startTime': startTime,
    'sourceLocation': sourceLocation,
    'activeRegionNum': activeRegionNum,
    'note': note,
    'instruments': instruments,
    'linkedEvents': linkedEvents
    })
    
    # Export to S3
    s3_export(df, name)
            
#%%
    
#CME Analysis - RDS

def CMEAnalysis(responseDict):
    
    import pandas as pd
    
    # Set-Up
    name = 'CMEAnalysis'
    api_list = responseDict[f'{name}']
    
    # Create Lists
    time21_5 = []
    latitude = []
    longitude = []
    halfAngle = []
    CME_type = []
    isMostAccurate = []
    associatedCMEID = []
    note = []
    catalog = []
    link = []
    
    # Extract Data from Dictionary
    
    api_range = list(range(len(api_list)))
    
    for i in api_range:
        time21_5.append(api_list[i]['time21_5'])
        latitude.append(api_list[i]['latitude'])
        longitude.append(api_list[i]['longitude'])
        halfAngle.append(api_list[i]['halfAngle'])
        CME_type.append(api_list[i]['type'])
        isMostAccurate.append(api_list[i]['isMostAccurate'])
        associatedCMEID.append(api_list[i]['associatedCMEID'])
        note.append(api_list[i]['note'])
        catalog.append(api_list[i]['catalog'])
        link.append(api_list[i]['link'])
    
    # Create Dataframe
        
    df = pd.DataFrame({
    'time21_5': time21_5,   
    'latitude': latitude,
    'longitude': longitude,
    'halfAngle': halfAngle,
    'CME_type': CME_type,
    'isMostAccurate': isMostAccurate,
    'associatedCMEID': associatedCMEID,
    'note': note,
    'catalog': catalog,
    'link': link
    })

    # Export to S3
    s3_export(df, name)

#%%
    
# HSS df - DynamoDB

def HSS(responseDict):
    
    import pandas as pd
    
    # Set-Up
    name = 'HSS'
    api_list = responseDict[f'{name}']
    
    # Create Lists
    hssID = []
    eventTime = []
    instruments = []
    linkedEvents = []
    link = []

    # Extract Data from Dictionary
    
    api_range = list(range(len(api_list)))
    
    for i in api_range:
        hssID.append(api_list[i]['hssID'])
        eventTime.append(api_list[i]['eventTime'])
        link.append(api_list[i]['link'])
        
        # Instruments
        if len(api_list[i]['instruments']) ==1:
            instruments.append(api_list[i]['instruments'][0]['displayName'])
        elif len(api_list[i]['instruments']) ==0:
            instruments.append('N/A')
        else:
            # Add Loop to Concatenate Later
            instruments.append('Multiple')
        
        # linkedEvents'
        if api_list[i]['linkedEvents'] == 'None':
            linkedEvents.append('N/A')
        elif type(api_list[i]['linkedEvents']) is list:
            # Add Loop to Concatenate Later
            linkedEvents.append('Multiple')
        else:
            linkedEvents.append(api_list[i]['linkedEvents'])

    # Create Dataframe
    
    df = pd.DataFrame({
    'hssID': hssID,   
    'eventTime': eventTime,
    'instruments': instruments,
    'linkedEvents': linkedEvents,
    'link': link
    })
   
    # Export to S3
    s3_export(df, name)

#%%
    
# WSA+EnlilSimulation - RDS

def WSAEnlilSimulations(responseDict):
        
    import pandas as pd
    
    # Set-Up
    name = 'WSAEnlilSimulations'
    api_list = responseDict[f'{name}']
    
    # Create Lists
    simulationID = []
    modelCompletionTime = []
    au = []
    cmeInputs = []
    estimatedShockArrivalTime = []
    estimatedDuration = []
    rmin_re = []
    kp_18 = []
    kp_90 = []
    kp_135 = []
    kp_180 = []
    isEarthGB = []
    impactList = []
    link = []
    
    # Extract Data from Dictionary
    
    api_range = list(range(len(api_list)))
    
    for i in api_range:
        simulationID.append(api_list[i]['simulationID'])
        modelCompletionTime.append(api_list[i]['modelCompletionTime'])
        au.append(api_list[i]['au'])
        cmeInputs.append(api_list[i]['cmeInputs'])
        estimatedShockArrivalTime.append(api_list[i]['estimatedShockArrivalTime'])
        estimatedDuration.append(api_list[i]['estimatedDuration'])
        rmin_re.append(api_list[i]['rmin_re'])
        kp_18.append(api_list[i]['kp_18'])
        kp_90.append(api_list[i]['kp_90'])
        kp_135.append(api_list[i]['kp_135'])
        kp_180.append(api_list[i]['kp_180'])
        isEarthGB.append(api_list[i]['isEarthGB'])
        impactList.append(api_list[i]['impactList'])
        link.append(api_list[i]['link'])    
    
    # Create Dataframe
    
    df = pd.DataFrame({
    'simulationID': simulationID,
    'modelCompletionTime': modelCompletionTime,
    'au': au,
    'cmeInputs': cmeInputs,
    'estimatedShockArrivalTime': estimatedShockArrivalTime,
    'estimatedDuration': estimatedDuration,
    'rmin_re': rmin_re,
    'kp_18': kp_18,
    'kp_90': kp_90,
    'kp_135': kp_135,
    'kp_180': kp_180,
    'isEarthGB': isEarthGB,
    'impactList': impactList,
    'link': link
    })

    # Export to S3
    s3_export(df, name)
    
#%%
# GST df - DynamoDB

def GST(responseDict):
    
    import pandas as pd
    
    # Set-Up
    name = 'GST'
    api_list = responseDict[f'{name}']
    
    # Create Lists
    gstID = []
    startTime = []
    allKpIndex = []
    linkedEvents = []
    link = []
    
    # Extract Data from Dictionary
    
    api_range = list(range(len(api_list)))
    
    for i in api_range:   
        gstID.append(api_list[i]['gstID'])   
        startTime.append(api_list[i]['startTime'])   
        allKpIndex.append(api_list[i]['allKpIndex'])           
        link.append(api_list[i]['link'])   

        # linkedEvents
        if api_list[i]['linkedEvents'] == 'None':
            linkedEvents.append('N/A')
        elif type(api_list[i]['linkedEvents']) is list:
            # Add Loop to Concatenate Later
            linkedEvents.append('Multiple')
        else:
            linkedEvents.append(api_list[i]['linkedEvents'])
    
    # Create Dataframe
    
    df = pd.DataFrame({
    'gstID': gstID,
    'startTime': startTime,
    'allKpIndex': allKpIndex,
    'linkedEvents': linkedEvents,
    'link': link
    })    
    
    # Export to S3
    s3_export(df, name)
    
#%%
    
    
# IPS df - DynamoDB

def IPS(responseDict):
    
    import pandas as pd
    
    # Set-Up
    name = 'IPS'
    api_list = responseDict[f'{name}']
    
    # Create Lists
    catalog = []
    activityID = []
    location = []
    eventTime = []
    link = []
    instruments = []
    
    # Extract Data from Dictionary
    
    api_range = list(range(len(api_list)))
    
    for i in api_range:   
        catalog.append(api_list[i]['catalog'])   
        activityID.append(api_list[i]['activityID'])   
        location.append(api_list[i]['location'])     
        eventTime.append(api_list[i]['eventTime'])             
        link.append(api_list[i]['link']) 
        
        # Instruments
        if len(api_list[i]['instruments']) ==1:
            instruments.append(api_list[i]['instruments'][0]['displayName'])
        elif len(api_list[i]['instruments']) ==0:
            instruments.append('N/A')
        else:
            # Add Loop to Concatenate Later
            instruments.append('Multiple')
            
    # Create Dataframe
    
    df = pd.DataFrame({
    'catalog': catalog,
    'activityID': activityID,
    'location': location,
    'eventTime': eventTime,
    'link': link,
    'instruments': instruments
    })
    
    # Export to S3
    s3_export(df, name)    

IPS(responseDict)     
    
#%%
# SEP df - DynamoDB

def SEP(responseDict):
    print(responseDict['SEP'][0])
    
    
    
# MPC df - DynamoDB

def MPC(responseDict):
    print(responseDict['MPC'][0])
    
    
    
# RBE df

def RBE(responseDict):
    print(responseDict['RBE'][0])
    
    
    
# FLR df

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


# Procedure

ParamsDict = params_dict(api_key)
responseDict = get_api_data(ParamsDict)

# Sends to S3
CME(responseDict)
CMEAnalysis(responseDict)
HSS(responseDict)
WSAEnlilSimulations(responseDict)
GST(responseDict)


#%% Insight Weather

#def insight_json():

  #url = "https://api.nasa.gov/insight_weather/"
  #params = {
     # 'api_key':api_key,
     # 'feedtype':'json',
     # 'ver':'1.0'
     # }
 # r = requests.get(url,params=params)
  #print(r.status_code)
  #print(r.headers.get('Content-Type'))
  #print(r.encoding)
  
  #response = r.json()
  #print(response)
  
#insight_json()

#%%

# DONKI

# application/json;charset=UTF-8
# Coronal Mass Ejection (CME) - https://api.nasa.gov/DONKI/CME/
# Coronal Mass Ejection (CME) Analysis - https://api.nasa.gov/DONKI/CMEAnalysis/
###### Hight Speed Stream (HSS) - https://api.nasa.gov/DONKI/HSS/
###### WSA+EnlilSimulation - https://api.nasa.gov/DONKI/WSAEnlilSimulations
# Notifications - https://api.nasa.gov/DONKI/notifications/

# text/plain; charset=UTF-8
# Geomagnetic Storm (GST) - https://api.nasa.gov/DONKI/GST/
# Interplanetary Shock (IPS) - https://api.nasa.gov/DONKI/IPS/
# Solar Energetic Particle (SEP) - https://api.nasa.gov/DONKI/SEP/
# Magnetopause Crossing (MPC) - https://api.nasa.gov/DONKI/MPC/
# Radiation Belt Enhancement (RBE) - https://api.nasa.gov/DONKI/RBE/

# text/html;charset=ISO-8859-1
# Solar Flare (FLR) - https://api.nasa.gov/DONKI/FLR/

#%%
#import boto3

#redshift = boto3.client('redshift')

#redshift.delete_cluster(ClusterIdentifier='redshift-cluster', 
#                        SkipFinalClusterSnapshot = True)


#%%