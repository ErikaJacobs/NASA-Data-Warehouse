# Connect to API

import requests

api_key = api_key

def neofeed():
  url = "https://api.nasa.gov/neo/rest/v1/feed"
  params = {
      'api_key':api_key,
      'start_date':'2020-01-22',
      'end_date':'2020-01-22'
  }
  response = requests.get(url,params=params).json()
  #print(response.status_code)
  
  print(response['near_earth_objects']['2020-01-22'][1]['links'])
  #print(response)
  
neofeed()


#%%
#import boto3

#redshift = boto3.client('redshift')

#redshift.delete_cluster(ClusterIdentifier='redshift-cluster', 
#                        SkipFinalClusterSnapshot = True)


#%%