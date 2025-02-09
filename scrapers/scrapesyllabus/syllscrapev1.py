from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import re
import time
import spacy
from tqdm import tqdm


currentmodel = "../../NLP/syllabus_classifierv4"

def classify(text):
    nlp_classifier = spacy.load(f'{currentmodel}')
    nlp = spacy.load("en_core_web_lg")

    nlp.disable_pipes(["ner", "tagger", "parser", "attribute_ruler", "lemmatizer"])
    nlp.enable_pipe("senter")

    max_length = nlp.max_length
    texts = [text[i:i+max_length] for i in range(0, len(text), max_length)]

    sentences = []

    truesyllabus = []

    for doc in tqdm(nlp.pipe(texts), desc="Processing Text"):
        sentences.extend([sent.text.strip() for sent in doc.sents if sent.text.strip()])

    final_sentences = []
    for sentence in sentences:
        sub_sentences = sentence.split('\n')
        final_sentences.extend([s.strip() for s in sub_sentences if s.strip()])

    for sentence in tqdm(final_sentences, desc="Classifying Sentences"):
        sentence_doc = nlp_classifier(sentence)

    for sentence in final_sentences:
        sentence_doc = nlp_classifier(sentence)
        if sentence_doc.cats.get('SYLLABUS', 0) > 0.9:
            truesyllabus.append(sentence)

    return truesyllabus


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

def extract_syllabus(driver):
    try:
        content_element = driver.find_element(By.XPATH, "/html/body")
        total_text = content_element.text
        print(f"✅ Successfully extracted {len(total_text)} characters of text")

        # Extract text output
        return total_text
    except Exception as e:
        print(f"❌ Failed to extract or write text: {str(e)}")



def scrape_syllabi():
    print("🚀 Starting syllabus scraping process")
    with open('../coursescraper/courses.json', 'r') as f:
        courses = json.load(f)

    driver = webdriver.Chrome()
    handle_login(driver)
    syllabus_data = []

    for idx, course in enumerate(courses):
        print(f"\n📚 Processing {idx+1}/{len(courses)}: {course['course_code']}")
        formatted_code = re.sub(r'(\D)(\d)', r'\1 \2', course['course_code'])

        try:
            # Debug current window state
            print(f"🪟 Current windows: {driver.window_handles}")
            print(f"📍 Current URL: {driver.current_url}")

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

            # Wait for search results to load
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody tr"))
            )
            results = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
            print(f"🔍 Found {len(results)} search results")

            # Click view button
            print("🔗 Accessing syllabus...")
            view_button = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'btn-outline-primary') and contains(@title, 'View Online')]"))
            )
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", view_button)

            view_button.click()


            # Wait for syllabus page to load
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody tr"))
            )


            print("🖨️ Extracting syllabus content...")
            topics = classify(extract_syllabus(driver))

            print("Adding to Json...")

            if len(topics) == 0:
                print("⚠️ Warning: No topics extracted")
            else:
                print(f"✔️ Success: Collected {len(topics)} topics")
                syllabus_data.append({
                    "course_id": course["course_id"],
                    "course_code": course["course_code"],
                    "course_name": course["course_name"],
                    "topics": topics
                })


        except Exception as e:
            print(f"❌ Error processing {course['course_code']}: {str(e)}")
            print(f"🌍 Current URL: {driver.current_url}")
            print(f"🪟 Window handles: {driver.window_handles}")
            continue

    with open('syllabi.json', 'w') as f:
        json.dump(syllabus_data, f, indent=4)

    driver.quit()
    print(f"\n🎉 Completed: {len(syllabus_data)} syllabi processed")
    print("💾 Output saved to syllabi.json")

if __name__ == "__main__":
    scrape_syllabi()
