from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import json
import re

load_dotenv()

llm = ChatMistralAI(
    model="mistral-medium",
    temperature=0.2
)

def clean_json_output(content: str):
    content = re.sub(r"```json|```", "", content)
    return content.strip()

def extract_info(text: str):

    prompt = ChatPromptTemplate.from_template("""
You are a strict JSON generator.

Extract structured information from the resume.

Return ONLY valid JSON.
Do NOT include explanations, markdown, or extra text.

Format:
{{
  "Skills": ["skill1", "skill2"],
  "Experience": 0,
  "Projects": ["project1", "project2"]
}}

Rules:
- Skills must be a list of strings
- Experience must be a number (years)
- Projects must be a list
- If something is missing, return empty list or 0

Resume:
{text}
""")

    try:
        chain = prompt | llm
        response = chain.invoke({"text": text})

        cleaned = clean_json_output(response.content)

        data = json.loads(cleaned)

        return data

    except Exception as e:
        return {
            "error": "Extraction failed",
            "details": str(e),
            "raw_output": response.content if 'response' in locals() else None
        }