import os
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
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
chrome_options.add_argument('--headless')

# ---------------------------------- OS ---------------------------------
zvOs = os.name
if zvOs == 'posix':
    chrome_options.binary_location = r"/usr/bin/google-chrome"
    zvDrvPath = 'lnx/chromedriver'
else:
    chrome_options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    zvDrvPath = 'win\chromedriver.exe'

# --------------------------------- Main ------------------------------------------------------

zvDriver = webdriver.Chrome(zvDrvPath, options=chrome_options)

# dist_in.txt
# dist_ou.txt

# 314+N+Franklin+St,+Holbrook,+MA+02343

# -- SUNDAY
# https://www.google.com/maps/dir/Braintree,+Massachusetts/314+N+Franklin+St,+Holbrook,+MA+02343/@42.1853596,-71.0506132,13z/data=!3m1!4b1!4m18!4m17!1m5!1m1!1s0x89e37d4cf965306b:0xacb38d9361185dbd!2m2!1d-71.0040013!2d42.2079017!1m5!1m1!1s0x89e482cdf663349b:0x4e37bd0b99442642!2m2!1d-71.0071066!2d42.1628302!2m3!6e1!7e2!8j1685277000!3e0

# -- TUESDAY
# https://www.google.com/maps/dir/Braintree,+Massachusetts/314+N+Franklin+St,+Holbrook,+MA+02343/@42.1853596,-71.0467309,13z/data=!3m1!4b1!4m18!4m17!1m5!1m1!1s0x89e37d4cf965306b:0xacb38d9361185dbd!2m2!1d-71.0040013!2d42.2079017!1m5!1m1!1s0x89e482cdf663349b:0x4e37bd0b99442642!2m2!1d-71.0071066!2d42.1628302!2m3!6e1!7e2!8j1685473200!3e0

zvTownLst = zvFileUtil("dist_in.txt", "r")
zvTownLst = zvTownLst.splitlines()

zvFileUtil("dist_ou.txt", "w", 'TOWN|MIN|MAX' +'\n')

zvKh = r"/314+N+Franklin+St,+Holbrook,+MA+02343"

for t in zvTownLst:
    _town = str(t)
    print(_town)

    try:    
        time.sleep(1)
        zvUrl = r"https://www.google.com/maps/dir/Braintree,+Massachusetts/314+N+Franklin+St,+Holbrook,+MA+02343/@42.1853596,-71.0467309,13z/data=!3m1!4b1!4m18!4m17!1m5!1m1!1s0x89e37d4cf965306b:0xacb38d9361185dbd!2m2!1d-71.0040013!2d42.2079017!1m5!1m1!1s0x89e482cdf663349b:0x4e37bd0b99442642!2m2!1d-71.0071066!2d42.1628302!2m3!6e1!7e2!8j1685473200!3e0"

        zvDriver.get(zvUrl)
        time.sleep(1)

        # //*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/span/div/div/div/div[2]
        zvAdrTxtBox = zvDriver.find_element("xpath", r'//*[@id="sb_ifc50"]/input')
        zvAdrTxtBox.click()
        zvAdrTxtBox.send_keys(_town)
        zvAdrTxtBox.send_keys(Keys.ENTER)

        time.sleep(5)

        # //*[@id="section-directions-trip-title-0"]
        # //*[@id="section-directions-trip-0"]/div[1]/div[1]/div[1]/div[1]/span[2]/span
        zvDstTim = zvDriver.find_element("xpath", r'//*[@id="section-directions-trip-0"]/div[1]/div/div[1]/div[1]/span')
        zvDstTim = zvDstTim.text
        zvDstTim = str(zvDstTim)

        zvDstTim = zvDstTim.split('typically ')[1]
        # ABINGTON, MA
        # 10–14 min
        # . . .
        # ACTON, MA
        # 45 min to 1 hr 10 min
        zvMin = ''
        zvMax = ''
        zvDstOut = ''

        print(f'raw:"{zvDstTim}"')

        try:
            if "–" in zvDstTim:
                zvMin = zvDstTim.split("–")[0]
                zvMax = zvDstTim.split("–")[1]
                zvMax = zvMax.split(' ')[0]

            else:
                zvMin = zvDstTim.split(" to ")[0]
                zvMax = zvDstTim.split(" to ")[1]

                # print(f'b4 max:"{zvMax}", min:"{zvMin}"')
                # raw:"45 min to 1 hr 10 min"
                # b4 max:"1 hr 10 min", min:"45 min"

                if zvMin == "1 hr":
                    zvMin = "60"
                elif zvMin == "2 hr":
                    zvMin = "120"
                elif zvMin == "3 hr":
                    zvMin = "180"
                else:
                    zvMinH = 0
                    zvMinM = 0
                    if "hr" in zvMin:
                        zvMinH = zvMin.split(" hr")[0]
                        zvMinH = int(zvMinH)
                        zvMinH = zvMinH * 60
                        zvMinM = zvMin.split(" min")[0]
                        zvMinM = zvMinM.split("hr ")[1]
                        zvMinM = int(zvMinM)
                    else:
                        zvMinM = zvMin.split(" min")[0]
                        zvMinM = int(zvMinM)
                    zvMinT = zvMinH + zvMinM
                    zvMin = str(zvMinT)

                if zvMax == "1 hr":
                    zvMax = "60"
                elif zvMax == "2 hr":
                    zvMax = "120"
                elif zvMax == "3 hr":
                    zvMax = "180"
                else:
                    zvMaxH = 0
                    zvMaxM = 0
                    if "hr" in zvMax:
                        zvMaxH = zvMax.split(" hr")[0]
                        zvMaxH = int(zvMaxH)
                        zvMaxH = zvMaxH * 60
                        zvMaxM = zvMax.split(" min")[0]
                        zvMaxM = zvMaxM.split("hr ")[1]
                        zvMaxM = int(zvMaxM)
                    else:
                        zvMaxM = zvMax.split(" min")[0]
                        zvMaxM = int(zvMaxM)
                    zvMaxT = zvMaxH + zvMaxM
                    zvMax = str(zvMaxT)
            zvDstOut = str(zvMin) +"|"+ str(zvMax)
        except:
            zvDstOut = zvDstTim

        zvFileUtil("dist_ou.txt", "a", _town +'|'+ str(zvDstOut) +'\n')

    except:
        zvFileUtil("dist_ou.txt", "a", _town +'|error\n')
