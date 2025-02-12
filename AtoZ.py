import os
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
import sys
import math
from myutils import zvFileUtil

# \\wsl.localhost\Ubuntu-20.04\home\andy\CodeProjects\selenium-a-to-z AtoZ.py '<LIST>top5names.txt</LIST>' Bedford Massachusetts
# python.exe AtoZ.py '<LIST>names\names_list.txt</LIST>' Hull Massachusetts --headless log-level=3
# started 4:10pm

# ---------- Args ----------
zaLastName = sys.argv[1]
zaCity = sys.argv[2]
zaState = sys.argv[3]
zvArgCnt = 0

# \\wsl$\Ubuntu\home\andy\CodeProjects\selenium-a-to-z AtoZ.py '<LIST>top5names.txt</LIST>' Bedford Massachusetts
# python.exe AtoZ.py '<LIST>names_list.txt</LIST>' Malden Massachusetts --headless log-level=3
# started 4:10pm

# --------------------------------------------- SETUP --------------------------------------------------------
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
options.add_argument('log-level=3')
zvDriver = webdriver.Chrome(service=service, options=options)

# zvDriver = webdriver.Chrome(zvDrvPath, options=chrome_options) 

# --------------------------------- Main ------------------------------------------------------
# zvDriver = webdriver.Chrome(zvDrvPath, options=chrome_options)
zvDriver.get("https://login.ezproxy.bpl.org/login?url=https://www.atozdatabases.com/search")
time.sleep(5)

# --------------------------------------------- LOGIN --------------------------------------------------------
username = zvDriver.find_element("name", "user")
password = zvDriver.find_element("name", "pass")
username.send_keys("20000001727244")
password.send_keys("1234")

zvDriver.find_element("xpath", r'/html/body/section/div[3]/div/div[3]/div/div/article/div/table/tbody/tr[3]/td[2]/input').click()

# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------

# zvState = 'Massachusetts'
# zvTown = 'bedford'

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

        zvDriver.get("https://login.ezproxy.bpl.org/login?url=https://www.atozdatabases.com/search")

        time.sleep(1)

        zvName = n
        print(zvName)

        if zvDriver.title == 'Session Timed Out | AtoZdatabases':
            zvDriver.find_element("xpath", r'//*[@id="total-wrapper"]/div/div/div/p/a').click()
            
        # ---------------------------------------------- SEARCH ------------------------------------------------------
        if zvDriver.title == 'Search | AtoZdatabases':
            
            zvState = Select(zvDriver.find_element("xpath", r'//*[@id="hpdeux_fap_state"]'))
            zvState.select_by_visible_text(zaState)

            zvLstNam = zvDriver.find_element("xpath", r'//*[@id="hpdeux_fap_ln"]')
            zvLstNam.send_keys(zvName)

            zvCity = zvDriver.find_element("xpath", r'//*[@id="hpdeux_fap_city"]')    
            zvCity.send_keys(zaCity)
            
            zvDriver.find_element("xpath", r'//*[@id="search_deux_fap"]').click()

            time.sleep(5)

        # ---------------------------------------------- RESULTS ------------------------------------------------------
            try:
                zvPopUp = zvDriver.find_element("xpath", r'//*[@id="deux_error-dialog"]')        
                print('*** NO RECORDS FOUND ***')
            except:

                zvCnt = zvDriver.find_element("xpath", r'//*[@id="total_records"]')
                zvCnt = zvCnt.text
                try:
                    zvCnt = int(zvCnt)
                except:
                    zvCnt = 1

                print('***', zvCnt, 'RECORDS FOUND ***')

                if zvCnt > 25:
                    zvPerPg = Select(zvDriver.find_element("xpath", r'//*[@id="recordFilter"]'))
                    zvPerPg.select_by_visible_text('100')

                    zvPgs = zvCnt / 100
                    zvPgs = math.ceil(zvPgs)

                    zvPgCnt = 1

                    while zvPgCnt <= zvPgs:
                        
                        time.sleep(5)

                        try:
                            
                            zvDriver.find_element("xpath", r'/html/body/div[3]/div[1]/a').click()
                            
                            zvResTab = zvDriver.find_element("xpath", r'//*[@id="results_table"]')
                            zvOut = zvResTab.text
                            zvOut = str(zvOut)
                            zvOut = zvOut.split('Legal Name')[1]
                            zvOut = zvOut.replace('Residential Record ','')
                            zvOut = zvOut + '\n'
                            zvFileUtil('test.txt', 'a', zvOut)

                        except:
                            
                            zvResTab = zvDriver.find_element("xpath", r'//*[@id="results_table"]')
                            
                            zvOut = zvResTab.text
                            zvOut = str(zvOut)
                            zvOut = zvOut.split('Legal Name')[1]
                            zvOut = zvOut.replace('Residential Record ','')
                            zvOut = zvOut + '\n'                    
                            zvFileUtil(zvFilName, 'a', zvOut)

                        zvDriver.find_element("xpath", r'//*[@id="resultFormId"]/div[1]/div[1]/div[3]/div/div[1]/div[3]').click()
                        zvPgCnt = zvPgCnt + 1

                else:
                    zvResTab = zvDriver.find_element("xpath", r'//*[@id="results_table"]')
                    zvOut = zvResTab.text
                    zvOut = str(zvOut)
                    zvOut = zvOut.split('Legal Name')[1]
                    zvOut = zvOut.replace('Residential Record ','')
                    zvOut = zvOut + '\n'
                    zvFileUtil(zvFilName, 'a', zvOut)

