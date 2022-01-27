# Author: Ryan Scarbrough
# LE: 1/26/22
# THIS FILE GETS THE ASSIGNMENTS FROM COVENANT'S WEBSITE AND PUTS THEM IN ORDER BY DATE (CLOSE->FURTHER)

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import login # login info
import time
import os # for windows driver

def getAsgn():
    # LINUX CHROMIUM DRIVER
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(executable_path=r'/usr/bin/chromedriver', chrome_options=options)
    # WINDOWS FIREFOX DRIVER
    # os.environ['MOZ_HEADLESS'] = '1'
    # driver = webdriver.Firefox(executable_path=r'C:\Programming\geckodriver.exe')

    driver.get(login.alt_url)

    usernameElement = driver.find_element_by_id("pseudonym_session_unique_id")
    usernameElement.send_keys(login.cov_username)
    passwordElement = driver.find_element_by_id("pseudonym_session_password")
    passwordElement.send_keys(login.cov_password)

    driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div/div[1]/div/div/div/div/div/div[2]/form[1]/div[3]/div[2]/button').click() # login button
    time.sleep(1) # give time to load
    try:
        driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[2]/div[1]/div/div/div[3]/div/div[9]/div/button').click() # clicking the 'load more' button
        time.sleep(1) # give time to load
    except:
        print('No more assignments to load')

    # getting *all* the assignment data
    asgn_class = driver.find_elements_by_class_name("ergWt_bGBk")
    text = []
    for i in asgn_class:
        text.append(i.text)
    driver.close()
    
    # getting just the assignment; not calendar events
    assignments = []
    for i in text:
        if "due" in i and "Calendar" not in i: 
            assignments.append(i)

    # getting the due dates
    time_data = []
    for i in assignments:
        time_data.append(i.split("day, ")[-1])
    
    # getting the assignment names
    asgn_name = []
    for i in assignments:
        temp = i.split(", due")[0]
        temp = temp.replace('Assignment ', '')
        asgn_name.append(temp)

    return asgn_name, time_data
