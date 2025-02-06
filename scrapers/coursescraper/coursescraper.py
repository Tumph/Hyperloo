from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json
import re

def scrape_courses():
    with open('../majorscraper/majors.json', 'r') as file:
        majors = json.load(file)
    
    driver = webdriver.Chrome()
    courses = []
    course_id = 1
    
    for idx, major in enumerate(majors):
        print(f"\nProcessing major {idx+1}/{len(majors)}: {major['major_name']}")
        try:
            driver.get(major['link'])
            
            # Wait for main container
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, "__KUALI_TLP"))
            )
            
            # Get fresh page source
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            
            # Find all course requirement sections
            sections = soup.find_all('div', class_='noBreak')
            
            for section in sections:
                h3 = section.find('h3', class_='program-view__label___3Ui-H')
                if not h3 or h3.get_text(strip=True) not in ['Course Requirements', 'Course Lists']:
                    continue
                
                # Find all term blocks
                term_blocks = section.find_all('div', class_='style__itemHeaderH2___3U8zB')
                
                for term_block in term_blocks:
                    term = term_block.get_text(strip=True)
                    
                    # Find the course list immediately following the term header
                    course_list = term_block.find_next('ul', style=re.compile(r'margin-top:\s*5px'))
                    if not course_list:
                        continue
                    
                    # Extract course items
                    for item in course_list.find_all('li'):
                        course_span = item.find('span')
                        if not course_span:
                            continue
                            
                        # Extract course code and link
                        a_tag = course_span.find('a')
                        if a_tag:
                            course_code = a_tag.get_text(strip=True)
                            course_link = a_tag['href']
                        else:
                            continue  # Skip entries without links
                        
                        # Extract full text and credits
                        full_text = course_span.get_text(strip=False)
                        credit_match = re.search(r'\((\d\.\d{2})\)', full_text)
                        credits = credit_match.group(1) if credit_match else "0.00"
                        
                        # Extract course name
                        name = re.split(r'\(?\d\.\d{2}\)?', full_text.split('-', 1)[-1])[0].strip()
                        
                        courses.append({
                            "course_id": course_id,
                            "course_code": course_code,
                            "course_name": name,
                            "link": course_link,
                            "credits": credits,
                            "term": term,
                            "major_id": major["major_id"],
                            "major_name": major["major_name"],
                            "program_id": major["program_id"],
                            "program_name": major["program_name"]
                        })
                        course_id += 1
                        print(f" ✔ Added course: {course_code} - {name}")
                        
        except Exception as e:
            print(f" !! Error processing major: {str(e)[:80]}")
            continue
    
    with open('courses.json2', 'w') as file:
        json.dump(courses, file, indent=4)
    
    print(f"\nScraping complete. Found {len(courses)} courses.")
    driver.quit()

if __name__ == "__main__":
    scrape_courses()