import os
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import time
import sys
import math
from myutils import zvFileUtil

# \\wsl$\Ubuntu\home\andy\CodeProjects\selenium-a-to-z AtoZ.py '<LIST>top5names.txt</LIST>' Bedford Massachusetts
# python.exe AtoZ.py '<LIST>names_list.txt</LIST>' Malden Massachusetts --headless log-level=3
# started 4:10pm

# --------------------------------------------- SETUP --------------------------------------------------------
# -- options:
#   --headless log-level=3
chrome_options = Options()
for a in sys.argv:
    chrome_options.add_argument(a)

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

zvAdr1 = ""
zvAdr2 = ""

zvAdrLst = zvFileUtil("/home/andy/CodeProjects/selenium-a-to-z/geoadr.txt", 'r')
zvAdrLst = zvAdrLst.splitlines()

for a in zvAdrLst:    

    zvAdr1 = str(a)
    zvAdr2 = zvAdr1.replace(" ", "+")

    zvDriver.get("https://www.google.com/maps/place/"+ zvAdr2)

    time.sleep(5)
    zvGeoInf = zvDriver.current_url

    zvLatLon = zvGeoInf.split("/@")[1]
    zvZip = zvGeoInf.split("/@")[0]
    zvZip = zvZip.rsplit("+", 1)[1]

    zvLat = zvLatLon.split(",")[0]
    zvLon = zvLatLon.split(",")[1]
    zvLon = zvLon.split(",")[0]

    zvFileUtil("/home/andy/CodeProjects/selenium-a-to-z/geoadr_out.txt", 'a', '{}|{}|{}|{}\n'.format(zvAdr1, zvLat, zvLon, zvZip))
