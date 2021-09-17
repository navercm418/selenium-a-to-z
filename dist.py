import os
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import time
import sys
import math
from myutils import zvFileUtil

# ------------------------- file utility ------------------------------------------
# -- example: zvFileUtil("Help.txt", "r")
def zvFileUtil(file, action, data=None):
    _file = open(file, action)    
    _wrt = data
    if action == "w":
        _file.write(_wrt)
    if action == "a":
        _file.write(_wrt)
    if action == "r":
        _wrt = _file.read()
        return _wrt
    _file.close()
# ----------------------------------------------------------------------------------

# --------------------------------------------- SETUP --------------------------------------------------------
# -- options:
#   --headless log-level=3
chrome_options = Options()
chrome_options.add_argument('log-level=3')

# ---------------------------------- OS ---------------------------------
zvOs = os.name
if zvOs == 'posix':
    chrome_options.binary_location = r"/usr/bin/google-chrome"
    zvDrvPath = 'lnx/chromedriver'
else:
    chrome_options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    zvDrvPath = 'win/chromedriver.exe'

# --------------------------------- Main ------------------------------------------------------

zvDriver = webdriver.Chrome(zvDrvPath, options=chrome_options)

# dist_in.txt
# dist_ou.txt
# https://www.google.com/maps/dir/Bondsville,+MA+01009/559+Pine+St,+Lowell,+MA+01851

zvTownLst = zvFileUtil("dist_in.txt", "r")
zvTownLst = zvTownLst.splitlines()
for t in zvTownLst:
    _town = str(t)
    zvDriver.get(r"https://www.google.com/maps/dir/"+ _town +r"/559+Pine+St,+Lowell,+MA+01851")


