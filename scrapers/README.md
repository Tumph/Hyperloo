# UWaterloo Program and Major Scraper

This repository contains two Python scripts to scrape academic program and major data from the University of Waterloo's academic calendar website.

## Features
- `programscrape.py`: Scrapes all undergraduate programs and their links into `programs.json`.
- `majorscrape.py`: Scrapes majors under each program from `programs.json` and saves them into `majors.json`.

## Prerequisites
1. **Python 3.7+**: [Download Python](https://www.python.org/downloads/)
2. **Chrome WebDriver**: Required for Selenium automation.
   - Download from [ChromeDriver](https://sites.google.com/chromium.org/driver/)
   - Ensure it is added to your system `PATH` or place it in the project directory.
3. **Git** (Optional): For cloning the repository.

---

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/hyperloo.git
cd scrapers
```

### 2. Install dependencies
```bash
pip install selenium
```

### 3. Run the scripts

Step 1: Scrape Programs
Run the first script to generate programs.json:

```bash
python programscrape.py
```
Step 2: Scrape Majors
After programs.json is generated, run the second script to scrape majors:

```bash
python majorscrape.py
```