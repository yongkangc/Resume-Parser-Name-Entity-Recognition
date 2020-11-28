# Resume Parser with Name Entity Recognition

The Program has 2 Parts.
1. Resume Extractor  
Takes in the resume in pdf or docx/doc form and extracts key information from it.
- Name
- Education
- Skills
- Designation

Name Entity Recognition Model is trained with 200 Datasets.

2. Job Matching With Resume
Match Resume with Job Description and obtain a similarity score

## Setup
```
env/bin/activate
pip install -r requirements.txt
```
## Extracting key information out of resume
```
# Extract Key information out of resume
# replace the resume file in main.py with the desired file path
python -m resume_parser/resume_parser.py
```

## Job Matching with Resume
