from angle import angle
import math

# Get the angle between the Moon and the Sun
date = "05-01-2021_00.00.00" # Example
angle = angle(date)
print(angle)

SE = 150 * (10 ** 6) # km
ME = 384400 # km

theta = math.asin((SE * math.sin(angle * math.pi / 180)) / math.sqrt((SE ** 2) + (ME ** 2) - (2 * SE * ME * math.cos(angle * math.pi / 180)))) * 180 / math.pi
print(theta)
