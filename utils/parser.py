import fitz
import re

# common skills database (expandable)
SKILL_DB = [
    "python", "java", "c++", "machine learning", "ai", "deep learning",
    "nlp", "data science", "docker", "kubernetes",
    "sales", "marketing", "communication", "management",
    "finance", "banking", "accounting",
    "html", "css", "javascript", "react",
    "project management", "leadership"
]

def extract_text_from_file(file):
    text = ""

    if file.filename.endswith(".pdf"):
        pdf = fitz.open(stream=file.file.read(), filetype="pdf")
        for page in pdf:
            text += page.get_text()
    else:
        text = file.file.read().decode("utf-8")

    return text.lower()


def extract_skills(text):

    found_skills = []

    for skill in SKILL_DB:
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text):
            found_skills.append(skill)

    return list(set(found_skills))