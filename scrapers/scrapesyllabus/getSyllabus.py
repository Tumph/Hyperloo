from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import spacy
from spacy.training.example import Example
bad = ["chapter","week","jan","feb","%", "mar","apr","may","jun","jul","aug","sept","oct","nov","dec","quiz","exam","tutorial","assignment","january","february","march","april","june","july","august","september","october","november","december"]
# Set up Chrome options to connect to the debugging port
chrome_options = Options()
chrome_options.debugger_address = "127.0.0.1:9222"  # Debugging port

# Specify the path to chromedriver.exe using Service
service = Service("scrapers/scrapesyllabus/chromedriver.exe")  # Replace with your actual path

# Connect to the existing browser session
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get("https://outline.uwaterloo.ca/browse/")  # Open a new page in the same session

# Step 1: Locate the text box and input search text
search_box = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'input[aria-label="Course Outline Search"]'))
)
search_box.clear()  # Clear any existing text
search_box.send_keys("ECE 109")  # Replace with the text you want to input
search_box.submit()  # Submit the search

# Step 2: Wait for the table and locate the first "View Online" button
view_online_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[title="View Online"]'))
)

# Click the first "View Online" button
view_online_button.click()

# Wait for the h2 element with id "tentative-course-schedule"
# Wait for the h2 element with id "tentative-course-schedule"
h2_element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "tentative-course-schedule"))
)

# Find all tables inside the same section/container as the h2 element
tables = h2_element.find_elements(By.XPATH, ".//following::*[self::table]")
nlp = spacy.load("syllabus_classifier2")

# Loop through each table and extract text
for idx, table in enumerate(tables, start=1):
    rows = table.find_elements(By.TAG_NAME, "tr")  # Find all rows
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")  # Find all cells
        row_text = [cell.text.strip() for cell in cells]  # Extract text
        for a in row_text:
            flag = False
            for b in bad:
                if b in a.lower():
                    flag = True
                    break
            if(not flag and a!="" and len(a)>3):
                doc = nlp(a)
                if doc.cats["SYLLABUS"]>0.4:
                    print(a)

# "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:/ChromeDebug"