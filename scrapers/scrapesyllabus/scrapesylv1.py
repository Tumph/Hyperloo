from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup
import json
import re
import time

def handle_login(driver):
    print("\n🔐 Manual Login Required")
    print("1. Browser window opening...")
    print("2. Complete institutional login")
    print("3. Wait for redirect to Outline after login")
    driver.get('https://outline.uwaterloo.ca/browse/')
    
    try:
        #Waits until Course search element is open to start the script
        WebDriverWait(driver, 120).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder*='Course Search']"))
        )
        print("\n✅ Login validated!")
        time.sleep(2)
    except Exception as e:
        print(f"\n❌ Login failed: {str(e)}")
        driver.quit()
        exit()


def extract_syllabus_data(soup):
    """Enhanced extraction with multiple fallback strategies"""
    print("🔍 Beginning syllabus extraction...")
    topics = []
    times = []
    
    # Strategy 1: Find schedule section using flexible header detection
    schedule_header = soup.find(['h2', 'h3', 'h4'], 
        string=re.compile(r'schedule|week|content week|tentative', re.IGNORECASE))
    
    if schedule_header:
        print(f"📑 Found schedule header: {schedule_header.get_text(strip=True)}")
        table = schedule_header.find_next('table')
        
        if table:
            print("📊 Processing schedule table")
            time_col, topic_col = get_column_indices(table)
            print(f"🔧 Detected columns - Time: {time_col+1}, Topics: {topic_col+1}")
            
            rows = table.find_all('tr')[1:]  # Skip header row
            for row in rows:
                cells = row.find_all(['td', 'th'])
                if len(cells) > max(time_col, topic_col):
                    time_text = cells[time_col].get_text(strip=True)
                    topic_text = cells[topic_col].get_text(strip=True)
                    
                    if time_text and topic_text:
                        times.append(time_text)
                        topics.append(topic_text)
            print(f"✅ Table extraction: {len(topics)} items found")
    
    # Strategy 2: Fallback to list items if table parse fails
    if not topics:
        print("⚠️ Table parse failed, trying list items...")
        list_items = soup.select('ul li, ol li')
        for item in list_items:
            if re.match(r'(week|session)\s+\d+', item.text, re.IGNORECASE):
                parts = re.split(r':\s*', item.text, 1)
                if len(parts) == 2:
                    times.append(parts[0])
                    topics.append(parts[1])
        print(f"📝 List extraction: {len(topics)} items found")
    
    # Remove duplicates while preserving order
    seen = set()
    topics = [x for x in topics if not (x in seen or seen.add(x))]
    seen = set()
    times = [x for x in times if not (x in seen or seen.add(x))]
    
    return topics, times

def scrape_syllabi():
    print("🚀 Starting syllabus scraping process")
    with open('../coursescraper/courses.json', 'r') as f:
        courses = json.load(f)
    
    driver = webdriver.Chrome()
    #Wait for login to execute scraping
    handle_login(driver)
    syllabus_data = []

    for idx, course in enumerate(courses):
        print(f"\n📚 Processing {idx+1}/{len(courses)}: {course['course_code']}")
        formatted_code = re.sub(r'(\D)(\d)', r'\1 \2', course['course_code'])
        
        try:
            # Navigate and search
            print("🌐 Navigating to search page...")
            driver.get('https://outline.uwaterloo.ca/browse/')
            
            print(f"🔎 Searching for {formatted_code}...")
            search_box = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder*='Course Search']"))
            )
            search_box.clear()
            search_box.send_keys(formatted_code)
            
            search_button = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button#button-addon2"))
            )
            search_button.click()

        except Exception as e:
            print(f"🔥 Error occured with course search: {str(e)}")
            print(f"🌍 Current Error URL: {driver.current_url}")
            continue

        # See if there are results or not
        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody tr"))
            )
        except TimeoutException:
            print("❌ No results found, skipping...")
            continue

        # Click view button to go to syllabus
        print("🔗 Accessing syllabus...")
        try:
            view_button = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'btn-outline-primary') and contains(@title, 'View Online')]"))
            )
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", view_button)
            time.sleep(0.5)
            view_button.click()
        except (TimeoutException, NoSuchElementException):
            print("❌ View button not found, skipping...")
            continue


        # Switch tabs and extract
        print("🔄 Switching to new tab...")
        
        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody tr"))
            )

            print("🖨️ Parsing...")
            
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(1)
            
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            topics, times = extract_syllabus_data(soup.get_text())
            
            # Validation check
            if len(topics) == 0:
                print("⚠️ Warning: No topics extracted")
            else:
                print(f"✔️ Success: Collected {len(topics)} topics")
            
            syllabus_data.append({
                "course_id": course["course_id"],
                "course_code": course["course_code"],
                "course_name": course["course_name"],
                "topics": topics,
                "time": times
            })

        except TimeoutException:
            print("❌ Syllabus content not found")
        finally:
            print("📂 Closing tab...")
            driver.close()



    # Save results
    with open('syllabi.json', 'w') as f:
        json.dump(syllabus_data, f, indent=4)
    
    driver.quit()
    print(f"\n🎉 Completed: {len(syllabus_data)} syllabi processed")
    print("💾 Output saved to syllabi.json")

if __name__ == "__main__":
    scrape_syllabi()
