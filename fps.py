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
zvDriver.get("https://www.fastpeoplesearch.com")

# --------------------------------------------- MAIN PAGE --------------------------------------------------------

# -- name
zvLstNam = zvDriver.find_element_by_xpath(r'//*[@id="search-name-name"]')
zvLstNam.send_keys(zaLastName)

# -- city
zvCtyStr = zaCity +', '+ zaState
zvCtySte = zvDriver.find_element_by_xpath(r'//*[@id="search-name-address"]')
zvCtySte.send_keys(zvCtyStr)

# -- click
zvDriver.find_element_by_xpath(r'//*[@id="form-search-name"]/div[3]/button[2]').click()

# ----------------------------------------- Results ------------------------------------------------------------

# -- blocks
zvBlks = zvDriver.find_elements_by_css_selector("div.card-block")

for p in zvBlks:

    zvBlkTxt = str(p.text)

    zvBlkCtySte = zvBlkTxt.split("Age:")[0]
    zvBlkCtySte = zvBlkCtySte.split("\n")[2]

    zvFmtBlkCty = zvBlkCtySte.upper()
    zvFmtBlkCty = zvFmtBlkCty.strip()

    zvFmtArgCty = zvCtyStr.upper()
    zvFmtArgCty = zvFmtArgCty.strip()

    if zvFmtArgCty == zvFmtBlkCty:
        
        zvBlkNam = zvBlkTxt.split("Goes By ")[1]
        zvBlkNam = zvBlkNam.split("\n")[0]

        zvBlkAdr = zvBlkTxt.split("Current Home Address:\n")[1]
        zvBlkAdr = zvBlkAdr.split("\nPast Addresses:")[0]
        zvBlkAdr = zvBlkAdr.replace("\n", ", ")

        zvBlkPhn = zvBlkTxt.split("telephone numbers for")[1]
        zvBlkPhn = zvBlkPhn.split(". ")[1]
        zvBlkPhn = zvBlkPhn.split("AKA:")[0]
        zvBlkPhn = zvBlkPhn.replace("\n", ",")
        zvBlkPhn = "[" + zvBlkPhn
        zvBlkPhn = zvBlkPhn + "]"

        zvBlkRel = zvBlkTxt.split("Relatives: ")[1]
        zvBlkRel = zvBlkRel.split(". ")[1]
        zvBlkRel = zvBlkRel.split("\n")[0]
        zvBlkRel = zvBlkRel.replace(" • ", ",")
        zvBlkRel = "[" + zvBlkRel
        zvBlkRel = zvBlkRel + "]"

        zvOut = zvBlkNam +"|"+ zvBlkAdr +"|"+ zvBlkPhn +"|"+ zvBlkRel +"\n"

        zvFileUtil('test.txt', 'a', zvOut)
