import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service

email_key = "exet5095@ox.ac.uk"
pwd = "VernVern01!!"

service = Service('chromedriver.exe')
service.start()
driver = webdriver.Remote(service.service_url)
driver.get('https://spacefinder.bodleian.ox.ac.uk/')
elem = driver.find_elements_by_xpath("//*[@type='email']")#put here the content you have put in Notepad, ie the XPath
time.sleep(1)
email = driver.find_element_by_id('i0116')
email.send_keys(email_key)
submit = driver.find_element_by_id("idSIButton9")
submit.click()
time.sleep(1)
password = driver.find_element_by_id("i0118")
password.send_keys(pwd)
time.sleep(1)
signin = driver.find_element_by_id("idSIButton9")
signin.click()


time.sleep(10)
driver.close()

temp = "ctl00$ContentPlaceHolder$Cart$CheckoutButton"
# hey buddy