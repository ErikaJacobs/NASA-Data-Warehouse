# Redshift Data Warehouse of NASA Weather Data
According to NASA, the Space Weather Database Of Notifications, Knowledge, Information (DONKI) is "a comprehensive on-line tool for space weather forecasters, scientists, and the general space science community." DONKI provides data on space weather events updated daily, which can be accessed through an API feed through NASA's website in json format.

This project takes the data from NASA's API, cleans aspects of the data, and converts the data into a set of structured datasets to be readily used for analysis. The datasets are then exported as CSV files in AWS S3 for staging, and are used to create a data warehouse through AWS Redshift for ease of online analytical processes. This process is handled by using boto3.

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

## How To Run

##### *AWS Credentials*
AWS Credentials will need to be saved locally in the .aws directory of an operating system in order for this project to successfully run. [Click here](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html) to learn more about this process.
##### *Adjust Configurations*
Configurations in the config.ini file, for the most part, would be optional changes regarding naming preferences. The config.ini file may need to be adjusted for node type, number of nodes, or AWS region depending on user need. Redshift’s default port is 5439 (which is the current configuration), but could potentially need adjustment depending on the AWS environment and this project were being run on.
##### *Obtain NASA API Token*
In order to pull data from NASA’s API for DONKI, an API token will need to be obtained directly from NASA. [Click here](https://api.nasa.gov/) to obtain a NASA API key.
##### *Set Environment Variables*
For this project to process, the NASA API access key will need to be set as an environment variable called "nasa_key". This environment variable will need to be set on the operating system this project is to be run on.
##### *Install Requirements and Run*
On the command line of your operating system, navigate to the repository directory (ideally using a Python virtual environment).

Run the following code on the command line to install requirements:
```
pip install -r requirements.txt 
```

Run the following code on the command line to run this project:
```
Python run.py
```

To remove the Redshift cluster and environment, run the following code:
```
Python delete.py
```
Please note that Redshift incurs an hourly charge depending on the node type and amount. Please [click here](https://aws.amazon.com/redshift/pricing/) to learn more about Redshift’s pricing structure.

# Featured Scripts or Deliverables
* [```run.py```](run.py)

# Other Repository Contents
* modules
     * [```create_tables.py```](modules/create_tables.py) - Pulls DONKI data from NASA API, creates structured dataframes, and exports to S3
     * [```execute_queries.py```](modules/execute_queries.py) - Creates and executes queries to drop, create, and insert into Redshift tables
     * [```main.py```](modules/main.py) - Organizes execution of all modules
     * [```redshift_connection.py```](modules/redshift_connection.py) - Creates Redshift cluster and security role for NASA data
* [```config.ini```](config.ini) - Configurations for Redshift
* [```delete.py```](delete.py) - Deletes Redshift cluster and security role created from this repository
* [```requirements.txt```](requirements.txt) - Python package requirements

# Sources
* [Boto3 - AWS Redshift](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html)
* [Boto3 - IAM](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html)
* [Requests: HTTP for Humans](https://requests.readthedocs.io/en/master/)
* [NASA Open APIs (DONKI)](https://api.nasa.gov/)
