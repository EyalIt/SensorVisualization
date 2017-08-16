import json
import requests

def generate_url(url, port):
    """ generate the url to use in order to dispatch a new sensor sample to the server """
    return "http://" + url + ":" + str(port) + "/update_sensors"

def communicate_sensor_operation(queue, url, port):
    """ listen on the queue and dispatch a sensor sample once available """
    while (True):
        item = queue.get()
        process_item(item, url, port)
        queue.task_done()

def process_item(item, url, port):
    # get the server api for sending the sensor data
    addr = generate_url(url, port)

    # convert the data to JSON format and dispatch
    json_str = json.dumps([item])
    requests.post(addr, data = None, json = json_str)
