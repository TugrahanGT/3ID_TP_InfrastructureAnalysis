import psutil
from threading import Thread
import os

class ThreadWithReturnValue(Thread):
    
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args,
                                                **self._kwargs)
    def join(self, *args):
        Thread.join(self, *args)
        return self._return


class HardwareUsage():
    def __str__(self):
        return f"Current CPU usage is {self.get_cpu_usage()} and RAM usage is: {self.get_ram_usage()}"

    def get_cpu_usage(self, number_of_data_points = 3):
        captured_cpu_usage = []
        for _ in range(number_of_data_points):
            captured_cpu_usage.append(psutil.cpu_percent(2))
        return captured_cpu_usage
    
    def get_ram_usage(self, number_of_data_points = 3):
        captured_ram_usage = []
        for _ in range(number_of_data_points):
            captured_ram_usage.append(psutil.virtual_memory()[2])
        return captured_ram_usage
    
def get_hardware_statistics():
    hardwareUsage = HardwareUsage()
    t1 = ThreadWithReturnValue(target=hardwareUsage.get_cpu_usage, args=(10,))
    t2 = ThreadWithReturnValue(target=hardwareUsage.get_ram_usage, args=(10,))

    t1.start()
    t2.start()

    cpu_usage_statistics = t1.join()
    ram_usage_statistics = t2.join()

    return {
        "CPU Usage": cpu_usage_statistics,
        "RAM Usage": ram_usage_statistics
    }