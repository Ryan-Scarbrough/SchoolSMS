# Author: Ryan Scarbrough
# LE: 1/26/22
# THIS FILE GETS THE CHAPEL DATA FROM COVENANT'S WEBSITE AND RETURNS THE DATA IN A LIST OF STRINGS

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import login # login info
import os # for windows driver

def getData():
    # LINUX CHROMIUM DRIVER
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(executable_path=r'/usr/bin/chromedriver', chrome_options=options)
    # WINDOWS FIREFOX DRIVER
    # os.environ['MOZ_HEADLESS'] = '1'
    # driver = webdriver.Firefox(executable_path=r'C:\Programming\geckodriver.exe')

    driver.get(login.cov_url)

    usernameElement = driver.find_element_by_id("username")
    usernameElement.send_keys(login.cov_username) 
    passwordElement = driver.find_element_by_id("password")
    passwordElement.send_keys(login.cov_password)

    driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[1]/div/div[1]/form/button").click() # clicking login button

    chapelAttend = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[2]/div[1]/div[1]/div[4]/div[2]').text
    chapelLeft = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[2]/div[1]/div[1]/div[5]/div[2]').text
    driver.close()
    return chapelAttend, chapelLeft



























# payload = {
#     'username' : "ryan.scarbrough",
#     'password' : "maR!o2002"
# }

# r = requests.get('https://portal.covenant.edu/')
# cookie = r.cookies['PHPSESSID']
# print(cookie)

# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0',
#     'Origin': 'https://portal.covenant.edu',
#     'Referer': 'https://portal.covenant.edu/',
#     'Cookie': 'PHPSESSID=' + f'{cookie}', #evtc582cmmnn828v3ie07e96op
# }

# # Use 'with' to ensure the session context is closed after use.
# with requests.Session() as s:
#     p = s.post('https://portal.covenant.edu/', data=payload, headers=headers)
#     # print the html returned or something more intelligent to see if it's a successful login page.
#     print(p.text)

#     # An authorised request.
#     r = s.get('https://portal.covenant.edu/chapel/checker')
#     print(r.text)
#     print(r.status_code)


# with open('pagedata.txt', 'w', encoding='utf-8') as f:
#     f.write(r.text)
