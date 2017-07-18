#!/usr/bin/env python3
from time import sleep
from fan import Fan
from sensor import Sensor

class PyFan_Controller:
    def __init__(self, refresh=5):
        self.__sensors = []
        self.__fans = []

        self._refresh = refresh

    def __enter__(self):
        """ return self to use PyFan_Controller with with statement """
        return self

    def __exit__(self, ext_type, exc_value, traceback):
        """ Set fans back to auto on exit """
        for fan, st in self.__fans:
            fan.set_auto()

    def add_sensor(self, sensor):
        self.__sensors.append(sensor)

    def add_fan(self, fan, strategy):
        self.__fans.append((fan, strategy))

    def start(self):
        # Give the sensor workers time to collect first data
        print('Take some time for initialization...')
        sleep(10)
        print('Ok, go!')

        # Start fan control loop
        while True:
            # Iterate over fans with associated strategy st
            for fan, strategy in self.__fans:
                strategy = strategy(fan, self.__sensors)
                level = strategy.level
                # Handle possible return values
                if level in range(0,8):
                    fan.set_level(level)
                elif level == "auto":
                    fan.set_auto()
                elif level == "off":
                    fan.set_off()
                else:
                    # Fallback for security reasons
                    fan.set_fullspeed()

                #print(level)

            sleep(self._refresh)

class PyFan_Strategy:
    """ Implements a strategy template to be used to determine the fan speed level """
    def __init__(self, fan, sensors):
        self._sensors = sensors
        self._fan = fan

    def get_fan_level(self):
        """ Override this to implement your strategy """
        pass

    def has_changed(self):
        """ @todo implemt something to determine if status chagned may level setter property ?"""
        pass

    @property
    def level(self):
        return self.get_fan_level()


class Permissive_Strategy(PyFan_Strategy):
    """ 
    temp_30s < 56 degree Celsius: Fan off 
    else: Fan auto
    """
    def get_fan_level(self):
        # if any of the 30s average temps goes above 56 set fan to auto
        for t in [s.temp_30s for s in self._sensors]:
            if t > 56:
                # exit loop and set fan to auto
                self._level = "auto"
                return self._level
            else:
                self._level = "off"

        return self._level

# Init fans
fan1 = Fan("/proc/acpi/ibm/fan")

# Init sensors
cpu1 = Sensor('/sys/devices/platform/coretemp.0/hwmon/hwmon2/temp1_input')
cpu2 = Sensor('/sys/devices/platform/coretemp.0/hwmon/hwmon2/temp2_input')
cpu3 = Sensor('/sys/devices/platform/coretemp.0/hwmon/hwmon2/temp3_input')
ssd = Sensor('/sys/devices/virtual/hwmon/hwmon0/temp1_input')

# Assign them to the controller
with PyFan_Controller() as controller:
    controller.add_sensor(cpu1)
    controller.add_sensor(cpu2)
    controller.add_sensor(cpu3)
    controller.add_sensor(ssd)
    controller.add_fan(fan1, Permissive_Strategy)
    controller.start()
