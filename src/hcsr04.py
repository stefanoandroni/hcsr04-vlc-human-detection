from gpiozero import DistanceSensor

import time
from statistics import median, mean

'''
    TODO
    For improved accuracy, use the pigpio pin driver rather than the 
    default RPi.GPIO driver (pigpio uses DMA sampling for much more 
    precise edge timing). This is particularly relevant if you’re using 
    Pi 1 or Pi Zero. See Changing the pin factory for further information.
'''
class HCSR04:
    def __init__(self, trigger_pin, echo_pin, num_floor_measurements):
        # Initialize sensor
        self.sensor = DistanceSensor(echo=echo_pin, trigger=trigger_pin)
        self.sensor.max_distance = 4
        # Initialize num_floor_measurements
        self.num_floor_measurements = num_floor_measurements

    def measure_floor_distance(self):
        distances = []
        for _ in range(self.num_floor_measurements):
            distance = self.measure_distance()
            distances.append(distance)
            time.sleep(0.1)  # Add a short delay between measurements

        # mean_distance = mean(distances)
        median_distance = median(distances)
        return median_distance
    
    def measure_distance(self):
        return round(self.sensor.distance * 100) # (cm)
