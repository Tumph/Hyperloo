from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

def scrape_majors():
    # Load the existing programs data
    with open('../programscraper/programs.json', 'r') as file:
        programs = json.load(file)
    
    # Setup the WebDriver
    driver = webdriver.Chrome()
    majors = []
    
    for program in programs:
        program_id = program['id']
        program_name = program['name']
        program_link = program['links'][0]  # Assuming each program has one link
        
        # Navigate to the program page
        driver.get(program_link)
        
        try:
            # Wait for the majors container to load
            container = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "style__withDivider___3R1Em"))
            )
            # Find all major elements within the container
            major_elements = container.find_elements(By.CLASS_NAME, "style__columns___1xpfv")
            
            major_id = 1
            for elem in major_elements:
                a_tag = elem.find_element(By.TAG_NAME, 'a')
                major_name = a_tag.text
                major_link = a_tag.get_attribute('href')
                
                majors.append({
                    "major_name": major_name,
                    "link": major_link,
                    "major_id": major_id,
                    "program_id": program_id,
                    "program_name": program_name
                })
                major_id += 1
        except Exception as e:
            print(f"Could not find majors for program '{program_name}': {e}")
            continue
    
    # Save the majors data to a JSON file
    with open('majors.json', 'w') as file:
        json.dump(majors, file, indent=4)
    
    # Close the browser
    driver.quit()

if __name__ == "__main__":
    scrape_majors()