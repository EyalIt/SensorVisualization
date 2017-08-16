import psutil

from Client.Sensors import sample
from Client.Sensors.sensor import Sensor


class NetworkSensor(Sensor):
    def __init__(self, interval, queue):
        Sensor.__init__(self, interval, queue)

        self.set_name("Network Sensor")

    def measure(self):
        measurement = psutil.net_connections()
        self._queue.put(sample.create(self.getName(), str(len(measurement))))