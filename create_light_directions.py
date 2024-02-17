from coordinates import *
from datetime import datetime, timedelta
from angle import get_ra_dec
from astropy.coordinates import SkyCoord
import astropy.units as u

start_date = datetime(2023, 10, 23)
end_date = datetime(2023, 11, 6)

current_date = start_date
date_list = []

while current_date <= end_date:
    date_list.append(current_date.strftime("%m-%d-%Y") + "_22.55.00")
    current_date += timedelta(days=1)

print(date_list)

def ra_dec_to_spherical(ra, dec):
    coord = SkyCoord(ra, dec, unit=(u.hourangle, u.deg))
    theta = coord.ra.degree
    phi = 90 - coord.dec.degree
    return theta, phi

SE = 150 * (10 ** 6) # km
ME = 384400 # km

file = open("light_directions_copernicus.txt", "w")

for date in date_list:
    ra1, dec1, ra2, dec2 = get_ra_dec(date)
    theta1, phi1 = ra_dec_to_spherical(ra1, dec1)
    theta2, phi2 = ra_dec_to_spherical(ra2, dec2)
    pos1 = SphericalCoordinate(ME, theta1, phi1).to_rectangular()
    pos2 = SphericalCoordinate(SE, theta2, phi2).to_rectangular()
    pos = RectangularCoordinate(pos2.x - pos1.x, pos2.y - pos1.y, pos2.z - pos1.z)
    pos.normalize()
    file.write(f"{pos.x} {pos.y} {pos.z}\n")
    print(f"{pos.x} {pos.y} {pos.z}")
file.close()
