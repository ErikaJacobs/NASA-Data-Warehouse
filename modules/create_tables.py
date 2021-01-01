import datetime
from dateutil.relativedelta import relativedelta
import os
import requests
import pandas as pd
import boto3
from io import StringIO

class Create_tables:
    
    def __init__(self):
        self.ParamsDict = {}
        self.api_key = os.environ.get('nasa_key')
        self.responseDict = {}
        self.df_Dicts = {}
        
    def params_dict(self):
        
        ParamsDict = self.ParamsDict
    
        # Set Dates
        now = str(datetime.datetime.now().date())
        then = str(datetime.datetime.now().date() - relativedelta(years=5))
        
        # application/json;charset=UTF-8
        paramsjson = {
              'api_key': self.api_key,
              'startDate': then,
              'endDate': now
              }
        
        # text/plain; charset=UTF-8
        paramstext = {
              'api_key': self.api_key,
              'startDate': then,
              'endDate': now,
              'feedtype': 'json'
              }
        
        # Append to Dict
        textlist = ['GST', 'IPS', 'SEP', 'MPC', 'RBE', 'FLR']
        jsonlist = ['CME', 'CMEAnalysis', 'HSS', 'WSAEnlilSimulations']
        self.api_list = textlist + jsonlist
        
        for item in textlist:
            ParamsDict[item]=paramstext
        
        for item in jsonlist:
            ParamsDict[item]=paramsjson
            
    def get_api_data(self):

        ParamsDict = self.ParamsDict
        responseDict = self.responseDict
        
        api_list = self.api_list
        
        def donki_json(API, ParamsDict):
          url = f"https://api.nasa.gov/DONKI/{API}"
          params = ParamsDict[API]
          r = requests.get(url, params = params)
          r.encoding = 'utf-8'
          
          try:
              response = r.json()
        
          except Exception as e:
              print(f"{API} was not successfully requested.")
              print(e)
              response = 'N/A'
              
          responseDict[API] = response
        
        for API in api_list:
            donki_json(API, ParamsDict)
            
    def s3_export(self, df, name):
        path = f'NASA/{name}.csv'
            
        s3 = boto3.resource('s3')
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index = False, sep="~")
        s3.Object('erikatestbucket', path).put(Body=csv_buffer.getvalue())
            
    def nasa_dfs(self):
        
        responseDict = self.responseDict
        nasa_api = self.api_list
        df_Dicts = self.df_Dicts
    
        for api in nasa_api:
    
            # Set-Up
            api_list = responseDict[f'{api}']
            columnDict = {}
    
            # Extract Data from Dictionary
            api_range = list(range(len(api_list)))
            
            # Get List of Columns from Longest Record
            max_index = 0
            max_length = 0
            
            for i in api_range:
                if len(api_list[i].keys()) > max_length:
                    max_length = len(api_list[i].keys())
                    max_index = i
            
            # Get Columns 
            columns = api_list[max_index].keys()
    
            for column in columns:
                column_list = []   
                
                if column == 'allKpIndex':
                    KpAvg_list = []
                    sources = []
                
                if column == 'cmeInputs':
                    cmeInputsDict = {}
                    WSAcolumns = ['latitude','longitude',
                                           'speed','halfAngle','isMostAccurate']
                            
                    for x in WSAcolumns:
                        cmeInputsDict[f'{x}'] = []
                
                # Loop through all entries of column
                for i in api_range:
                    
                    if column == 'instruments':
                        try:
                            instruments = range(len(api_list[i]['instruments']))
                            
                            instrument_list = []
                            
                            for x in instruments:
                                instrument_list.append(api_list[i]['instruments'][x]['displayName'])
                           
                            col = '_'.join(instrument_list)
                            column_list.append(col)
                            continue
    
                        except:
                            continue
                    
                    if column == 'linkedEvents':
                        try:
                            event = api_list[i]['linkedEvents']
                        
                            if event is None:
                                col = 'None'
                                column_list.append(col)
                                continue
                            else:
                                events = range(len(event))
                                event_list = []
                                
                                for x in events:
                                    event_list.append(api_list[i]['linkedEvents'][x]['activityID'])
                                col = '_'.join(event_list)
                                column_list.append(col)
                                continue
                        except:
                            continue
                    
                    if column =="allKpIndex" and api == 'GST':
                        try:
                            KpIndex_list = []
                            Source_list = []
                            
                            KpIndexes = range(len(api_list[i]['allKpIndex']))
                            
                            for x in KpIndexes:
                                KpIndex_list.append(int(api_list[i]['allKpIndex'][x]['kpIndex']))
                                Source_list.append(api_list[i]['allKpIndex'][x]['source'])
                            
                            # Build kpAvg Field
                            if len(KpIndex_list) >= 1:
                                kpAvg = sum(KpIndex_list)/len(KpIndex_list)
                                KpAvg_list.append(kpAvg)
                            else:
                                KpAvg_list.append('N/A')
                            
                            # Build Source Field
                            Source_list = list(dict.fromkeys(Source_list))
                            
                            if len(Source_list) == 0:
                                source = 'N/A'
                                
                            if len(Source_list) == 1:
                                source = Source_list[0]
    
                            else:
                                source = '_'.join(Source_list)
                            
                            sources.append(source)
                            continue
                    
                        except:
                            continue
                        
                    if column == 'cmeInputs' and api == 'WSAEnlilSimulations':
                        for x in WSAcolumns:
                            try:
                                cmeInputsDict[f'{x}'].append(api_list[i][f'{column}'][0][f'{x}'])
                            except:
                                cmeInputsDict[f'{x}'].append("N/A")
    
                    if column == 'impactList':
                        try:
                            impact = api_list[i]['impactList']
                        
                            if impact is None:
                                col = 'None'
                                column_list.append(col)
                                continue
                            else:
                                impacts = range(len(impact))
                                impact_list = []
                                
                                for x in impacts:
                                    impact_list.append(api_list[i]['impactList'][x]['location'])
                                col = '_'.join(impact_list)
                                column_list.append(col)
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
                        
                # Putting Together Columns or Dictionaries      
                if column =="allKpIndex" and api == 'GST':
                    if KpAvg_list and len(KpAvg_list) > 0:
                        columnDict['KpAvg'] = KpAvg_list
                    if sources and len(sources) > 0:
                        columnDict['source'] = sources
                    else:
                        continue
                    
                if column == 'cmeInputs' and api == 'WSAEnlilSimulations':
                    keys = list(cmeInputsDict.keys())
                    
                    for key in keys:
                        columnDict[f'{key}'] = cmeInputsDict[f'{key}']
                    
                elif len(column_list) > 0:
                    columnDict[f'{column}'] = column_list
                else:
                    continue
    
            # Else
            df_Dicts[f'{api}'] = columnDict
    
            # Create Dataframe
            df = pd.DataFrame(df_Dicts[f'{api}'])
            
            # Final Touches to df
            for item in df.columns:
                df[item] = df[item].apply(lambda x: str(x).replace('~', '-'))
                df[item] = df[item].fillna('N/A')
            
            if 'note' in df.columns:
                df['note'] = df['note'].apply(lambda x: str(x)[0:499])
            
            # Export to S3
            self.s3_export(df, api)  
    