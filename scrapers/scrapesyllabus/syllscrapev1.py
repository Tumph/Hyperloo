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

def extract_and_format_course_codes(course_titles):
    pattern = r'([A-Z]+)(\d+)([A-Z]*)'

    matches = re.findall(pattern, course_titles)

    formatted_codes = [f"{match[0]} {match[1]}{match[2]}" for match in matches]
    subject_codes = [match[0] for match in matches]
    catalog_numbers = [f"{match[1]}{match[2]}" for match in matches]

    return formatted_codes[0], subject_codes[0], catalog_numbers[0]


def scrape_syllabi():
    print("🚀 Starting syllabus scraping process")
    with open('../coursescraper/shortcourse2.json', 'r') as f:
        majors = json.load(f)

    driver = webdriver.Chrome()
    handle_login(driver)
    syllabus_data = []

    for idx, major in enumerate(majors):
        for idy, course in enumerate(major['courses']):
            print(f"\n📚 Processing {idx+1}/{len(majors)}: {major['major_name']}")
            print(f"\n📚 Processing {idy+1}/{len(major['courses'])}: {course[1]}")
            course_code, subject_code, catalog_number = extract_and_format_course_codes(course[1])

            try:
                # Debug current window state
                print(f"🪟 Current windows: {driver.window_handles}")
                print(f"📍 Current URL: {driver.current_url}")

                # Navigate and search
                print("🌐 Navigating to search page...")
                driver.get(f'https://outline.uwaterloo.ca/browse/search/?q={subject_code}+{catalog_number}&term=')

                # Wait for search results to load
                # At this point the script should be on the page with the view button
                WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody tr"))
                )
                results = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
                print(f"🔍 Found {len(results)} search results")

                # Click view button
                print("🔗 Accessing syllabus...")
                view_button = WebDriverWait(driver, 2).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'btn-outline-primary') and contains(@title, 'View Online')]"))
                )
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", view_button)

                view_button.click()


                # Wait for syllabus page to load
                WebDriverWait(driver, 5).until(
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
                        "course_id": idy,
                        "course_code": course_code,
                        "course_name": course[1],
                        "term_name": course[0],
                        "program_name": major['program_name'],
                        "program_id": major['program_id'],
                        "major_id": major['major_id'],
                        "major_name": major['major_name'],
                        "topics": topics
                    })


            except Exception as e:
                print(f"❌ Error processing {course_code}: {str(e)}")
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
