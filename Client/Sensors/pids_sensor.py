import psutil

from Client.Sensors import sample
from Client.Sensors.sensor import Sensor


class ProcessIdsSensor(Sensor):
    def __init__(self, interval, queue):
        Sensor.__init__(self, interval, queue)

        self.set_name("Process IDs Sensor")

    def measure(self):
        measurement = psutil.pids()
        self._queue.put(sample.create(self.getName(), str(len(measurement))))

