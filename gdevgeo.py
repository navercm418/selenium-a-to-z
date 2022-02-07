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

zvAdId = ""
zvAdr1 = ""
zvZip1 = ""
zvLat1 = ""
zvLon1 = ""

zvAdrLst = zvFileUtil("/home/andy/CodeProjects/selenium-a-to-z/geoadr.txt", 'r')
zvAdrLst = zvAdrLst.splitlines()

for a in zvAdrLst:    

    zvAdId = a.split('|')[0]
    zvSta1 = a.split('|')[1]
    zvSta1 = zvSta1.upper()
    zvAdr1 = a.split('|')[2]
    zvAdr1Mtch = zvAdr1.split(' ')[0]
    zvAdr1Mtch = zvAdr1Mtch + zvAdr1.split(' ')[1]
    zvZip1 = a.split('|')[3]
    zvLat1 = a.split('|')[4]
    zvLon1 = a.split('|')[5]

    zvDriver.get("https://www.mapdevelopers.com/geocode_tool.php")

    
    zvAdrIn = zvDriver.find_element_by_xpath(r'//*[@id="address"]')
    zvAdrIn.send_keys(zvAdr1)

    zvDriver.find_element_by_xpath(r'//*[@id="search-form"]/div[1]/span[2]/button').click()

    time.sleep(2)

    zvLat = zvDriver.find_element_by_xpath(r'//*[@id="display_lat"]')
    zvLat = zvLat.text
    zvLon = zvDriver.find_element_by_xpath(r'//*[@id="display_lng"]')
    zvLon = zvLon.text
    zvZip = zvDriver.find_element_by_xpath(r'//*[@id="display_zip"]')
    zvZip = zvZip.text
    zvZip = zvZip.split('-')[0]
    zvSta = zvDriver.find_element_by_xpath(r'//*[@id="display_city"]')
    zvSta = zvSta.text
    zvSta = str(zvSta)
    zvSta = zvSta.upper()
    zvAdr = zvDriver.find_element_by_xpath(r'//*[@id="display_address"]')
    zvAdr = zvAdr.text
    zvAdr = str(zvAdr)
    zvAdr = zvAdr.upper()
    zvAdrMtch = zvAdr.split(' ')[0]
    zvAdrMtch = zvAdrMtch + zvAdr1.split(' ')[1]

    print('cty1: {}, cty2:{} | adr1:{}, adr2:{}'.format(zvSta1, zvSta, zvAdr1Mtch, zvAdrMtch))

    if zvAdr1Mtch == zvAdrMtch:
        print('{}|{}|{}|{}'.format(zvAdr1, zvLat, zvLon, zvZip))
        zvFileUtil("/home/andy/CodeProjects/selenium-a-to-z/geoadr_out.txt", 'a', '{}|{}|{}|{}|{}\n'.format(zvAdId, zvAdr1, zvZip, zvLat, zvLon))

    else:
        print('{}|{}|{}|{} ... orig'.format(zvAdr1, zvLat1, zvLon1, zvZip1))
        zvFileUtil("/home/andy/CodeProjects/selenium-a-to-z/geoadr_out.txt", 'a', '{}|{}|{}|{}|{}\n'.format(zvAdId, zvAdr1, zvZip1, zvLat1, zvLon1))

