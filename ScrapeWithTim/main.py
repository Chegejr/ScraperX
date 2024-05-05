from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
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
previous_value = None
data_list = [] # Create an empty list to store the data
def parse_dynamic_content(driver):
    data = []
    bet_items = driver.find_elements(By.CSS_SELECTOR, "app-bet-item")
    for bet_item in bet_items:
        usernamem = bet_item.find_element(By.CSS_SELECTOR, "div.username").text
        bet_amount = bet_item.find_element(By.CSS_SELECTOR, "app-bet-amount > div").text
        if bet_amount.isdigit():
            data.append({
                "username": usernamem,
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
    wait = WebDriverWait(driver, 5)

     # Handle the pop-up
    try:
        popup_cancel_button = wait.until(EC.presence_of_element_located((By.ID, "onesignal-slidedown-cancel-button")))
        popup_cancel_button.click()
    except:
        print("No pop-up found. ")
    print("Everything is okay up to here!")
    print(driver.page_source)

    while True:
        wait = WebDriverWait(driver, 6)
        try:
            payouts_block = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.payouts-block")))

            # Find all "app-bubble-multiplier" elements within the "payouts-block" div
            multiplier_elements = payouts_block.find_elements(By.CSS_SELECTOR, "app-bubble-multiplier")

            # Extract the multiplier values from each "app-bubble-multiplier" element
            multiplier_values = []
            for multiplier_element in multiplier_elements:
                value_div = multiplier_element.find_element(By.CSS_SELECTOR, "div[appcoloredmultiplier].bubble-multiplier")
                multiplier_value = value_div.text
                multiplier_values.append(multiplier_value)

            # Print the extracted multiplier values
            print("Multiplier Values:")
            for value in multiplier_values:
                print(value)
        except TimeoutException:
            print("Timeout occurred while waiting for elements to load.")
        except Exception as e:
            print(f"An error occurred: {e}")
    # window_after = driver.window_handles[1]  # Switch to the new window
    # driver.switch_to.window(window_after)

    # incase one of the line of code throws an error, the except part of the code is executed, prints("locator not found") and finally quits the driver.
except:
    print("Locator not found")
    driver.quit()



