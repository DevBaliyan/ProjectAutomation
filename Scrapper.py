#USE COOKIES FOR SIGNIN
import json

import undetected_chromedriver as uc

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from time import sleep
from QuestionMatcher import find_best_match, find_best_match_opt


options = uc.ChromeOptions()
options.add_argument("--start-maximized")  # Open browser in maximized mode
options.add_argument("--disable-extensions")  # Disable extensions
options.add_argument("--disable-popup-blocking")  # Disable popups
##options.add_argument("--remote-debugging-port=9222")  #Reconnect
##options.add_argument("--user-data-dir=C:/ChromeProfile")

# Reattach to the existing browser
driver = uc.Chrome(options=options)
driver.get("https://finish66-edtech.vercel.app/")


#NAVIGATE TO QUESTION SET





#FETCH DATA
lis_test_name = [i.text for i in driver.find_elements(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div/div[2]/div/div/div[1]/div/div/div[2]/h3')]

lis_ques = [
    [element.text for element in driver.find_elements(By.XPATH, f'/html/body/div[1]/div[2]/div[2]/div/div[2]/div[{i}]/div/div[2]/div')]
    for i in range(2, 593, 2)
]

lis_options = [
    [element.text for element in driver.find_elements(By.XPATH, f'/html/body/div[1]/div[2]/div[2]/div/div[2]/div[{i}]/div/div[2]/div/div[2]/div[2]/div')]                      for i in range(2, 593, 2)
]

lis_ans = [
    [j.text for j in driver.find_elements(
        By.XPATH, f'/html/body/div[1]/div[2]/div[2]/div/div[2]/div[{i}]/div/div[2]//*[contains(@class, "p-3") and contains(@class, "rounded-xl") and contains(@class, "bg-violet-500/10") and contains(@class, "border") and contains(@class, "border-violet-500/30")]'
    )]
    for i in range(2, 593, 2)
]


for i, test_name in enumerate(lis_test_name):
    data[test_name] = {
        "Ques": lis_ques[i],
        "Options": lis_options[i],
        "Ans": lis_ans[i]
    }

    
with open("CogniteL1.json", "w", encoding='utf-8') as json_file:
    json.dump(data, json_file, indent=4)
