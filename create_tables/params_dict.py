#%%

#  Create Parameters to Pull from API

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