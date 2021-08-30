import os
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import time
import sys
import math
from myutils import zvFileUtil

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

# --------------------------------- Main ------------------------------------------------------
# https://www.searchpeoplefree.com/find/tabayoyong/ma/randolph
zvDriver.get("https://www.searchpeoplefree.com/find/"+ zaLastName.lower() +"/"+ zaState.lower() +"/"+ zaCity.lower())
# ------------------------------------------------------------------------------------------------------------

# ---- Main page ----

if '<LIST>' in zaLastName:
    zvNamFileName = zaLastName    
    zvNamFileName = zvNamFileName.split('<LIST>')[1]
    zvNamFileName = zvNamFileName.split('</LIST>')[0]
    zvNameLst = zvFileUtil(zvNamFileName, 'r')
    zvNameLst = zvNameLst.splitlines()

else:
    zvNameLst = [zaLastName]
    zvNameLst = zvNameLst.splitlines()

zvTotRes = zvDriver.page_source
zvTotRes = str(zvTotRes)

zvCnt = 1
zvTemp = zvTotRes.split('<article>')
for t in zvTemp:
    per = t.split('</article>')[0]
    
    try:
        nam = per.split('<h2 class="h2">')[1]
        nam = nam.split('<span>in '+ zaCity.lower().capitalize() +', '+ zaState.upper() +'</span>')[0]
        nam = nam.strip()

        adr = per.split('<address>')[1]        
        adr = adr.split('</address>')[0]
        adr = adr.split('>')[1]
        adr = adr.split('<')[0]
        adr = adr.strip()

        phnlst = []
        phnout = '{'

        phn = per.split('<i class="text-muted">Home telephone')[1]
        phn = phn.split('</ul>')[0]
        
        phnlst = phn.split('<a href="https://www.searchpeoplefree.com/phone-lookup/')        

        for i in range( len(phnlst)):
            phnlst[i] = phnlst[i].split('">')[0]
            if len(phnlst[i]) < 15:
                phnout = phnout + phnlst[i] + ","

        phnout = phnout[:-1]
        phnout = phnout + '}'

        zvOut = '{}|{}|{}'.format(adr, nam, phnout)        
        print(zvOut)


        zvCnt = zvCnt + 1
    except:
        print("*** error ***")

