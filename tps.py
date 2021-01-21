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

# ---- Results Loop ----
zvBtnStrtNum = 4
zvCurBtnNum = 0
zvBtnClkNum = zvBtnStrtNum + zvCurBtnNum
zvBtnClkStr = str(zvBtnClkNum)

zvDriver.find_element_by_xpath(r"/html/body/div[3]/div/div[2]/div["+ zvBtnClkStr +r"]/div[1]/div[2]/a").click()

zvDriver.execute_script("window.history.go(-1)")
