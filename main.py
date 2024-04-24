from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time
import requests
import datetime

url = input("url: ")
base_url = ""
for i in url.split("/")[0:-1]:
    base_url += i + "/"
base_url = base_url[0:-1]

driver = webdriver.Chrome()
driver.get(url)

container = driver.find_element(by=By.CLASS_NAME, value="AlbumPage__photos")
#photos = container.find_element(by=By.TAG_NAME, value="div")
photo_button = photos.find_element(by=By.TAG_NAME, value="a")
photo_button.click()
time.sleep(0.1)
close_button = driver.find_element(by=By.CLASS_NAME, value="UnauthActionBox__close")
if close_button != None:
    close_button.click()

time.sleep(0.5)
counter = driver.find_element(by=By.CLASS_NAME, value="pv_counter")

while True:
    counts = counter.text.split(" из ")
    if int(counts[0]) == int(counts[1]):
        break
    driver.execute_script("Photoview.show(false, cur.pvIndex + 1, event);")
    time.sleep(0.1)
    photo_container = driver.find_element(by=By.ID, value="pv_photo")
    photo = photo_container.find_element(by=By.TAG_NAME, value="img")
    dt = str(datetime.datetime.now()).replace(":", "-").replace(" ","")
    print(photo.get_attribute("src"))
    req = requests.get(photo.get_attribute("src"))
    with open("Downloads/" + dt + "-" + counts[0] + ".jpg", "wb") as file:
        file.write(req.content)
        file.close()
    time.sleep(0.1)

time.sleep(1)

driver.quit()