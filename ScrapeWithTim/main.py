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
bet_amount_xpath = "//div[@class='game-container']//div[@class='game-controls']//div[@class='game-info']//span[@class='ng-star-inserted']"
multiplier_css_selector = "div.payouts-block app-bubble-multiplier div[appcoloredmultiplier].bubble-multiplier"
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
    # window_after = driver.window_handles[1]  # Switch to the new window
    # driver.switch_to.window(window_after)

    # incase one of the line of code throws an error, the except part of the code is executed, prints("locator not found") and finally quits the driver.
except:
    print("Locator not found")
    driver.quit()
wait = WebDriverWait(driver, 5)
print("Everything is okay up to here!")

# Now up to this point, we should be logged in  to our target website where we should be able to collect the data
# print("We now getting started. Wait for 15 seconds")
while True:
    try:
        wait = WebDriverWait(driver, 5)
        parent_div = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.payouts-block"))) # Find the parent div element
        print("The 'payouts-block' div element was found on the page!")
        
        # wait = WebDriverWait(driver, 3)
        # # Find all child elements with the same identifier (app-bubble-multiplier)
        # child_elements = wait.until(lambda d: parent_div.find_elements(By.TAG_NAME, "app-bubble-multiplier"))

        # # Create an empty list to store the values
        # values = []

        # # Loop through each child element and extract its text content
        # for child in child_elements:
        #     value_div = child.find_element(By.CSS_SELECTOR, "div[appcoloredmultiplier].bubble-multiplier")
        #     value = value_div.text
        #     values.append(value)

        # print(values)  # Output: ['10.29x', '4.03x', '1.38x', '2.09x']
    except TimeoutException:
        print("Timeout occurred while waiting for elements to load.")
    except Exception as e:
        print(f"An error occurred: {e}")

