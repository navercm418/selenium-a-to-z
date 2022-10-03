from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import time
import sys
import math
from myutils import zvFileUtil


# --------------------------------------------- SETUP --------------------------------------------------------
# -- options:
#   --headless
#   log-level=3
chrome_options = Options()
for a in sys.argv:    
    chrome_options.add_argument(a)
    
chrome_options.binary_location = r"/mnt/c/Program Files/Google/Chrome/Application/chrome.exe"
# chrome_options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

zvDrvPath = '/mnt/c/Users/amcc4/CodeProjects/selenium-a-to-z/chromedriver.exe'
zvDriver = webdriver.Chrome(zvDrvPath, options=chrome_options)
zvDriver.get("https://login.ezproxy.bpl.org/login?url=https://www.atozdatabases.com/search")
