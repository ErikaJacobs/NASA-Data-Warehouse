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
* [```run.py```](https://github.com/ErikaJacobs/NASA-Data-Warehouse/blob/master/run.py)

# Other Repository Contents
* create_tables
     * [```get_api_data.py```](https://github.com/ErikaJacobs/NASA-Data-Warehouse/blob/master/create_tables/get_api_data.py) - Pulls DONKI data from NASA API in json format
     * [```nasa_dfs.py```](https://github.com/ErikaJacobs/NASA-Data-Warehouse/blob/master/create_tables/nasa_dfs.py) - Creates structured dataframes from the NASA data, and exports to S3
     * [```params_dict.py```](https://github.com/ErikaJacobs/NASA-Data-Warehouse/blob/master/create_tables/params_dict.py) - Creates individualized parameters for pulling each individual type of NASA DONKI data
     * [```s3_export.py```](https://github.com/ErikaJacobs/NASA-Data-Warehouse/blob/master/create_tables/s3_export.py) - Code used for exporting a dataframe to S3
* main
     * [```main.py```](https://github.com/ErikaJacobs/NASA-Data-Warehouse/blob/master/main/main.py) - Organizes execution of all modules
* queries
     * [```execute_queries.py```](https://github.com/ErikaJacobs/NASA-Data-Warehouse/blob/master/queries/execute_queries.py) -  Executes queries to drop, create, and insert into Redshift tables
     * [```redshift_queries.py```](https://github.com/ErikaJacobs/NASA-Data-Warehouse/blob/master/queries/redshift_queries.py) - Creates queries for all dataframes to be dropped, created, and inserted into Redshift tables
     * [```table_configs.py```](https://github.com/ErikaJacobs/NASA-Data-Warehouse/blob/master/queries/table_configs.py) - Sets data types for each column in all dataframes, and aggregates content for SQL create statements
* redshift_cluster
     * [```config.py```](https://github.com/ErikaJacobs/NASA-Data-Warehouse/blob/master/redshift_cluster/config.py) - Imports configurations for the Redshift cluster from configuration file (config.ini) - makes dictionary
     * [```create_cluster.py```](https://github.com/ErikaJacobs/NASA-Data-Warehouse/blob/master/redshift_cluster/create_cluster.py) - Creates Redshift cluster for NASA data
     * [```endpoint.py```](https://github.com/ErikaJacobs/NASA-Data-Warehouse/blob/master/redshift_cluster/endpoint.py) - Obtains endpoint for Redshift cluster after creation, and adds it to the configuration dictionary
     * [```iam.py```](https://github.com/ErikaJacobs/NASA-Data-Warehouse/blob/master/redshift_cluster/iam.py) - Creates security role for Redshift to use to copy data into cluster
     * [```open_port.py```](https://github.com/ErikaJacobs/NASA-Data-Warehouse/blob/master/redshift_cluster/open_port.py) - Opens the port to connect to Redshift
     * [```redshift_boto.py```](https://github.com/ErikaJacobs/NASA-Data-Warehouse/blob/master/redshift_cluster/redshift_boto.py) - Creates AWS CLI access to perform operations in Redshift   
     * [```redshift_connection.py```](https://github.com/ErikaJacobs/NASA-Data-Warehouse/blob/master/redshift_cluster/redshift_connection.py) - Creates SQL connection to Redshift database
* undo
     * [```delete.py```](https://github.com/ErikaJacobs/NASA-Data-Warehouse/blob/master/undo/delete.py) - Deletes both the Redshift cluster and IAM rule created to access it
* [```config.ini```](https://github.com/ErikaJacobs/NASA-Data-Warehouse/blob/master/config.ini) - Redshift configurations

# Sources
* [Boto3 - AWS Redshift](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html)
* [Boto3 - IAM](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html)
* [Requests: HTTP for Humans](https://requests.readthedocs.io/en/master/)
