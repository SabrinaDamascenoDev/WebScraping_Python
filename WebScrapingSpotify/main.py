import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time


driver = webdriver.Firefox()
driver.get("http://www.google.com")

driverLocal =driver.find_element(By.ID, "APjFqb")
driverLocal.send_keys("Musicas mais famosas Leandro e Leonardo")
driverLocal.send_keys(Keys.RETURN)

time(5)

assert "No results found." not in driver.page_source
driver.close()
