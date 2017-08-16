from Common.json_keys import *

def create(sensor_name, sensor_value):
    return {SENSOR_DATA_KEY: {SENSOR_ORIGIN_KEY: sensor_name, SENSOR_VALUE_KEY: sensor_value}}