
# SkillGap AI 🎯
### AI-Based Resume and Job Description Skill Gap Analyzer

SkillGap AI is a Python-based application that compares a candidate's resume with a job description to identify matching skills, missing skills, and areas for improvement.

The application uses Natural Language Processing (NLP) techniques and text similarity analysis to help job seekers understand how their resumes align with job requirements.

## Features

- **Resume Upload:** Upload a resume in PDF format.
- **Skill Extraction:** Identify recognized technical and professional skills.
- **Skill Gap Analysis:** Compare resume skills with job requirements.
- **Skill Coverage:** Calculate the percentage of recognized job skills found in the resume.
- **Text Similarity:** Use TF-IDF and cosine similarity to measure textual similarity.
- **Learning Checklist:** Display missing skills as a checklist.
- **CSV Report:** Download the skill gap analysis report.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Interactive web application |
| pandas | Data processing and report generation |
| scikit-learn | TF-IDF and cosine similarity |
| pypdf | Extract text from PDF resumes |
| Git and GitHub | Version control and project hosting |

## Project Structure

```text
SkillGap-AI/
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/AkshataHangari003/SkillGap-AI.git
cd SkillGap-AI
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
streamlit run app.py
```

The application will normally open at:

http://localhost:8501

## How to Use

1. Upload a text-based PDF resume.
2. Paste the target job description.
3. Click **Analyze Skill Gap**.
4. Review matched skills, missing skills, and skill coverage.
5. Download the results as a CSV file.

## Current Limitations

- Skill extraction uses a predefined dictionary and may miss unlisted skills or synonyms.
- Scanned PDFs without selectable text are not supported in the current version.
- TF-IDF similarity measures textual similarity, not actual candidate competence.
- Skill coverage is not an official ATS score or a prediction of hiring success.
- Learning recommendations are currently a basic checklist rather than an intelligent recommendation model.

## Future Enhancements

- Expand the skill dictionary and synonym detection.
- Evaluate skill extraction using a labeled dataset.
- Add priority-based skill gap recommendations.
- Generate personalized learning roadmaps.
- Compare one resume against multiple job descriptions.
- Improve the user interface and deploy a live demo.

## Learning Outcomes

This project demonstrates practical experience with Python, text preprocessing, NLP fundamentals, TF-IDF vectorization, cosine similarity, PDF text extraction, data processing, and Streamlit application development.

## Author

**Akshata Hangari**

GitHub: [AkshataHangari003](https://github.com/AkshataHangari003)

---

*SkillGap AI is an educational portfolio project. Its results should be treated as guidance, not as a definitive assessment of employability.*
