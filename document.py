from Common.json_keys import *

DOC_SENSOR_DATA_KEY = 'Sensor Data'
DOC_SENSOR_ORIGIN_KEY = 'Origin'
DOC_SENSOR_VALUE_KEY = 'Value'

DOC_CLIENT_ID_KEY = 'Client Id'

def create(sample, remote_addr):
        try:
            # extract the data from the sensor sample received by the user
            sensor_data = sample[SENSOR_DATA_KEY]
            sensor_origin = sensor_data[SENSOR_ORIGIN_KEY]
            sensor_value = sensor_data[SENSOR_VALUE_KEY]

            # add the data to the dictionary
            document = {}
            document.update({DOC_SENSOR_DATA_KEY : {DOC_SENSOR_ORIGIN_KEY : sensor_origin, DOC_SENSOR_VALUE_KEY : sensor_value}})
            document.update({DOC_CLIENT_ID_KEY : remote_addr})

            return document
        except Exception, err:
            print err