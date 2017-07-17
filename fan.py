#!/usr/bin/env python3
import re

class Fan:
    """ A fan """
    def __init__(self, path):
        self.path = path

    def _set_level(self, level):
        """ Sets the fan level. NO VALIDATION! BE CAREFUL! """
        with open(self.path, 'w+') as f:
            f.write('level {}'.format(level))

    def set_fullspeed(self):
        """ set fan to full speed """
        self._set_level('full-speed')

    def set_off(self):
        """ shortcut for level 0 """
        self.set_level(0)

    def set_auto(self):
        """ Set fan to auto """
        self._set_level('auto')

    def set_level(self, level):
        """ Set fan to given integer level (1-7) """
        if level in range(0, 8):
            self._set_level(int(level))

    def get_level(self):
        """ Returns the current fan level """
        with open(self.path, 'r') as f:
            # Get level line 
            level = re.search('level:(.*)', f.read())

            # Extract level setting
            # @todo: Proper regex
            if level:
                level = level.group().split(':')[-1]
                return level.strip()
            else:
                return False

    def get_rpm(self):
        """ Returns the current rpms """
        with open(self.path, 'r') as f:
            # Get speed line 
            speed = re.search('speed:\s+\d+', f.read())

            # Extract rpm
            if speed:
                rpm = re.search('\d+', speed.group())
                return int(rpm.group())
            else:
                return False
