from astropy.coordinates import SkyCoord
import astropy.units as u
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
import chromedriver_autoinstaller
import math

def get_ra_dec(date):
    """
    Get the RA and Dec of the sun at a given date and time.
    :param date: The date of the observation in the format MM-DD-YYYY_HH.MM.SS.
    :return: The RA and Dec of the sun at the given date and time in the format (RA_moon, Dec_moon, RA_sun, Dec_sun)
    """
    chromedriver_autoinstaller.install()
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    time = date.split('_')[1].split(".")
    date = date.split('_')[0].split("-")
    print(f"Getting RA and Dec for Moon on {date[0]}/{date[1]}/{date[2]} at {time[0]}:{time[1]}:{time[2]}")
    driver.get("https://www.heavens-above.com/moon.aspx")
    driver.find_element(By.ID, "ctl00_cph1_TimeSelectionControl1_comboYear").send_keys(date[2])
    month_select = Select(driver.find_element(By.ID, "ctl00_cph1_TimeSelectionControl1_comboMonth"))
    month_select.select_by_value(date[0].lstrip("0"))
    day_select = Select(driver.find_element(By.ID, "ctl00_cph1_TimeSelectionControl1_comboDay"))
    day_select.select_by_value(date[1].lstrip("0"))
    driver.find_element(By.ID, "ctl00_cph1_TimeSelectionControl1_txtTime").clear()
    driver.find_element(By.ID, "ctl00_cph1_TimeSelectionControl1_txtTime").send_keys(":".join(time))
    driver.find_element(By.ID, "ctl00_cph1_TimeSelectionControl1_btnSubmit").click()
    ra1 = driver.find_element(By.ID, "ctl00_cph1_lblRA").text
    dec1 = driver.find_element(By.ID, "ctl00_cph1_lblDec").text
    print(ra1, dec1)
    driver.get("https://www.heavens-above.com/sun.aspx")
    driver.find_element(By.ID, "ctl00_cph1_TimeSelectionControl1_comboYear").send_keys(date[2])
    month_select = Select(driver.find_element(By.ID, "ctl00_cph1_TimeSelectionControl1_comboMonth"))
    month_select.select_by_value(date[0].lstrip("0"))
    day_select = Select(driver.find_element(By.ID, "ctl00_cph1_TimeSelectionControl1_comboDay"))
    day_select.select_by_value(date[1].lstrip("0"))
    driver.find_element(By.ID, "ctl00_cph1_TimeSelectionControl1_txtTime").clear()
    driver.find_element(By.ID, "ctl00_cph1_TimeSelectionControl1_txtTime").send_keys(":".join(time))
    driver.find_element(By.ID, "ctl00_cph1_TimeSelectionControl1_btnSubmit").click()
    ra2 = driver.find_element(By.ID, "ctl00_cph1_lblRA").text
    dec2 = driver.find_element(By.ID, "ctl00_cph1_lblDec").text
    print(ra2, dec2)
    driver.quit()
    return ra1, dec1, ra2, dec2

def angle(date):
    """
    Calculate the angle between the sun and moon as viewed from earth at a given date and time.

    Parameters
    ----------
    date : str
        The date of the observation in the format MM-DD-YYYY_HH.MM.SS.

    Returns
    -------
    angle : float
        The angle between the two points in degrees.
    """
    # Calculate the angle
    ra1, dec1, ra2, dec2 = get_ra_dec(date)
    coord1 = SkyCoord(ra1, dec1, unit=(u.hourangle, u.deg))
    coord2 = SkyCoord(ra2, dec2, unit=(u.hourangle, u.deg))
    angle = coord1.separation(coord2)
    return angle.degree

def sun_moon_earth_angle(sem: float) -> float:
    """
    Calculate the angle between the sun and earth as viewed from the moon.
    :param sem: The angle between the sun and moon as viewed from earth in degrees.
    :return: The angle between the sun and earth as viewed from the moon in degrees.
    """
    SE = 150 * (10 ** 6) # km
    ME = 384400 # km
    theta = math.asin((SE * math.sin(sem * math.pi / 180)) / math.sqrt((SE ** 2) + (ME ** 2) - (2 * SE * ME * math.cos(sem * math.pi / 180)))) * 180 / math.pi
    return theta

if __name__ == "__main__":
    date = "01-01-2021_00.00.00"
    time = date.split('_')[1].split(".")
    date2 = date.split('_')[0].split("-")
    print(f"On {date2[0]}/{date2[1]}/{date2[2]} at {time[0]}:{time[1]}:{time[2]} there is a {angle(date)}° separation between the sun and moon as viewed from the earth.")