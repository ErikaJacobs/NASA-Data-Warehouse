# Redshift Data Warehouse of NASA Weather Data
Pulls data from NASA DONKI API, and stages data in S3 to load to Redshift using boto3

## Methods Used
* ETL
* Data Warehousing
* API Connection

## Technologies Used
* Python
* S3
* Redshift

## Packages Used
* Requests
* Psycopg2
* Pandas
* Boto3

# Featured Notebooks, Scripts, Analysis, or Deliverables
* [```run.py```](https://github.com/ErikaJacobs/NASA-Redshift/blob/master/run.py)

# Other Repository Contents
* 

# Sources
* create_tables
     * [```get_api_data.py```]() - Pulls DONKI data from NASA API in json format
     * [```nasa_dfs.py```]() - Creates structured dataframes from the NASA data, and exports to S3
     * [```params_dict.py```]() - Creates individualized parameters for pulling each individual type of NASA DONKI data
     * [```s3_export.py```]() - Code used for exporting a dataframe to S3
* main
     * [```main.py```]() - Organizes execution of all modules
* queries
     * [```execute_queries.py```]() -  Executes queries to drop, create, and insert into Redshift tables
     * [```redshift_queries.py```]() - Creates queries for all dataframes to be dropped, created, and inserted into Redshift tables
     * [```table_configs.py```]() - Sets data types for each column in all dataframes, and aggregates content for SQL create statements
* redshift_cluster
     * [```config.py```]() - Imports configurations for the Redshift cluster from configuration file (config.ini) - makes dictionary
     * [```create_cluster.py```]() - Creates Redshift cluster for NASA data
     * [```endpoint.py```]() - Obtains endpoint for Redshift cluster after creation, and adds it to the configuration dictionary
     * [```iam.py```]() - Creates security role for Redshift to use to copy data into cluster
     * [```open_port.py```]() - Opens the port to connect to Redshift
     * [```redshift_boto.py```]() - Creates AWS CLI access to perform operations in Redshift   
     * [```redshift_connection.py```]() - Creates SQL connection to Redshift database
* undo
     * [```delete.py```]() - Deletes both the Redshift cluster and IAM rule created to access it
* config.ini - Redshift configurations
