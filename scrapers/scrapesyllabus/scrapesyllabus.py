import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup



# Set up the Selenium WebDriver (ensure the path to chromedriver is correct)
service = Service('Hyperloo/chromedriver.exe')  # Update this path
options = webdriver.ChromeOptions()
# options.add_argument('--headless')  # Run in headless mode if needed

def courses(url):
    driver = webdriver.Chrome(service=service, options=options)
    temp = []
    try:
        driver.get(url)

        # Wait for 3 seconds to ensure content is loaded
        time.sleep(1)

        # Extract page content
        page_content = driver.page_source

        # Parse with BeautifulSoup
        soup = BeautifulSoup(page_content, 'html.parser')

        # Find all <span> elements (adjust to the exact tags you need)
        items = soup.find_all('span')

        # Initialize an empty list to store courses with additional info
        courses = []

        for i, span in enumerate(items, start=1):
            # Find the link inside the <span> tag
            link_tag = span.find('a')
            if link_tag and 'href' in link_tag.attrs:
                link = link_tag['href']  # Extract the href attribute

                # Find the previous div with class 'style__itemHeaderH2___3U8zB' before this span
                previous_div = span.find_previous('div', class_='style__itemHeaderH2___3U8zB')
                previous_text = previous_div.text.strip() if previous_div else 'No previous div found'

                # Append the result (previous text, course text, and link) to the courses list
                courses.append([previous_text, span.text.strip(), link])

        # Filter out courses based on certain conditions and deduplicate
        for course in courses:
            if ("(0.50)" in course[1] or "(0.25)" in course[1]) and len(course[1]) != 6:
                for existing_course in temp:
                    if course[1] in existing_course[1]:
                        temp.pop(temp.index(existing_course))
                temp.append(course)

        # Print the results

    finally:
        driver.quit()
        return temp


url='https://uwaterloo.ca/academic-calendar/undergraduate-studies/catalog#/programs/H1zle10Cs3?searchTerm=sof&bc=true&bcCurrent=Software%20Engineering%20(Bachelor%20of%20Software%20Engineering%20-%20Honours)&bcItemType=programs'

print(courses(url))
print(courses("https://uwaterloo.ca/academic-calendar/undergraduate-studies/catalog#/programs/H1-0kyACi3?searchTerm=physics&bc=true&bcCurrent=Physics%20(Bachelor%20of%20Science%20-%20Honours)&bcItemType=programs"))
