# Hyperloo

This repository is a knowledge graph of all UWaterloo programs, majors, courses, and topics. Similar to [Hyperphysics](http://hyperphysics.phy-astr.gsu.edu/hbase/index.html), except algorithmically generated for any and all topics instead of just physics. 


## Act I: Scraping the Data

This repository contains three Python scripts to scrape academic program, major data, and courses from the University of Waterloo's academic calendar website.

### Features
- `programscrape.py`: Scrapes all undergraduate programs and their links into `programs.json`.
- `majorscrape.py`: Scrapes majors under each program from `programs.json` and saves them into `majors.json`.
- `coursescraper.py`: Scrapes courses under each major from `majors.json` and saves them into `courses.json`.

### Prerequisites
1. **Python 3.7+**: [Download Python](https://www.python.org/downloads/)
2. **Chrome WebDriver**: Required for Selenium automation.
   - Download from [ChromeDriver](https://sites.google.com/chromium.org/driver/)
   - Ensure it is added to your system `PATH` or place it in the project directory.
3. **Git** (Optional): For cloning the repository.

---

### Installation

#### 1. Clone the Repository
```bash
git clone https://github.com/tumph/hyperloo.git
cd scrapers
```

#### 2. Install dependencies
```bash
pip install selenium
pip install beautifulsoup4
```

#### 3. Run the scripts

Step 1: Scrape Programs
Run the first script to generate programs.json:

Hyperloo/scrapers/programscraper/programscrape.py
```bash
python programscrape.py
```
Step 2: Scrape Majors
After programs.json is generated, run the second script to scrape majors:

Hyperloo/scrapers/majorscraper/majorscraper.py
```bash
python majorscrape.py
```
Step 3: Scrape Courses
After majors.json is generated, run the third script to scrape courses:

Hyperloo/scrapers/coursescraper/coursescraper.py
```bash
python coursescraper.py
```