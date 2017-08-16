import threading

from abc import ABCMeta, abstractmethod


class Sensor(threading.Thread):
    __metaclass__ = ABCMeta


    def __init__(self, interval, queue):
        threading.Thread.__init__(self)
        self._finished = threading.Event()

        self._interval = interval
        self._queue = queue

    def set_name(self, name):
        self.setName(name)

    def run(self):
        """ initiate a worker thread that will measure the required sensor every predefined frequency """

        while (self._finished.is_set() == False):
            try:
                # perform the sensor measurement
                self.measure()
            except Exception, err:
                print err

            # sleep for the predefined amount interval
            self._finished.wait(self._interval)

    def stop(self):
        """ set the internal flag, indicating that the thread should stop """
        self._finished.set()

    @abstractmethod
    def measure(self):
        """ measure the output of the sensor. abstract method that should implemented by the derived classes """
        pass