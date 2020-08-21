#!python3

from selenium import webdriver

zvDrvPath = 'chromedriver.exe'
zvDriver = webdriver.Chrome(zvDrvPath)

zvDriver.get("https://login.ezproxy.bpl.org/login?url=https://www.atozdatabases.com/search")