else:
    zvName = zaLastName
        
    zvDriver.get("https://login.ezproxy.bpl.org/login?url=https://www.atozdatabases.com/search")

    time.sleep(1)

    print(zvName)

    if zvDriver.title == 'Session Timed Out | AtoZdatabases':
        zvDriver.find_element("xpath", r'//*[@id="total-wrapper"]/div/div/div/p/a').click()
        
    # ---------------------------------------------- SEARCH ------------------------------------------------------
    if zvDriver.title == 'Search | AtoZdatabases':
        
        zvState = Select(zvDriver.find_element("xpath", r'//*[@id="hpdeux_fap_state"]'))
        zvState.select_by_visible_text(zaState)

        zvLstNam = zvDriver.find_element("xpath", r'//*[@id="hpdeux_fap_ln"]')
        zvLstNam.send_keys(zvName)

        zvCity = zvDriver.find_element("xpath", r'//*[@id="hpdeux_fap_city"]')    
        zvCity.send_keys(zaCity)
        
        zvDriver.find_element("xpath", r'//*[@id="search_deux_fap"]').click()

        time.sleep(5)

    # ---------------------------------------------- RESULTS ------------------------------------------------------
        try:
            zvPopUp = zvDriver.find_element("xpath", r'//*[@id="deux_error-dialog"]')        
            print('*** NO RECORDS FOUND ***')
        except:

            zvCnt = zvDriver.find_element("xpath", r'//*[@id="total_records"]')
            zvCnt = zvCnt.text
            try:
                zvCnt = int(zvCnt)
            except:
                zvCnt = '?'

            print('***', zvCnt, 'RECORDS FOUND ***')

            if zvCnt > 25:
                zvPerPg = Select(zvDriver.find_element("xpath", r'//*[@id="recordFilter"]'))
                zvPerPg.select_by_visible_text('100')

                zvPgs = zvCnt / 100
                zvPgs = math.ceil(zvPgs)

                zvPgCnt = 1

                while zvPgCnt <= zvPgs:
                    
                    time.sleep(5)

                    try:
                        
                        zvDriver.find_element("xpath", r'/html/body/div[3]/div[1]/a').click()
                        
                        zvResTab = zvDriver.find_element("xpath", r'//*[@id="results_table"]')
                        zvOut = zvResTab.text
                        zvOut = str(zvOut)
                        zvOut = zvOut.split('Legal Name')[1]
                        zvOut = zvOut.replace('Residential Record ','')
                        zvOut = zvOut + '\n'
                        zvFileUtil('test.txt', 'a', zvOut)

                    except:
                        
                        zvResTab = zvDriver.find_element("xpath", r'//*[@id="results_table"]')
                        
                        zvOut = zvResTab.text
                        zvOut = str(zvOut)
                        zvOut = zvOut.split('Legal Name')[1]
                        zvOut = zvOut.replace('Residential Record ','')
                        zvOut = zvOut + '\n'                    
                        zvFileUtil(zvFilName, 'a', zvOut)

                    zvDriver.find_element("xpath", r'//*[@id="resultFormId"]/div[1]/div[1]/div[3]/div/div[1]/div[3]').click()
                    zvPgCnt = zvPgCnt + 1

            else:
                zvResTab = zvDriver.find_element("xpath", r'//*[@id="results_table"]')
                zvOut = zvResTab.text
                zvOut = str(zvOut)
                zvOut = zvOut.split('Legal Name')[1]
                zvOut = zvOut.replace('Residential Record ','')
                zvOut = zvOut + '\n'
                zvFileUtil(zvFilName, 'a', zvOut)

# //*[@id="results_table"]
# //*[@id="results_table"]/tbody/tr[1]
# //*[@id="results_table"]/tbody/tr[2]
# //*[@id="results_table"]/tbody/tr[3]
