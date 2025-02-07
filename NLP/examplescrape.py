from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def initialize_driver():
    try:
        driver = webdriver.Chrome()
        print("✅ Chrome WebDriver initialized successfully")
        return driver
    except Exception as e:
        print(f"❌ Failed to initialize Chrome WebDriver: {str(e)}")
        exit()

def handle_login(driver):
    print("\n🔐 Manual Login Required")
    print("1. Browser window opening...")
    print("2. Complete institutional login")
    print("3. Wait for redirect to Outline after login")
    try:
        driver.get('https://outline.uwaterloo.ca/view/npycyp')
        print("✅ Successfully navigated to the login page")
    except Exception as e:
        print(f"❌ Failed to navigate to the login page: {str(e)}")
        driver.quit()
        exit()

    print("Error 4")
    WebDriverWait(driver, 200).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody tr"))
    )
    print("\n✅ Successfully loaded Outline page")

def extract_and_save_text(driver):
    try:
        content_element = driver.find_element(By.XPATH, "/html/body")
        total_text = content_element.text  # Remove .text from here
        print(f"✅ Successfully extracted {len(total_text)} characters of text")

        with open('example.txt', 'w', encoding='utf-8') as file:
            file.write(total_text)
        print("✅ Text extracted and written to example.txt")
    except Exception as e:
        print(f"❌ Failed to extract or write text: {str(e)}")


def main():
    driver = initialize_driver()
    handle_login(driver)
    extract_and_save_text(driver)
    print(f"Final URL: {driver.current_url}")
    driver.quit()
    print("✅ WebDriver closed")

main()
