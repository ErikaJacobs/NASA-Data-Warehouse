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
     * [```get_api_data.py```]() - DESCRIPTION
     * [```nasa_dfse.py```]() - DESCRIPTION
     * [```params_dict.py```]() - DESCRIPTION
     * [```s3_export.py```]() - DESCRIPTION
* main
     * [```main.py```]() - DESCRIPTION
* queries
     * [```execute_queries.py```]() - DESCRIPTION
     * [```redshift_queries.py```]() - DESCRIPTION
     * [```table_configs.py```]() - DESCRIPTION
* redshift_cluster
     * [```config.py```]() - DESCRIPTION
     * [```create_cluster.py```]() - DESCRIPTION
     * [```tendpoint.py```]() - DESCRIPTION
     * [```iam.py```]() - DESCRIPTION
     * [```open_port.py```]() - DESCRIPTION
     * [```redshift_boto.py```]() - DESCRIPTION     
     * [```redshift_connection.py```]() - DESCRIPTION
* undo
* config.ini
