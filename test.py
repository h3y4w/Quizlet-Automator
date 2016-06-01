from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

drive = webdriver.Firefox()

drive.get('http://www.quizlet.com')
login_link = drive.find_element_by_css_selector('[class^="login activate link"]').get_attribute('href')
print login_link



drive.quit()
