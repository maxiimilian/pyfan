from time import sleep

class PyFan_Controller:
    def __init__(self, refresh=5):
        self.__strategies = []

        self._refresh = refresh

    def __enter__(self):
        """ return self to use PyFan_Controller with with statement """
        return self

    def __exit__(self, ext_type, exc_value, traceback):
        """ Set fans back to auto on exit """
        for s in self.__strategies:
            s.fan.set_auto()

    def add_strategy(self, strategy):
        self.__strategies.append(strategy)

    def start(self):
        # Give the sensor workers time to collect first data
        print('Take some time for initialization...')
        sleep(10)
        print('Ok, go!')

        # Start fan control loop
        while True:
            # Set fan levels according to each strategy
            for strategy in self.__strategies:
                strategy.set_fan_level()

            sleep(self._refresh)
