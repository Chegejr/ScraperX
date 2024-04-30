from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import pandas as pd
# The link below takes you where to find the chrome driver for your chrome browser, 
# make sure to chose the same version of chrome driver as your chrome browser for seamless use
# https://sites.google.com/chromium.org/driver/

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)
username = 742866249
password = "blackdolphin"
data_list = [] # Create an empty list to store the data

def parse_dynamic_content(driver):
    data = []
    bet_items = driver.find_elements(By.CSS_SELECTOR, "app-bet-item")
    for bet_item in bet_items:
        username = bet_item.find_element(By.CSS_SELECTOR, "div.username").text
        bet_amount = bet_item.find_element(By.CSS_SELECTOR, "app-bet-amount > div").text
        if bet_amount.isdigit():
            data.append({
                "username": username,
                "bet_amount": int(bet_amount)
            })
    return data

driver.get("https://odibets.com/aviator")
wait = WebDriverWait(driver, 10)  # Sets a wait time of 10 seconds for the page to be fully loaded,before executing the try code

try:
    title_div = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "title"))) # wait until the element with class_name "title" is located
    # If the above element is present, now we can proceed to locate the text field that takes in username input and password
    username_field = wait.until(EC.presence_of_element_located((By.ID, "phone")))
    password_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password'][placeholder='• • • • • • • •']")))

    # Now that we have located out text input fields, we pass in our login credentials to initiate an auto login
    username_field.send_keys(username)
    password_field.send_keys(password)

    # The three lines below locates the login button and clicks it 
    login_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button.cta")))
    print("Locator found")
    login_button.click()
    print("Login successful")
    # wait = WebDriverWait(driver, 5)

     # Handle the pop-up
    try:
        popup_cancel_button = wait.until(EC.presence_of_element_located((By.ID, "onesignal-slidedown-cancel-button")))
        popup_cancel_button.click()
    except:
        print("No pop-up found. ")
    # window_after = driver.window_handles[1]  # Switch to the new window
    # driver.switch_to.window(window_after)

    # incase one of the line of code throws an error, the except part of the code is executed, prints("locator not found") and finally quits the driver.
except:
    print("Locator not found")
    driver.quit()
# Now up to this point, we should be logged in  to our target website where we should be able to collect the data
# print("We now getting started. Wait for 15 seconds")

wait = WebDriverWait(driver, 10)
initial_page_source = driver.page_source # Get the initial page source
while True:
    parse_dynamic_content(driver)
    # Create a DataFrame from the collected data
    # df = pd.DataFrame(data_list, columns=['Value'])
    # print(df)


