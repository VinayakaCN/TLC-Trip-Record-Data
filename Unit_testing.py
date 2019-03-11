#-------------------------------------------------------------------------
# Author: Vinayaka CN
# Date: 10 Mar 2019
# Content : Below Program Tests the Airflow job "Yello_taxies_trip_length.py"
# Language : Python (3.6.4)
#--------------------------------------------------------------------------

import Yellow_taxies_Average_trip_length

unit_test_file_path = 'UnitTesting/sample_unit_testing_data.CSV'
test_slack_message = 'Hi this is a test message'

#below is the test data for unit testing in the file "sample_unit_testing_data.CSV"

"""
tpep_dropoff_datetime    ,trip_distance
2018-01-01 00:15:40     ,5.0
2018-01-01 00:15:40     ,5.0
2018-01-01 00:15:40     ,0.0
2018-02-02 00:15:40     ,6.0
2018-02-02 00:15:40     ,6.0
"""

def test_average_distance(unit_test_file_path):
    print(Yello_taxies_Average_trip_length2.get_average_distance(unit_test_file_path))
    print( '\n'+("*"*100+'\n' )*3 )

    print("########### expected out put should be as below #########################")

    print(""" Note >  Average Trip distance for a month :
         year  month
        2018  1        5.0
              2        6.0
        Name: trip_distance, dtype: float64
         **************************************************
         Note > from past 45 days Average Trip distance :
        5.5""")

test_average_distance()

# kindly configure the Slack config file under shared folder
def test_slack_notification(test_slack_message):
    get_slack_notification(test_slack_message)
    Print("The avove tesst message should have been reached your slack channel, kindly check")