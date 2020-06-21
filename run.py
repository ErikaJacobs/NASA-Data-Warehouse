#%%

# NASA Data Warehouse - RUN FILE

# Input below for run.py repo file directory

####################################

# Input - Script Directory
file =  'C:/Users/cluel/Documents/GitHub/NASA-Redshift'

api_key = 'oXd16S7iyStpHG1br0c1yTq9B5kFftCoqx9lfUoE'

####################################

# Set Working Directory
import os
os.chdir(file)

# Import Run Modules
from main import main

# Run Application
if __name__ == '__main__' :
    main.run(api_key)
        
#%%