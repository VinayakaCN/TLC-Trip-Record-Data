Analysing the TLC Trip Record Data using AIrflow and dask


# Overview
  The packaged program is an Airflow Job written in Python Language which reads a CSV file of "TLC Trip Record Data" orginally posted from"https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page and provides basic analytics on it like an average distance per monthly  and also provides a rooling 45 days Average distance (Assuming max of tpep_dropoff_datetime as present date)
and also Same result message will be sent to your Slack communicator(configuration in Shared.confile file)

  The Above program is written by using Dask libraries , to acheive distributed parallel processing.


# Requirements and Installation
  * Python (3.6.4) , recomended above 3.0
  * Dask dataframe 
  * Airflow Version : 1.9.0
  * Slack client 
  
  Kindly refer Requirements.txt for pip commands
  
 # how to execute 
  * install all the above packages
  * Download "yellow_tripdata_XXXX.csv" CSV file from NYC website : https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page to a         local directory
  * Deploy the "Yello_taxies_Average_trip_length.py" job into your Airflow service
  * pass the local_file_path as variable called "File_path" to the DAG.
  * configure the slack configuration in file shared/config.py
  * Trigger the DAG
 
 * And also i have attached as sample file for quick checkup "Sample_trip_data.CSV"
 
 # test Cases
 * The above DAG will throw an error if the provide input CSV file does not have column called "'tpep_dropoff_datetime' , 'trip_distance'"
 * if the date format for the column 'tpep_dropoff_datetime' is not in "2019-01-01 23:59:59" in that case too the program will throw and      error 
 
 # Output 
  The output will be in below format
  ```
  Note >  Average Trip distance for a month :
         year  month
        2018  1        5.0
              2        6.0
        Name: trip_distance, dtype: float64
         **************************************************
  Note > from past 45 days Average Trip distance : 5.5
        
  '''