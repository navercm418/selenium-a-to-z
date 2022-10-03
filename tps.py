#!python3
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import time
import sys
import math
from myutils import zvFileUtil


# ---------- Args ----------
zaLastName = sys.argv[1]
zaCity = sys.argv[2]
zaState = sys.argv[3]
zvArgCnt = 0
# --------------------------

# --------------------------------------------- SETUP --------------------------------------------------------
# -- options:
#   --headless
#   log-level=3
chrome_options = Options()
for a in sys.argv:
    if zvArgCnt > 3:
        chrome_options.add_argument(a)
    zvArgCnt = zvArgCnt + 1
chrome_options.binary_location = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

zvDrvPath = 'chromedriver.exe'
zvDriver = webdriver.Chrome(zvDrvPath, options=chrome_options)
zvDriver.get("https://www.truepeoplesearch.com/")
# ------------------------------------------------------------------------------------------------------------

# ---- Main page ----
# -- name
zvLstNam = zvDriver.find_element_by_xpath(r'//*[@id="id-d-n"]')
zvLstNam.send_keys(zaLastName)

# -- city
zvCtyStr = zaCity +', '+ zaState
zvCtySte = zvDriver.find_element_by_xpath(r'//*[@id="id-d-loc-name"]')
zvCtySte.send_keys(zvCtyStr)

# -- click
zvDriver.find_element_by_xpath(r'//*[@id="btnSubmit-d-n"]').click()
# ----------------------------------------------------------------------------------------------------------

# ---- Results Page ----
# -- results & Pages
zvTotRes = zvDriver.page_source
zvTotRes = str(zvTotRes)
try:
    zvTotRes = zvTotRes.split('<div class="col-10 mt-1">')[1]
    zvTotRes = zvTotRes.split(' records')[0]
    zvTotRes = int(zvTotRes)
    zvTotPgs = zvTotRes / 9
    zvTotPgs = math.ceil(zvTotPgs)
except:
    zvTotRes = 0
    zvTotPgs = 0

print('***', zvTotRes, 'RECORDS', zvTotPgs,'PAGES FOUND ***')
# ------------------------------------------------------------------------------------------------------------

# ---- GetRes Def ----
def GetRes(blks):

    global zvCtyStr

    _totblk = blks + 4
    _curblk = 4

    while  _curblk <= _totblk:

        _blkstr = str(_curblk)

        print("on block:", _curblk)        

        zvUprCtySt = zvCtyStr.upper()
        zvBoxCtySt = zvDriver.find_element_by_xpath(r"/html/body/div[3]/div/div[2]/div["+ _blkstr +r"]/div[1]/div[1]/div[3]/span[2]").text
        zvBoxCtySt = str(zvBoxCtySt)
        zvBoxCtySt = zvBoxCtySt.upper()

        print('city:', zvBoxCtySt, r"/html/body/div[3]/div/div[2]/div["+ _blkstr +r"]/div[1]/div[1]/div[3]/span[2]")

        if zvUprCtySt == zvBoxCtySt:
            print("CLICK:", r"/html/body/div[3]/div/div[2]/div["+ _blkstr +r"]/div[1]/div[2]/a")
            zvDriver.find_element_by_xpath(r"/html/body/div[3]/div/div[2]/div["+ _blkstr +r"]/div[1]/div[2]/a").click()

            zvCurName = zvDriver.find_element_by_xpath(r'//*[@id="personDetails"]/div[1]/div/span[1]').text
            zvCurAddr = zvDriver.find_element_by_xpath(r'//*[@id="personDetails"]/div[4]/div[2]').text
            zvCurPhns = zvDriver.find_element_by_xpath(r'//*[@id="personDetails"]/div[6]/div[2]').text

            zvCurAddr = str(zvCurAddr)
            zvCurAddr = zvCurAddr.split("Current Address")[1]
            zvCurAddr = zvCurAddr.split("Map")[0]

            zvCurPhns = str(zvCurPhns)
            zvCurPhns = zvCurPhns.split("Phone Numbers")[1]
            zvCurPhns = zvCurPhns.split("View All Phone Numbers")[0]

            zvOut = zvCurName +' - '+ zvCurAddr +' - '+ zvCurPhns

            zvFileUtil('test.txt', 'a', zvOut)

            zvDriver.execute_script("window.history.go(-1)")

        else:
            print("doesnt match")

        _curblk = _curblk + 1



# ---- Results Loop ----
zvPgsLft = zvTotPgs
zvCurPag = 1

# -- pages loop
while zvCurPag <= zvTotPgs:

    print('on page:', zvCurPag)

    if zvCurPag == 1:
        GetRes(9)
    else:
        GetRes(10)

    zvCurPag = zvCurPag + 1    
    zvDriver.find_element_by_xpath(r'//*[@id="btnNextPage"]').click()
