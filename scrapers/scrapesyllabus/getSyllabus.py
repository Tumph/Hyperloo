from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up Chrome options to connect to the debugging port
chrome_options = Options()
chrome_options.debugger_address = "127.0.0.1:9222"  # Debugging port

# Specify the path to chromedriver.exe using Service
service = Service("Hyperloo/chromedriver.exe")  # Replace with your actual path

# Connect to the existing browser session
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get("https://outline.uwaterloo.ca/browse/")  # Open a new page in the same session

# Step 1: Locate the text box and input search text
search_box = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'input[aria-label="Course Outline Search"]'))
)
search_box.clear()  # Clear any existing text
search_box.send_keys("MTE 119")  # Replace with the text you want to input
search_box.submit()  # Submit the search

# Step 2: Wait for the table and locate the first "View Online" button
view_online_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[title="View Online"]'))
)

# Click the first "View Online" button
view_online_button.click()

tentative_schedule_h2 = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "tentative-course-schedule"))
)

# Find all <p> elements that are directly under <h2> with id="tentative-course-schedule"
# but are not under any other <h2> tags that are descendants of it.
p_elements = driver.find_elements(By.XPATH, "//h2[@id='tentative-course-schedule']/following-sibling::p")

# Extract and print the text from each <p> element
p_texts = [p.text for p in p_elements]
print("Paragraphs under <h2> with id='tentative-course-schedule':")
print("\n".join(p_texts))



#"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:/ChromeDebug"
