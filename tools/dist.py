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
chrome_options.add_argument('--headless')

# ---------------------------------- OS ---------------------------------
zvOs = os.name
if zvOs == 'posix':
    chrome_options.binary_location = r"/usr/bin/google-chrome"
    zvDrvPath = 'lnx/chromedriver'
else:
    chrome_options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    zvDrvPath = '/home/andy/CodeProjects/selenium-a-to-z/win/chromedriver.exe'

# --------------------------------- Main ------------------------------------------------------

zvDriver = webdriver.Chrome(zvDrvPath, options=chrome_options)

# dist_in.txt
# dist_ou.txt
# https://www.google.com/maps/dir/Bondsville,+MA+01009/559+Pine+St,+Lowell,+MA+01851
# 314+N+Franklin+St,+Holbrook,+MA+02343

zvTownLst = zvFileUtil("dist_in.txt", "r")
zvTownLst = zvTownLst.splitlines()

# zvKh = r"/314+N+Franklin+St,+Holbrook,+MA+02343"
# zvKh = r"/559+Pine+St,+Lowell,+MA+01851"
zvKh = r"/1672+Washington+St,+Newton+MA"

for t in zvTownLst:
    _town = str(t)
    print(_town)
    
    time.sleep(1)
    zvUrl = r"https://www.google.com/maps/dir/"+ _town + zvKh
    print(zvUrl)
    # zvDriver.get(r"https://www.google.com/maps/dir/"+ _town +r"/314+N+Franklin+St,+Holbrook,+MA+02343")
    zvDriver.get(zvUrl)
    time.sleep(1)

    # //*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/span/div/div/div/div[2]
    zvDriver.find_element_by_xpath(r'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/span/div/div/div/div[2]').click()

    # //*[@id=":2"]/div
    zvDriver.find_element_by_xpath(r'//*[@id=":2"]/div').click()
    time.sleep(1)

    # //*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/span[1]/input
    zvDriver.find_element_by_xpath(r'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/span[1]/input').click()
    time.sleep(1)

    # //*[@id=":q"]/div
    zvDriver.find_element_by_xpath(r'//*[@id=":q"]/div').click()
    time.sleep(1)

    # //*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/span[2]/span[2]/button[2]
    zvDriver.find_element_by_xpath(r'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/span[2]/span[2]/button[2]').click()
    time.sleep(1)
    zvDriver.find_element_by_xpath(r'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/span[2]/span[2]/button[2]').click()
    time.sleep(1)
    zvDriver.find_element_by_xpath(r'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/span[2]/span[2]/button[2]').click()
    time.sleep(2)

    # //*[@id="section-directions-trip-0"]/div[1]/div[1]/div[1]/div[1]/span[2]/span
    zvDstTim = zvDriver.find_element_by_xpath(r'//*[@id="section-directions-trip-0"]/div[1]/div[1]/div[1]/div[1]/span[2]/span')
    zvDstTim = zvDstTim.text
    zvDstTim = str(zvDstTim)
    zvDstTim = zvDstTim.split(' - ')[0]

    zvFileUtil("dist_ou.txt", "a", _town +'~'+ str(zvDstTim) +'\n')
    print(' . . . ', zvDstTim)


'''
for t in zvTownLst:
    _town = str(t)
    print(_town)
    
    # zvDriver.get(r"https://www.google.com/maps/dir/"+ _town +r"/314+N+Franklin+St,+Holbrook,+MA+02343")
    # /html/body/div[3]/div[9]/div[8]/div/div[1]/div/div/div[5]/div[1]/div/div[1]/div[1]/div[1]/span[1]
    #zvDist = zvDriver.find_element_by_xpath(r'/html/body/div[3]/div[9]/div[8]/div/div[1]/div/div/div[5]/div[1]/div/div[1]/div[1]/div[1]/span[1]').text
    #zvFileUtil("dist_ou.txt", "a", _town +'~'+ str(zvDist) +'\n')
'''