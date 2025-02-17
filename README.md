# Hyperloo

This repository is a knowledge graph of all UWaterloo programs, majors, courses, and topics. Similar to [Hyperphysics](http://hyperphysics.phy-astr.gsu.edu/hbase/index.html), except algorithmically generated for any and all topics instead of just physics.


## I: Scraping the Data

This repository contains three Python scripts to scrape academic program, major data, and courses from the University of Waterloo's academic calendar website.

### Features
- `programscrape.py`: Scrapes all undergraduate programs and their links into `programs.json`.
- `majorscrape.py`: Scrapes majors under each program from `programs.json` and saves them into `majors.json`.
- `coursescraper.py`: Scrapes courses under each major from `majors.json` and saves them into `courses.json`.
- `syllabuscraper.py`: Scrapes syllabi under each course from `courses.json` and saves them into `syllabi.json`.

### Prerequisites
1. **Python 3.9+**: [Download Python](https://www.python.org/downloads/)
2. **Chrome WebDriver**: Required for Selenium automation.
   - Download from [ChromeDriver](https://sites.google.com/chromium.org/driver/)
   - Ensure it is added to your system `PATH` or place it in the project directory.
3. **Git** (Optional): For cloning the repository.
4. ```pip install selenium```
5. ```pip install beautifulsoup4```
6. ```pip install spacy```

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
pip install spacy
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


Obviously, if you have a mac you need to configure your venv in order to run the python scripts and pip.

Step 3b: Stem Major Scrape

You need to run
```bash
python STEMfilter.py
```
in order to generate the stem_majors.json file. This file is used to filter out the majors that are not relevant to the topic of interest.

Step 4: Scrape Syllabi
Then, you need to run scrape syllabus. After courses.json is generated, run the fourth script to scrape syllabi:

Hyperloo/scrapers/syllabuscraper/syllabuscraper.py
```bash
python syllabuscraper.py
```
This creates the syllabi.json file.

---

## II: NLP and Processing
Generating the NLP model is the most time consuming part of the process. It takes a few hours to train, so we made a chunker that splits up the syllabi text into 60 chunks that all get processed parallelly. The chunker is located in the NLP folder.

The chunker is a python script that takes syllabi.json as input and outputs a new folder called `chunks` that contains the chunked syllabi.json files.

Run
```bash
python NLPtrainer.py
```
in order to train the NLP model. This will create a new folder called `syllabus_classifierv4` that contains the trained model.

Then, go into NLP/Processing and run these commands as in commands.txt

# Split into chunks
```bash
python split_syllabi.py
```

# Process in parallel (use nohup for long-running)
```bash
chmod +x run_parallel.sh
./run_parallel.sh
```

# Combine results
```bash
cat trees/trees_*.jsonl > final_trees.jsonl
```

#combine error jsnols as well
```bash
cat missedtrees/trees_*.jsonl > final_missed_trees.jsonl
```

## III: Generating Knowledge Graph

Taking the final trees.jsonl file, we can generate the knowledge graph. The knowledge graph is a JSON file that contains all the information about the topics, majors, and courses. It is located in the `UI` folder.

Convert the trees.jsonl file into a JSON file, and then run the Graph.js file on it.

You are done!
