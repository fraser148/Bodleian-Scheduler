import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service

email_key = "exet5095@ox.ac.uk"
pwd = "VernVern01!!"

def highlight(element):
    # Highlights a Selenium webdriver element
    driver = element._parent
    def apply_style(s):
        driver.execute_script("arguments[0].setAttribute('style', arguments[1])", element, s)
    orignal_style = element.get_attribute('style')
    apply_style("border: 4px solid red")
    if (element.get_attribute("style")!=None):
        time.sleep(5)
    apply_style(orignal_style)

service = Service('chromedriver.exe')
service.start()
driver = webdriver.Remote(service.service_url)
driver.get('https://spacefinder.bodleian.ox.ac.uk/')
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
time.sleep(3)

calendar = driver.find_element_by_xpath("//span[@aria-label='January 30, 2021']")
calendar.click()
time.sleep(2)
slot = driver.find_element_by_xpath("//div[contains(h5, 'Lower Reading Room Desk Booking') and contains(p, '10:00')]/parent::*/descendant::a")
#highlight(slot)
slot.click()
time.sleep(2)
confirm = driver.find_element_by_name("ctl00$ContentPlaceHolder$Cart$CheckoutButton")
confirm.click()
time.sleep(3)
element = driver.find_element_by_xpath("//option[@label='Mr']")
element.click()

ids = {"FirstNameundefined":"Fraser","LastNameundefined":"Rennie","Phoneundefined":"1266833","Street2undefined":"Exeter","Emailundefined":"fraser.rennie@exeter.ox.ac.uk","ConfirmEmailundefined":"fraser.rennie@exeter.ox.ac.uk"}

for key in ids:
    element = driver.find_element_by_id(key)
    element.send_keys(ids[key])

time.sleep(10)
driver.close()