# NASA Redshift - Data Warehouse Project
# Inputs


#%%
api_key = api_key
def params_dict():
    
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
    
    jsonlist = ['CME', 'CMEAnalysis', 'HSS', 'WSAEnlilSimulations', 'notifications']
    
    # text/plain; charset=UTF-8
    paramstext = {
          'api_key':api_key,
          'startDate':then,
          'endDate':now,
          'feedtype':'json'
          }
    
    # Append to Dict
    
    textlist = ['GST', 'IPS', 'SEP', 'MPC', 'RBE', 'FLR']
    jsonlist = ['CME', 'CMEAnalysis', 'HSS', 'WSAEnlilSimulations', 'notifications']
    
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

ParamsDict = params_dict()
responseDict = get_api_data(ParamsDict)




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