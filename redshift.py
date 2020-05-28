# NASA Redshift - Data Warehouse Project
# Inputs


#%%

# Import Packages - Set Dates
import datetime
from dateutil.relativedelta import relativedelta

ParamsDict=dict()
now = str(datetime.datetime.now().date())
then = str(datetime.datetime.now().date() - relativedelta(years=5))

api_key = api_key
# application/json;charset=UTF-8
params = {
      'api_key':api_key,
      'startDate':then,
      'endDate':now
      }
ParamsDict['CME']=params
ParamsDict['CMEAnalysis']=params
ParamsDict['HSS']=params
ParamsDict['WSAEnlilSimulations']=params
ParamsDict['notifications']=params

# text/plain; charset=UTF-8
params = {
      'api_key':api_key,
      'startDate':then,
      'endDate':now,
      'feedtype':'json'
      }

ParamsDict['GST']=params
ParamsDict['IPS']=params
ParamsDict['SEP']=params
ParamsDict['MPC']=params
ParamsDict['RBE']=params

# text/html;charset=ISO-8859-1
params = {
      'api_key':api_key,
      'startDate':then,
      'endDate':now,
      'feedtype':'json'
      }

ParamsDict['FLR']=params

#%%

#DONKI REQUESTS

import requests

responseDict = {}

api_list = ['CME','CMEAnalysis','HSS','WSAEnlilSimulations', 
            'notifications', 'GST', 'IPS', 'SEP', 'MPC', 'RBE','FLR']

def donki_json(API):
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
    donki_json(API)

#%%



#DONKI PLAIN TEXT REQUESTS

#def donki_gst():
#  url = "https://api.nasa.gov/DONKI/GST/"
#  params = {
#      'api_key':api_key,
#      'startDate':'2015-05-28',
#      'endDate':'2020-05-28',
#      'feedtype':'json'
#      }
#  r = requests.get(url,
#                   params=params)
#  #print(r.status_code)
#  #print(r.headers.get('Content-Type'))
#  #print(r.encoding)
  
#  response = r.json()
#  pp.pprint(response[2])
  
#donki_gst()

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