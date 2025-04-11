##import json
##from PyPDF2 import PdfReader
##
##def extract_questions_answers(pdf_path):
##    reader = PdfReader(pdf_path)
##    questions_answers = {}
##    question_id = 1
##
##    for page in reader.pages:
##        text = page.extract_text()
##        lines = text.split("\n")
##        
##        for line in lines:
##            if line.startswith("Q") and "." in line:
##                question, *answer = line.split("Ans:")
##                question = question.strip()
##                answer = "Ans: " + " ".join(answer).strip()
##                questions_answers[f"Q{question_id}"] = {
##                    "question": question,
##                    "answer": answer
##                }
##                question_id += 1
##
##    return questions_answers
##
##def save_to_json(data, json_path):
##    with open(json_path, "w", encoding="utf-8") as f:
##        json.dump(data, f, indent=4, ensure_ascii=False)
##
### Path to your PDF file
##pdf_path = "MyPerf.pdf"
##
### Path to save the JSON file
##json_path = "questions_answers.json"
##
### Extract and save
##qa_data = extract_questions_answers(pdf_path)
##save_to_json(qa_data, json_path)
##print(f"Extracted data saved to {json_path}")

import json
import re
from PyPDF2 import PdfReader

def clean_text(text):
    """Clean text by removing extra spaces and line breaks."""
    return re.sub(r"\s+", " ", text).strip()

def extract_questions_answers_correctly(pdf_path):
    global reader
    reader = PdfReader(pdf_path)
    questions_answers = {}
    question_id = 1

    # Iterate through all pages in the PDF
    for page in reader.pages:
        text = page.extract_text()
        lines = text.split("\n")  # Split by lines
        
        buffer = ""
        for line in lines:
            buffer += line.strip() + " "  # Reconstructing text for better parsing
        
        # Split questions and answers by pattern
        qa_pairs = re.findall(r"(Q\d+\..*?Ans:\s+.*?)(?=Q\d+\.|$)", buffer)
        
        for qa in qa_pairs:
            question_match = re.match(r"(Q\d+\..*?)Ans:", qa)
            answer_match = re.search(r"Ans:\s+(.*)", qa)
            
            question = clean_text(question_match.group(1)) if question_match else ""
            answer = clean_text(answer_match.group(1)) if answer_match else ""
            
            questions_answers[f"Q{question_id}"] = {
                "question": question,
                "answer": answer
            }
            question_id += 1

    return questions_answers

def save_to_json(data, json_path):
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# Path to your PDF file
pdf_path = "MyPerf.pdf"

# Path to save the JSON file
json_path = "Ques.json"

# Extract and save
qa_data = extract_questions_answers_correctly(pdf_path)
save_to_json(qa_data, json_path)
print(f"Correctly extracted data saved to {json_path}")
