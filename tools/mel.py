import os
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import time
import sys
import math
from myutils import zvFileUtil
from selenium.webdriver.common.action_chains import ActionChains

# \\wsl$\Ubuntu\home\andy\CodeProjects\selenium-a-to-z spf.py '<LIST>filename</LIST>' Burlington MA
# python3 spf.py '<LIST>filename</LIST>' Burlington MA

# ---------- Args ----------
zaLastName = sys.argv[1]
zaCity = sys.argv[2]
zaState = sys.argv[3]
zvArgCnt = 0

# --------------------------------------------- SETUP --------------------------------------------------------
# -- options:
#   --headless
#   log-level=3
chrome_options = Options()
for a in sys.argv:
    if zvArgCnt > 3:
        chrome_options.add_argument(a)
    zvArgCnt = zvArgCnt + 1

# ---------------------------------- OS ---------------------------------
zvOs = os.name
if zvOs == 'posix':
    chrome_options.binary_location = r"/usr/bin/google-chrome"
    zvDrvPath = 'lnx/chromedriver'
else:
    chrome_options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    zvDrvPath = 'win/chromedriver.exe'

zvDriver = webdriver.Chrome(zvDrvPath, options=chrome_options)

# -----------------------------------------------
zvFilName = zaCity +'_'+ zaState +'_Results.txt'
# -----------------------------------------------

if '<LIST>' in zaLastName:
    zvNamFileName = zaLastName    
    zvNamFileName = zvNamFileName.split('<LIST>')[1]
    zvNamFileName = zvNamFileName.split('</LIST>')[0]
    zvNameLst = zvFileUtil(zvNamFileName, 'r')
    zvNameLst = zvNameLst.splitlines()

    for n in zvNameLst:
        # https://www.melissa.com/v2/lookups/personatorsearch/?name=tabayoyong&city=randolph&state=MA&postalCode=
        zvName = str(n)
        zvDriver.get("https://www.melissa.com/v2/lookups/personatorsearch/?name="+ zvName.lower() +"&city="+ zaCity.lower() +"&state="+ zaState.upper() +"&postalCode=")
        # ------------------------------------------------------------------------------------------------------------

        print(n)

        # ---- Main page ----
        zvTotRes = zvDriver.page_source
        zvTotRes = str(zvTotRes)
        print(zvTotRes)

else:
    # https://www.searchpeoplefree.com/find/tabayoyong/ma/randolph
    zvName = zaLastName
    zvDriver.get("https://www.melissa.com/v2/lookups/personatorsearch/?name="+ zvName.lower() +"&city="+ zaCity.lower() +"&state="+ zaState.upper() +"&postalCode=")
    # ------------------------------------------------------------------------------------------------------------
    # <table
    print(zvName)

    # ---- Main page ----
    zvTotRes = zvDriver.page_source
    zvTotRes = str(zvTotRes)

    zvTmp = zvTotRes.split('<tbody>')[1]
    zvTmp = zvTmp.split('</tbody>')[0]
    # <tr class="item">
    zvTmpLst = zvTmp.split('<tr class="item">')

    zvCnt = 1
    for t in zvTmpLst:
        print(t)
        '''zvNam = t.split('fullName=')[1]
        zvNam = zvNam.split('">')[1]
        zvNam = zvNam.split('<')[0]

        zvAdr = t.split('makaddressinfo')[1]
        zvAdr = zvAdr.split('">')[1]

        zvAdrStr = zvAdr.split('<')[1]

        zvAdrCty = zvAdr.split('<td>')[1]
        zvAdrCty = zvAdr.split('</td>')[0]

        zvAdrSta = zvAdr.split('<td class="text-center">')[1]
        zvAdrZip = zvAdrSta.split('<td class="text-center">')[1]
        zvAdrSta = zvAdrSta.split('</td>')[0]
        zvAdrZip = zvAdrZip.split('</td>')[0]

        zvAdr = zvAdrStr +', '+ zvAdrCty +', '+ zvAdrSta +' '+ zvAdrZip

        zvOut = 'adr: {}, nam: {}'.format(zvAdr, zvNam)

        print(zvOut)'''