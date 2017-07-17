#!/usr/bin/env python3
from threading import Thread
from collections import deque
from time import sleep
from math import floor

class Sensor:
    """ A sensor that logs its temperature for mean values """
    def __init__(self, path, refresh=5, temp_multiplicator=0.001):
        # Path to sensor
        self._path = path
        
        # Multiplicator to get celsius
        self._temp_multiplicator = temp_multiplicator

        # Refresh rate in seconds
        self._refresh = refresh
        
        # Log with last 60 temps (5min history with default 5s refresh)
        self.log = deque(maxlen=60)

        # Start background thread to keep log up to date
        self._updater = Thread(target=self._update_log)
        self._updater.daemon = True
        self._updater.start()

    def _update_log(self):
        """ Appends current temperatur to log and waits """
        while True:
            self.log.append(self.temp)
            sleep(self._refresh)

    def _update_temp(self):
        """ Fetch current temperatur """
        with open(self._path, 'r') as f:
            return int(f.read())

    def _get_average(self, n_elements):
        """ returns the average temperatur from log most recent/last n_elements """
        # Make sure its an integer and not zero
        assert(n_elements != 0)
        n_elements = int(floor(n_elements))

        # Return average of whole log if not enough data
        if len(self.log) < n_elements:
            return sum(self.log)/len(self.log)
        else:
            temp_sum = 0
            # Iterate over queue from behind
            # @todo: efficiency?
            for i in range(-1, -1*n_elements-1, -1):
                temp_sum += self.log[i]
            return temp_sum/n_elements

    @property
    def temp(self):
        """ Current temperature """
        return self._update_temp()*self._temp_multiplicator

    @property
    def temp_1m(self):
        """ Mean temperature of the last minute """
        # Elements needed for 60 second average
        elements = 60/self._refresh

        return self._get_average(elements)
        
        
    @property
    def temp_30s(self):
        """ Mean temperature of the last 30 seconds """
        return self._get_average(30/self._refresh)

