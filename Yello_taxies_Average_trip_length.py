#-------------------------------------------------------------------------
# Author: Vinayaka CN
# Date: 10 Mar 2019
# Content : Below Airflow Job will read a CSV file of "TLC Trip Record Data" orginally posted from "https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page"
#           and provides a Average distance per monthly . and also provides a rooling 45 days Average distance (Assuming max of tpep_dropoff_datetime as present date)
#           and also Same result message will be sent to your Slack communicator(configuration in Shared.confile file)
# Language : Python (3.6.4)
#--------------------------------------------------------------------------


import airflow
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.models import DAG
from airflow.operators.slack_operator import SlackAPIPostOperator
from botocore.vendored import requests
from datetime import datetime, timedelta
import dask.dataframe as dd

import logging
from shared.config import slack_user ,slack_channel , slack_token
from slackclient import SlackClient

# variables
local_file_path = 'FILE_path'  # pass the file path from Airflow variables
use_column_list = ['tpep_dropoff_datetime' , 'trip_distance' ]

slack_notification_message = ''


#
def get_average_distance(ds, **kwargs):
    logging.info("> started executing get_average_duration() ")
    global slack_notification_message
    try:
        df = dd.read_csv(local_file_path, header=0, low_memory=False,
                         usecols=use_column_list)  # , nrows = '10' , ,usecols = ''
        df['year'] = dd.to_datetime(df['tpep_dropoff_datetime']).dt.year
        df['month'] = dd.to_datetime(df['tpep_dropoff_datetime']).dt.month
        average_trip_distance  = str(df.groupby(['year', 'month'])['trip_distance'].mean().compute().round(2))
        logging.info("Average Trip distance : {}".format(average_trip_distance))

        rolling_average_trip_distance = str(get_rooling_average_distance(df))
        logging.info("45 days Average Trip distance : {}".format(rolling_average_trip_distance))

        slack_notification_message  = """ Note >  Average Trip distance for a month : \n {} \n {} \n Note > from past 45 days Average Trip distance : \n{}""".format(average_trip_distance, '*'*50 ,rolling_average_trip_distance)


        return True

    except Exception as e:
        logging.error('ERROR !!: some issue with File in the location {} and error is {}'.format(local_file_path , str(e)))
        raise

def get_rooling_average_distance(df):
    logging.info("> started executing get_rooling_average_duration() ")
    max_rooling_trip_end_date = datetime.strptime(str(df['tpep_dropoff_datetime'].max().compute()),
                                                  '%Y-%m-%d %H:%M:%S') - timedelta(days=45)
    return df['trip_distance'].loc[df['tpep_dropoff_datetime'] >= str(max_rooling_trip_end_date)].mean().compute().round(2)


def get_slack_notification(ds, **kwargs):
    logging.info("> started executing get_slack_notification() ")
    global slack_notification_message
    try:
        print("*************** > ",slack_notification_message)
        requests.post(slack_token , json={"channel": slack_channel , "text": slack_notification_message })
        slack_push_notification = SlackAPIPostOperator(
            task_id='slack_notification_records',
            channel= slack_channel,
            token= slack_token,
            username= slack_user ,
            text="Hi Update from Airflow \n "+slack_notification_message,
            dag=dag
        )
        slack_push_notification.execute()
        return True

    except Exception as e:
        logging.error('ERROR: some issue with Slack configuration'.format(local_file_path, str(e)))
        raise

default_args = {
    'owner': 'Vinayaka CN',
    'depends_on_past': False,
    'start_date': datetime(2019, 3, 10),
    'retries': 1 ,
    'email': ['vinayaka.cn@informa.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retry_delay': timedelta(minutes=2)
}

dag = DAG(dag_id="get_taxi_average_trip_distance",
          default_args=default_args,
          schedule_interval= '00 10 * * *',
          catchup=False)


get_average_distance = \
    PythonOperator(task_id='get_average_distance',
                   provide_context=True,
                   python_callable= get_average_distance,
                   dag=dag)


get_slack_notification = \
    PythonOperator(task_id='get_slack_notification',
                   provide_context=True,
                   python_callable= get_slack_notification ,
                   dag=dag)

get_average_distance >> get_slack_notification
