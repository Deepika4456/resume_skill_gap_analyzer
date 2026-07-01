# Resume Skill Gap Analyzer

A Streamlit web app that analyzes a resume PDF against a pasted job description, extracts skills from both using regex-based matching against a reference skill list, and reports a match score along with matched, missing, and bonus skills — helping candidates quickly identify gaps to close before applying.

🔗 **Live demo:** 

## Problem

Manually comparing a resume against a job description to spot missing skills is slow and easy to get wrong. This tool automates that comparison so a candidate can instantly see where they stand — and export a report to act on.

## Features
- Upload a resume as a **PDF** and paste a job description
- Extracts skills from both using whole-word regex matching against a reference skill list (longest-skill-first, so multi-word skills like "machine learning" aren't broken up by shorter matches)
- Calculates a **match score** and categorizes it (🟢 Strong / 🟡 Moderate / 🟠 Fair / 🔴 Weak)
- Tabbed results view: ✅ Matched skills, ❌ Missing skills, ➕ Extra (bonus) skills, plus full skill lists for both JD and resume
- Built-in **debug panel** — inspect extracted text length, skill counts, and manually test whether a specific skill is detected
- **Export results** as a downloadable `.txt` report with timestamp

## Tech Stack
- **Python**
- **Streamlit** — web app UI
- **PyPDF2** — PDF text extraction
- **re** (regex) — whole-word skill matching
- `skills.txt` — reference list of skills used for extraction

## Project Structure
```
resume_skill_gap_analyzer/
├── app.py            # Streamlit UI, scoring, tabs, export
├── utils.py           # PDF extraction, skill matching, score categorization
├── skills.txt          # Reference list of skills used for extraction
└── requirements.txt      # Python dependencies
```

## How It Works
1. User uploads a resume PDF and pastes a job description into the text area
2. `extract_text_from_pdf()` pulls text from every page of the PDF using PyPDF2
3. `match_skills()` checks the reference skill list against both texts using word-boundary regex, sorting skills longest-first so phrases match before their substrings do
4. The app computes matched, missing, and extra skills as set operations, then a match % = matched / JD-required skills
5. `categorize_score()` labels the result (Strong/Moderate/Fair/Weak Match)
6. Results render in tabs, and the full report can be downloaded as text

## Run Locally
```bash
git clone https://github.com/Deepika4456/resume_skill_gap_analyzer.git
cd resume_skill_gap_analyzer
pip install -r requirements.txt
streamlit run app.py
```

## Future Improvements
- [ ] Support DOCX resume upload (currently PDF only)
- [ ] Use NLP (spaCy) for more flexible skill matching beyond exact keywords
- [ ] Suggest learning resources for missing skills
- [ ] Hide/remove the debug panel for the public demo — great for development, but looks unfinished in front of a recruiter

## Author
**Deepika** — Data Analyst | Data Engineering enthusiast
[LinkedIn] · [GitHub](https://github.com/Deepika4456)
