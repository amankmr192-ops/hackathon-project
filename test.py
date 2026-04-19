from utils.utils.extractor import extract_info
sample_text = """
John Doe
Skills: Python, Machine Learning, FastAPI
Experience: 2 years
Projects: Resume Analyzer, Chatbot
"""

result = extract_info(sample_text)

print(result)