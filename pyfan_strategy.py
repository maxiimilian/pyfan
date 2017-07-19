from fan import Fan
from sensor import Sensor

class PyFan_Strategy:
    """ 
    Implements a strategy template to be used to determine the fan speed level 
    
    private sensors to provide access to temperatur data
    public fan to control fan
    """

    # Static list with all the bound fans to prevent double bindings
    bound_fans = []

    def __init__(self, fan, sensors):
        if fan not in self.bound_fans:
            self.fan = fan
            self.bound_fans.append(fan)
        else:
            raise ImproperlyConfigured('You cannot bind this fan to another strategy.')

        # Convert to array if only one sensor was passed 
        if isinstance(sensors, Sensor):
            sensors = [sensors, ]

        self._sensors = sensors

    def add_sensor(self, sensor):
        """ add sensor to strategy """
        self._sensors.append(sensor)

    def set_fan_level(self):
        """ Override this to implement your strategy """
        pass

    def has_changed(self):
        """ @todo implemt something to determine if status chagned may level setter property ?"""
        pass

    @property
    def level(self):
        return self.fan.get_level()


class ImproperlyConfigured(Exception):
    """ Exception to show when configuration is wrong """
    def __init__(self, msg):
        self.msg = msg
