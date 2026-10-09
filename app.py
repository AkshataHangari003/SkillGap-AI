
import re
from io import BytesIO

import pandas as pd
import streamlit as st
from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# -------------------- Page configuration --------------------

st.set_page_config(
    page_title="SkillGap AI",
    page_icon="🎯",
    layout="wide",
)

st.title("SkillGap AI")
st.subheader("Resume and Job Skill Gap Analyzer")

st.write(
    "Compare your resume with a job description, "
    "identify skill gaps, and plan what to learn next."
)


# -------------------- Skill dictionary --------------------

SKILLS = {
    "Python": ["python"],
    "SQL": ["sql", "structured query language"],
    "Machine Learning": ["machine learning", "ml"],
    "Deep Learning": ["deep learning"],
    "Data Analysis": ["data analysis", "data analytics"],
    "Pandas": ["pandas"],
    "NumPy": ["numpy"],
    "Scikit-learn": ["scikit-learn", "sklearn"],
    "TensorFlow": ["tensorflow"],
    "NLP": ["natural language processing", "nlp"],
    "Power BI": ["power bi"],
    "Tableau": ["tableau"],
    "Excel": ["excel", "microsoft excel"],
    "Statistics": ["statistics", "statistical analysis"],
    "Data Visualization": ["data visualization"],
    "Streamlit": ["streamlit"],
    "Flask": ["flask"],
    "FastAPI": ["fastapi"],
    "Git": ["git", "github"],
    "MySQL": ["mysql"],
    "PostgreSQL": ["postgresql", "postgres"],
    "Java": ["java"],
    "JavaScript": ["javascript"],
    "React": ["react"],
    "Node.js": ["node.js", "node js"],
    "HTML": ["html"],
    "CSS": ["css"],
    "Docker": ["docker"],
    "Cloud Computing": ["cloud computing"],
    "Communication": ["communication skills", "communication"],
    "Problem Solving": ["problem solving", "problem-solving"],
    "Project Management": ["project management"],
}


# -------------------- Text processing --------------------

def normalize_text(text):
    """Normalize text for more reliable matching."""
    text = text.lower()
    text = text.replace("\u2010", "-").replace("\u2011", "-")
    return re.sub(r"\s+", " ", text).strip()


def contains_term(text, term):
    """Match a term without matching it inside unrelated words."""
    pattern = r"(?<!\w)" + re.escape(term.lower()) + r"(?!\w)"
    return re.search(pattern, text) is not None


def extract_skills(text):
    """Return recognized skills found in the supplied text."""
    text = normalize_text(text)
    found = []

    for skill, aliases in SKILLS.items():
        if any(contains_term(text, alias) for alias in aliases):
            found.append(skill)

    return sorted(found)


# -------------------- PDF extraction --------------------

def extract_resume_text(pdf_file):
    """Extract selectable text from a PDF resume."""
    reader = PdfReader(BytesIO(pdf_file.getvalue()))

    if reader.is_encrypted:
        raise ValueError("This PDF is encrypted. Upload an accessible PDF.")

    pages = []

    for page in reader.pages:
        pages.append(page.extract_text() or "")

    text = "\n".join(pages).strip()

    if not text:
        raise ValueError(
            "No selectable text found. This may be a scanned PDF. "
            "Use a text-based PDF for this version."
        )

    return text


# -------------------- Analysis --------------------

def calculate_similarity(resume_text, job_text):
    """Calculate text similarity, not hiring probability."""
    vectorizer = TfidfVectorizer(stop_words="english")

    try:
        vectors = vectorizer.fit_transform(
            [resume_text, job_text]
        )
        score = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
        return round(float(score) * 100, 2)
    except ValueError:
        return 0.0


def analyze_resume(resume_text, job_text):
    resume_skills = set(extract_skills(resume_text))
    job_skills = set(extract_skills(job_text))

    matched = sorted(resume_skills & job_skills)
    missing = sorted(job_skills - resume_skills)
    extra = sorted(resume_skills - job_skills)

    if job_skills:
        skill_coverage = round(
            len(matched) / len(job_skills) * 100, 2
        )
    else:
        skill_coverage = 0.0

    similarity = calculate_similarity(resume_text, job_text)

    return {
        "resume_skills": sorted(resume_skills),
        "job_skills": sorted(job_skills),
        "matched": matched,
        "missing": missing,
        "extra": extra,
        "skill_coverage": skill_coverage,
        "similarity": similarity,
    }


# -------------------- User interface --------------------

st.markdown("### 1. Upload your resume")

uploaded_file = st.file_uploader(
    "Choose your resume PDF",
    type=["pdf"],
)

st.markdown("### 2. Enter the job description")

job_description = st.text_area(
    "Paste the complete job description here",
    height=220,
    placeholder=(
        "Example: We are looking for a Data Analyst "
        "with Python, SQL, Power BI, and data visualization skills."
    ),
)

if st.button("Analyze Skill Gap", type="primary"):
    if uploaded_file is None:
        st.error("Please upload a resume PDF.")
    elif not job_description.strip():
        st.error("Please enter a job description.")
    else:
        try:
            resume_text = extract_resume_text(uploaded_file)
            results = analyze_resume(resume_text, job_description)

            if not results["job_skills"]:
                st.warning(
                    "No recognized skills were found in the job "
                    "description. Try a more detailed description."
                )
            else:
                st.markdown("---")
                st.header("Analysis Report")

                col1, col2, col3 = st.columns(3)

                col1.metric(
                    "Skill Coverage",
                    f'{results["skill_coverage"]:.1f}%'
                )
                col2.metric(
                    "Matched Skills",
                    len(results["matched"])
                )
                col3.metric(
                    "Missing Skills",
                    len(results["missing"])
                )

                st.progress(
                    results["skill_coverage"] / 100
                )

                st.caption(
                    "Skill coverage is the percentage of recognized "
                    "job-description skills also found in the resume. "
                    "It is not an ATS score or hiring probability."
                )

                st.subheader("Matched Skills")

                if results["matched"]:
                    st.write(", ".join(results["matched"]))
                else:
                    st.info("No matching skills were identified.")

                st.subheader("Missing Skills")

                if results["missing"]:
                    st.write(", ".join(results["missing"]))
                    st.write("Suggested learning checklist:")

                    for skill in results["missing"]:
                        st.checkbox(
                            f"Learn and practise {skill}",
                            key=f"learn_{skill}",
                        )
                else:
                    st.success(
                        "All recognized job skills were found "
                        "in the resume."
                    )

                st.subheader("Other Skills in Your Resume")

                if results["extra"]:
                    st.write(", ".join(results["extra"]))
                else:
                    st.write("No additional recognized skills found.")

                st.subheader("Text Similarity")

                st.metric(
                    "TF-IDF Similarity",
                    f'{results["similarity"]:.1f}%'
                )

                st.caption(
                    "This measures textual similarity between the "
                    "resume and job description. A high score does "
                    "not guarantee qualifications or hiring success."
                )

                report = pd.DataFrame({
                    "Skill": results["job_skills"],
                    "Status": [
                        "Matched" if skill in results["matched"]
                        else "Missing"
                        for skill in results["job_skills"]
                    ],
                })

                st.subheader("Download Your Report")

                st.download_button(
                    label="Download skill gap report (CSV)",
                    data=report.to_csv(index=False).encode("utf-8"),
                    file_name="skillgap_report.csv",
                    mime="text/csv",
                )

        except Exception as error:
            st.error(f"Could not analyze the resume: {error}")


st.markdown("---")
st.caption(
    "SkillGap AI | Educational portfolio project | "
    "Results depend on the skills recognized by the dictionary."
)
