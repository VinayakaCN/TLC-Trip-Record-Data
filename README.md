Analysing the TLC Trip Record Data using AIrflow


# Overview
  The packaged program is an Airflow Job written in Python Language which reads a CSV file of "TLC Trip Record Data" orginally posted from"https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page and provides basic analytics on it like an average distance per monthly  and also provides a rooling 45 days Average distance (Assuming max of tpep_dropoff_datetime as present date)
and also Same result message will be sent to your Slack communicator(configuration in Shared.confile file)

  The Above program is written by using Dask libraries , to acheive distributed parallel processing.


# Requirements and Installation
  > Python (3.6.4) , recomended above 3.0
  > Dask dataframe 
  > Airflow Version : 1.9.0
  > Slack client 
  
  Kindly refer Requirements.txt for pip commands
  
 # how to execute 
  > install all the above packages
  > Download "yellow_tripdata_XXXX.csv" CSV file from NYC website : https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page to a         local directory
  > Deploy the "Yello_taxies_Average_trip_length.py" job into your Airflow service
  > pass the local_file_path as variable called "File_path" to the DAG.
  > Trigger the 
 # test Cases
 > This 
