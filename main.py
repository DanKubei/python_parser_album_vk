from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import requests
import datetime
from sys import argv

if len(argv) < 2:
    url = input("url: ")
else:
    url = argv[1]
base_url = ""
for i in url.split("/")[0:-1]:
    base_url += i + "/"
base_url = base_url[0:-1]

print("Starting driver")
driver = webdriver.Chrome()
driver.get(url)
print("Finding photos...")
container = driver.find_element(by=By.CLASS_NAME, value="photos_container")
photos = container.find_element(by=By.TAG_NAME, value="div")
photo_button = photos.find_element(by=By.TAG_NAME, value="a")
photo_button.click()
time.sleep(1)
try:
    close_button = driver.find_element(by=By.CLASS_NAME, value="UnauthActionBox__close")
except:
    pass
if close_button != None:
    close_button.click()

time.sleep(1)
counter = driver.find_element(by=By.CLASS_NAME, value="pv_counter")
dt = str(datetime.datetime.now()).replace(":", "-").replace(" ","")
print("Starting download")
last_src = ""
while True:
    counts = counter.text.split(" из ")
    print('Download: {0} - {1:3}%'.format(counter.text, int(int(counts[0])/int(counts[1]) * 100)), end='\r')
    if int(counts[0]) == int(counts[1]):
        print()
        print('Downloading complete')
        break
    cycle_counter = 0
    while True:
        photo_container = driver.find_element(by=By.ID, value="pv_photo")
        photo = photo_container.find_element(by=By.TAG_NAME, value="img")
        cycle_counter += 1
        if last_src != photo.get_attribute("src") or cycle_counter == 10:
            last_src = photo.get_attribute("src")
            break
        time.sleep(0.1)
    req = requests.get(photo.get_attribute("src"))
    driver.execute_script("Photoview.show(false, cur.pvIndex + 1, event);")
    with open("Downloads/" + dt + "-" + counts[0] + ".jpg", "wb") as file:
        file.write(req.content)
        file.close()

driver.quit()