#!python3
"""Gets lat, lon & zip using selenium"""

import sys
# import os
import time
# import math
from selenium import webdriver
# from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from myutils import zvFileUtil

# \\wsl$\Ubuntu\home\andy\CodeProjects\selenium-a-to-z AtoZ.py '<LIST>top5names.txt</LIST>' Bedford Massachusetts
# python.exe AtoZ.py '<LIST>names_list.txt</LIST>' Malden Massachusetts --headless log-level=3
# started 4:10pm

# --------------------------------------------- SETUP ---------------------------------------------
# options...
# --headless log-level=3
chrome_options = Options()
for a in sys.argv:
    chrome_options.add_argument(a)

# ---------------------------------- OS ---------------------------------
# zvOs = os.name
# if zvOs == 'posix':
#     chrome_options.binary_location = r"/usr/bin/google-chrome"
#     zvDrvPath = '/home/CodeProjects/selenium-a-to-z/lnx/chromedriver'
# else:
#     chrome_options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
#     zvDrvPath = 'win/chromedriver.exe'
# --------------------------------- Main ------------------------------------------------------
service = Service(executable_path=r'C:\CodeProjects\selenium-a-to-z\win\chromedriver.exe')
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
zvDriver = webdriver.Chrome(service=service, options=options)

# zvDriver = webdriver.Chrome(zvDrvPath, options=chrome_options)

zvAdId = ""
zvAdr1 = ""
zvZip1 = ""
zvLat1 = ""
zvLon1 = ""

zvAdrLst = zvFileUtil(r"C:\CodeProjects\selenium-a-to-z\tools\geoadr.txt", 'r')
zvAdrLst = zvAdrLst.splitlines()

for a in zvAdrLst:
    zvAdId = a.split('|')[0]
    zvSta1 = a.split('|')[1]
    zvSta1 = zvSta1.upper()
    zvAdr1 = a.split('|')[2]
    zvAdr1Mtch = zvAdr1.split(' ')[0]
    zvAdr1Mtch = zvAdr1Mtch + zvAdr1.split(' ')[1]
    zvAdr1Mtch = zvAdr1Mtch.upper()
    zvZip1 = a.split('|')[3]
    zvLat1 = a.split('|')[4]
    zvLon1 = a.split('|')[5]

    zvDriver.get("https://www.bing.com/maps/")

    zvAdrIn = zvDriver.find_element("xpath", r'//*[@id="maps_sb"]')
    zvAdrIn.send_keys(zvAdr1)
    zvDriver.find_element("xpath", r'//*[@id="maps_sb_container"]/div[1]/div[2]/a').click()

    time.sleep(2)

    try:
        #zvAdr = zvDriver.find_element("xpath", (r'//*[@id="container"]/div[3]/div[1]/div[1]/div[2]/div[2]/div/div/div[2]/div[3]/div/div/div/div/div[2]/div/div/div/div/div/div[2]/div/div[1]/div/div[2]')
        zvAdrBlk = zvDriver.find_element("id", "container")
        zvAdrBlk = zvAdrBlk.text
        zvAdrSpl = str(zvAdrBlk)
        zvAdrSpl = zvAdrSpl.split("Bird's Eye")[1]
        zvAdrSpl = zvAdrSpl.split("\n")[1]
        zvAdrSpl = zvAdrSpl.split("\n")[0]
        zvAdr = zvAdrSpl
        zvAdrSpl = zvAdrSpl.split(' ')[0] + zvAdrSpl.split(' ')[1]
        zvAdrSpl = zvAdrSpl.upper()

        zvZip = zvAdr.rsplit(' ', 1)[1]

        zvLatLon = zvAdrBlk.split('Search nearby')[1]
        zvLatLon = zvLatLon.split('\n')[2]
        zvLat = zvLatLon.split(', ')[0]
        zvLon = zvLatLon.split(', ')[1]

        if zvAdr1Mtch == zvAdrSpl:
            print( f'{zvAdr1}|{zvLat}|{zvLon}|{zvZip}')
            zvFileUtil(r"C:\CodeProjects\selenium-a-to-z\tools\geoadr_out.txt", 'a', f'{zvAdId}|{zvAdr1}|{zvZip}|{zvLat}|{zvLon}\n')

        else:
            print(f'{zvAdr1}|{zvLat1}|{zvLon1}|{zvZip1} ... orig')
            zvFileUtil(r"C:\CodeProjects\selenium-a-to-z\tools\geoadr_out.txt", 'a', f'{zvAdId}|{zvAdr1}|{zvZip1}|{zvLat1}|{zvLon1}|orig\n')

    except Exception:
        print('2nd attempt . . .')
        try:
            time.sleep(2)
            #zvAdr = zvDriver.find_element("xpath", (r'//*[@id="container"]/div[3]/div[1]/div[1]/div[2]/div[2]/div/div/div[2]/div[3]/div/div/div/div/div[2]/div/div/div/div/div/div[2]/div/div[1]/div/div[2]')
            zvAdrBlk = zvDriver.find_element("id", "container")
            zvAdrBlk = zvAdrBlk.text
            zvAdrSpl = str(zvAdrBlk)
            zvAdrSpl = zvAdrSpl.split("Bird's Eye")[1]
            zvAdrSpl = zvAdrSpl.split("\n")[1]
            zvAdrSpl = zvAdrSpl.split("\n")[0]
            zvAdr = zvAdrSpl
            zvAdrSpl = zvAdrSpl.split(' ')[0] + zvAdrSpl.split(' ')[1]
            zvAdrSpl = zvAdrSpl.upper()

            zvZip = zvAdr.rsplit(' ', 1)[1]

            zvLatLon = zvAdrBlk.split('Search nearby')[1]
            zvLatLon = zvLatLon.split('\n')[2]
            zvLat = zvLatLon.split(', ')[0]
            zvLon = zvLatLon.split(', ')[1]

            if zvAdr1Mtch == zvAdrSpl:
                print(f'{zvAdr1}|{zvLat}|{zvLon}|{zvZip}')
                zvFileUtil(r"C:\CodeProjects\selenium-a-to-z\tools\geoadr_out.txt", 'a', f'{zvAdId}|{zvAdr1}|{zvZip}|{zvLat}|{zvLon}\n')

            else:
                print(f'{zvAdr1}|{zvLat1}|{zvLon1}|{zvZip1} ... orig')
                zvFileUtil(r"C:\CodeProjects\selenium-a-to-z\tools\geoadr_out.txt", 'a', f'{zvAdId}|{zvAdr1}|{zvZip1}|{zvLat1}|{zvLon1}|orig\n')
        except Exception:
            print(f'{zvAdr1}|{zvLat1}|{zvLon1}|{zvZip1} ... failed')
            zvFileUtil(r"C:\CodeProjects\selenium-a-to-z\tools\geoadr_out.txt", 'a', f'{zvAdId}|{zvAdr1}|{zvZip1}|{zvLat1}|{zvLon1}|err\n')
