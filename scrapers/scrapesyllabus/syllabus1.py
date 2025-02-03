from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup
import spacy
import json
import re
import time
from collections import defaultdict

def load_nlp_model():
    """Load and configure spaCy model"""
    print("🔧 Loading spaCy model...")
    nlp = spacy.load("en_core_web_lg")
    
    # Add custom patterns for academic terms
    ruler = nlp.get_pipe("attribute_ruler")
    patterns = [
        {"label": "TOPIC", "pattern": [{"LOWER": {"IN": ["week", "lecture", "module", "unit", "topic", "session"]}}]},
        {"label": "ACADEMIC", "pattern": [{"POS": "NOUN"}, {"LOWER": "theory"}]},
        {"label": "ACADEMIC", "pattern": [{"POS": "NOUN"}, {"LOWER": "analysis"}]},
        {"label": "ACADEMIC", "pattern": [{"POS": "NOUN"}, {"LOWER": "methods"}]}
    ]
    for pattern in patterns:
        ruler.add(pattern)
    return nlp

def get_column_indices(table):
    """Determine the indices of time and topic columns in a table."""
    headers = table.find('tr').find_all(['th', 'td'])
    time_col = None
    topic_col = None
    
    for idx, header in enumerate(headers):
        text = header.get_text(strip=True).lower()
        if any(word in text for word in ['week', 'time', 'date', 'schedule']):
            time_col = idx
        if any(word in text for word in ['topic', 'content', 'subject', 'title']):
            topic_col = idx
    
    # Default to first two columns if headers not found
    if time_col is None:
        time_col = 0
    if topic_col is None:
        topic_col = 1
    
    return time_col, topic_col

def handle_login(driver):
    print("\n🔐 Manual Login Required")
    print("1. Browser window opening...")
    print("2. Complete institutional login")
    print("3. Wait for redirect to Outline after login")
    driver.get('https://outline.uwaterloo.ca/browse/')
    
    try:
        WebDriverWait(driver, 120).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder*='Course Search']"))
        )
        print("\n✅ Login validated!")
        time.sleep(2)
    except Exception as e:
        print(f"\n❌ Login failed: {str(e)}")
        driver.quit()
        exit()

def extract_syllabus_data(soup, nlp):
    """Enhanced extraction with NLP filtering"""
    print("🔍 Beginning syllabus extraction...")
    topics = []
    times = []
    
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
                        doc = nlp(topic_text)
                        if doc.cats["SYLLABUS"] > 0.5:
                            times.append(time_text)
                            topics.append(topic_text)
            print(f"✅ Table extraction: {len(topics)} items found (NLP filtered)")
    
    if not topics:
        print("⚠️ Table parse failed, trying list items...")
        list_items = soup.select('ul li, ol li')
        for item in list_items:
            item_text = item.get_text(strip=True)
            if re.match(r'(week|session)\s+\d+', item_text, re.IGNORECASE):
                parts = re.split(r':\s*', item_text, 1)
                if len(parts) == 2:
                    time_part, topic_part = parts[0], parts[1]
                    doc = nlp(topic_part)
                    if doc.cats["SYLLABUS"] > 0.5:
                        times.append(time_part)
                        topics.append(topic_part)
        print(f"📝 List extraction: {len(topics)} items found (NLP filtered)")
    
    seen = set()
    topics = [x for x in topics if not (x in seen or seen.add(x))]
    seen = set()
    times = [x for x in times if not (x in seen or seen.add(x))]
    
    return topics, times

def scrape_syllabi():
    print("🚀 Starting syllabus scraping process")
    with open('../coursescraper/courses.json', 'r') as f:
        courses = json.load(f)
    
    try:
        nlp = spacy.load("../../syllabus_classifier2")
    except Exception as e:
        print(f"❌ Failed to load NLP model: {e}")
        exit()
    
    driver = webdriver.Chrome()
    handle_login(driver)
    syllabus_data = []

    for idx, course in enumerate(courses):
        print(f"\n📚 Processing {idx+1}/{len(courses)}: {course['course_code']}")
        formatted_code = re.sub(r'(\D)(\d)', r'\1 \2', course['course_code'])
        
        try:
            driver.get('https://outline.uwaterloo.ca/browse/')
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
            print(f"🔥 Error occurred with course search: {str(e)}")
            print(f"🌍 Current Error URL: {driver.current_url}")
            continue

        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody tr"))
            )
        except TimeoutException:
            print("❌ No results found, skipping...")
            continue

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

        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody tr"))
            )

            print("🖨️ Parsing...")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(1)
            
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            topics, times = extract_syllabus_data(soup, nlp)
            
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

    with open('syllabi.json', 'w') as f:
        json.dump(syllabus_data, f, indent=4)
    
    driver.quit()
    print(f"\n🎉 Completed: {len(syllabus_data)} syllabi processed")
    print("💾 Output saved to syllabi.json")

if __name__ == "__main__":
    scrape_syllabi()