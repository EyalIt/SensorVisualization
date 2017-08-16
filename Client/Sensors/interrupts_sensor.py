import psutil

from Client.Sensors import sample
from Client.Sensors.sensor import Sensor


class InterruptsSensor(Sensor):
    def __init__(self, interval, queue):
        Sensor.__init__(self, interval, queue)

        self.set_name("Interrupts Sensor")

    def measure(self):
        measurement = psutil.cpu_stats()
        self._queue.put(sample.create(self.getName(), str(measurement.interrupts)))