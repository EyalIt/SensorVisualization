import Queue
import http_dispatcher

from threading import Thread
from Client.Sensors import sensor_generator


def start(url, port):
    # initialize all sensor threads
    queue = Queue.Queue()
    generator = sensor_generator.activate_sensors(0.1, queue)

    # start the http dispatcher (listening on the queue and dispatch once an item is available)
    httpDispatcher = Thread(target = http_dispatcher.communicate_sensor_operation, args = (queue, url, port))
    httpDispatcher.start()