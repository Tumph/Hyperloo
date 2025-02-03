from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json


def scrape():
    driver = setup()
    driver.implicitly_wait(5)
    print("Scraping UWaterloo Programs...")

    # Initialize a list to store program data
    programs = []

    # Find the list container
    list = driver.find_element(By.ID, "__KUALI_TLP")
    items = list.find_elements(By.CLASS_NAME, "style__collapsibleBox___15waq")
    idcount = 0

    for item in items:
        idcount += 1
        # Get the program name
        name = item.get_attribute("name")

        try:
            # Click the item to expand it
            driver.execute_script("arguments[0].click();", item)
            link_elements = item.find_elements(By.TAG_NAME, "a")

            # Collect all links for the program
            links = [link.get_attribute("href") for link in link_elements]

            # Add the program data to the list
            programs.append({
                "name": name,
                "links": links,
                "id": idcount
            })

        except Exception as e:
            print(f"Error clicking element: {e}")

    # Convert the list of programs to JSON
    with open("programs1.json", "w") as file:
        json.dump(programs, file, indent=4)

    teardown(driver)

def setup():
    driver = webdriver.Chrome()
    driver.get("https://uwaterloo.ca/academic-calendar/undergraduate-studies/catalog#/programs")
    return driver

def teardown(driver):
    driver.quit()

if __name__ == "__main__":
    scrape()