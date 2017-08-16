from Client.Sensors.ctx_sensor import ContextSwitchSensor
from Client.Sensors.network_sensor import NetworkSensor
from Client.Sensors.interrupts_sensor import InterruptsSensor
from Client.Sensors.pids_sensor import ProcessIdsSensor


def activate_sensors(interval, queue):
    """ get the interval between measurements of the sensor and the queue to add the samples to and
        generate all the sensors available """
    sensors = []

    sensors.append(ContextSwitchSensor(interval, queue))
    sensors.append(InterruptsSensor(interval, queue))
    sensors.append(ProcessIdsSensor(interval, queue))
    sensors.append(NetworkSensor(interval, queue))

    for sensor in sensors:
        sensor.start()