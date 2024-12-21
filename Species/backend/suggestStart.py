import json
from fastapi import HTTPException
import google.generativeai as genai
import os
import json 
os.environ['GOOGLE_APPLICATION_CREDENTIALS']=r'c:\Users\deepa\Downloads\orbital-stream-426213-r2-6040f858ab8b.json'

def suggestStart():
    api_key='AIzaSyCivb2rBfdp-xP-nU7xCszkpOo5JdJM-24'
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash-001",generation_config={"response_mime_type": "application/json"})
    
    prompt = """"Generate a list of conversational and engaging questions about annelids and other marine species, focusing on recent trends in marine biology. Each question should have a concise title that sparks curiosity and encourages interactive discussion. Please provide the output in the following format:

questions = [
  {title: "...", question: "..."},
  {title: "...", question: "..."},
  {title: "...", question: "..."},
  ...
];

Some topics to consider include:
1. The latest research on annelid behaviors or adaptations.
2. New discoveries about marine species and their ecosystems.
3. Recent conservation efforts in marine biology.
4. Fascinating or little-known facts about marine species.
5. Marine species’ adaptations to climate change or environmental changes.

Ensure the questions are thought-provoking, suitable for conversations between marine biology enthusiasts, and that the titles are short and engaging. Focus on making the questions interesting and inviting for discussion.
"""

    response=model.generate_content(prompt)
    try:
        response_json = json.loads(response.text)
        return response_json
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON: {str(e)}")
