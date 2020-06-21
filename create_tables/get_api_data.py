#%%

# Pull DONKI Requests from API
    
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