#!python3
import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time 

# start
zvStartTime = datetime.datetime.now()

# --------------------------------------------- SETUP --------------------------------------------------------
zvDrvPath = 'chromedriver.exe'
zvDriver = webdriver.Chrome(zvDrvPath)
zvDriver.get("https://login.ezproxy.bpl.org/login?url=https://www.atozdatabases.com/search")

# --------------------------------------------- LOGIN --------------------------------------------------------
username = zvDriver.find_element_by_name("user")
password = zvDriver.find_element_by_name("pass")
username.send_keys("20000001303814")
password.send_keys("1234")
# //*[@id="post-170332"]/div/table/tbody/tr[3]/td[2]/input
zvDriver.find_element_by_xpath(r'//*[@id="post-170332"]/div/table/tbody/tr[3]/td[2]/input').click()

if zvDriver.title == 'Session Timed Out | AtoZdatabases':
    # 
    zvDriver.find_element_by_xpath(r'//*[@id="total-wrapper"]/div/div/div/p/a').click()
    
# ---------------------------------------------- SEARCH ------------------------------------------------------
if zvDriver.title == 'Search | AtoZdatabases':
    # //*[@id="hpdeux_fap_state"]
    select = Select(zvDriver.find_element_by_xpath(r'//*[@id="hpdeux_fap_state"]'))
    select.select_by_visible_text('Massachusetts')
    zvLstNam = zvDriver.find_element_by_xpath(r'//*[@id="hpdeux_fap_ln"]')
    zvCity = zvDriver.find_element_by_xpath(r'//*[@id="hpdeux_fap_city"]')
    zvLstNam.send_keys("Tabayoyong")
    zvCity.send_keys("Randolph")
    # //*[@id="search_deux_fap"]
    zvDriver.find_element_by_xpath(r'//*[@id="search_deux_fap"]').click()

    # ---------------------------------------------- RESULTS ------------------------------------------------------
    time.sleep(5)
    zvCnt = 1
    zvResTab = zvDriver.find_element_by_xpath(r'//*[@id="results_table"]')
    print(zvResTab.text)

# //*[@id="results_table"]
# //*[@id="results_table"]/tbody/tr[1]
# //*[@id="results_table"]/tbody/tr[2]
# //*[@id="results_table"]/tbody/tr[3]







# end
zvEndTime = datetime.datetime.now()
zvTotalTime = zvEndTime - zvStartTime
print('done in:', zvTotalTime)
