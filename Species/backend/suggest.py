import json
from fastapi import HTTPException
import google.generativeai as genai
import os
import json 
os.environ['GOOGLE_APPLICATION_CREDENTIALS']=r'c:\Users\deepa\Downloads\orbital-stream-426213-r2-6040f858ab8b.json'

def suggest(question ,answer):
    api_key='AIzaSyCivb2rBfdp-xP-nU7xCszkpOo5JdJM-24'
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash-001",generation_config={"response_mime_type": "application/json"})
    
    prompt = f"""Analyze the following conversation and, based on it, suggest the most interesting and relevant follow-up questions. Focus only on generating insightful questions and do not provide any answers. 
Conversation:
1. Question: """+question+"""
   Answer: """+answer+"""

Now, based on the above conversation, generate the next few thought-provoking questions that will continue the discussion in a meaningful and engaging way. Present the questions in the following format:
questions = [
    "First insightful question?",
    "Second insightful question?",
    "Third insightful question?"
]
"""

    response=model.generate_content(prompt)
    try:
        response_json = json.loads(response.text)
        return response_json
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON: {str(e)}")
