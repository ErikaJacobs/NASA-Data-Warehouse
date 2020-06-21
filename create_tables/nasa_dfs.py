#%%

# One Combined User-Defined Function to create ALL tables

def nasa_dfs(responseDict):
    import pandas as pd
    from create_tables import s3_export

    nasa_api = ['CME','CMEAnalysis','HSS','WSAEnlilSimulations', 
    'GST', 'IPS', 'SEP', 'MPC', 'RBE','FLR']

    df_Dicts = {}

    for api in nasa_api:

        # Set-Up
        api_list = responseDict[f'{api}']
        columnDict = {}

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
        s3_export.s3_export(df, api)  
        
    return df_Dicts

#%%