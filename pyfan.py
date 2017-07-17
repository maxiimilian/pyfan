from time import sleep
from fan import Fan
from sensor import Sensor

class PyFan_Controller:
    def __init__(self, refresh=5):
        self.__sensors = []
        self.__fans = []

        self._refresh = refresh

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
            for f,st in self.__fans:
                # Mean of mean.. a little ugly but only for testing
                temp_30s = sum([s.temp_30s for s in self.__sensors])/len(self.__sensors)
                if temp_30s>55:
                    print("Mean temp_30s is {} -> fan auto".format(temp_30s))
                    f.set_auto()
                else:
                    print("Mean temp_30s is {} -> fan off".format(temp_30s))
                    f.set_off()

            sleep(self._refresh)

class PyFan_Strategy:
    """ Implements a strategy to use to determine the fan speed level """
    pass

class Permissive_Strategy(PyFan_Strategy):
    """ 
    temp_30s < 55 degree Celsius: Fan off 
    else: Fan auto
    """
    pass

# Init fans
fan1 = Fan("/proc/acpi/ibm/fan")

# Init sensors
cpu1 = Sensor('/sys/devices/platform/coretemp.0/hwmon/hwmon2/temp1_input')
cpu2 = Sensor('/sys/devices/platform/coretemp.0/hwmon/hwmon2/temp2_input')
cpu3 = Sensor('/sys/devices/platform/coretemp.0/hwmon/hwmon2/temp3_input')
ssd = Sensor('/sys/devices/virtual/hwmon/hwmon0/temp1_input')

# Assign them to the controller
controller = PyFan_Controller()
controller.add_sensor(cpu1)
controller.add_sensor(cpu2)
controller.add_sensor(cpu3)
controller.add_sensor(ssd)
controller.add_fan(fan1, Permissive_Strategy)
controller.start()
