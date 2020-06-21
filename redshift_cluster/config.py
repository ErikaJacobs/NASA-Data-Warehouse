#%%

# IMPORT CONFIGS

def config():

    import configparser
    
    Config = configparser.ConfigParser()
    Config.read("C:/Users/cluel/Documents/GitHub/NASA-Redshift/config.ini")
    Config.sections()
    
    config_list = Config.options('Redshift')
    configs = {}
    
    # Create Dictionary of Configurations
    
    for option in config_list:
        if option == 'numberofnodes' or option == 'port':
            configs[f'{option}'] = int(Config.get('Redshift', option))
        else:
            configs[f'{option}'] = Config.get('Redshift', option)
    
    return configs

#%%
    