#!/usr/bin/env python3
from fan import Fan
from sensor import Sensor
from controller import PyFan_Controller
from pyfan_strategy import PyFan_Strategy

class Permissive_Strategy(PyFan_Strategy):
    """ 
    temp_30s < 56 degree Celsius: Fan off 
    temp_30s < 60 degree Celsius: Fan 1 
    temp_30s < 65 degree Celsius: Fan 2 
    else: Fan auto
    """
    def set_fan_level(self):
        # if any of the 30s average temps goes above 56 enable fan
        for t in [s.temp_30s for s in self._sensors]:
            if t > 65:
                self.fan.set_auto()
                return self._level
            if t > 60:
                self.fan.set_level(2)
                return
            if t > 56:
                self.fan.set_level(1)
                return

        # Switch fan off if none of the conditions were met
        self.fan.set_off()

# Init fans
fan1 = Fan("/proc/acpi/ibm/fan")

# Init sensors
cpu1 = Sensor('/sys/devices/platform/coretemp.0/hwmon/hwmon2/temp1_input')
cpu2 = Sensor('/sys/devices/platform/coretemp.0/hwmon/hwmon2/temp2_input')
cpu3 = Sensor('/sys/devices/platform/coretemp.0/hwmon/hwmon2/temp3_input')
ssd = Sensor('/sys/devices/virtual/hwmon/hwmon0/temp1_input')

# Start controller with strategy
with PyFan_Controller() as c:
    c.add_strategy(Permissive_Strategy(
        fan1,
        (cpu1, cpu2, cpu3, ssd)
    ))
    c.start()
