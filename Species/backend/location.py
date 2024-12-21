import json
from fastapi import HTTPException
import google.generativeai as genai
import os
import json 
os.environ['GOOGLE_APPLICATION_CREDENTIALS']=r'c:\Users\deepa\Downloads\orbital-stream-426213-r2-6040f858ab8b.json'

def locationSuggest(inp):
    api_key='AIzaSyCivb2rBfdp-xP-nU7xCszkpOo5JdJM-24'
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash-001",generation_config={"response_mime_type": "application/json"})
    prompt="""You are an expert in marine biology and ecology. When provided with a query that mentions multiple species or topics, analyze the query and generate a response that includes the following:
           
           1. **Locations**: For each species or topic mentioned in the query, generate an array of relevant specific geographical locations associated with that species or topic. Each location should have a name (e.g., city, country, or marine protected area) and brief details about its significance concerning the species or topic.
           
           2. **Common Points**: Provide a summary of common points related to the locations generated for each species or topic, focusing on key characteristics, species found there, and any notable features.
           
           Format the response as a JSON object like this:
           
           ```json
           {
             "species": [
               {
                 "name": "Annelids",
                 "locations": [
                   {
                     "name": "Tropical Rainforests",
                     "details": "Annelids, specifically earthworms, play a crucial role in soil health and nutrient cycling in tropical rainforests."
                   },
                   {
                     "name": "Temperate Forests",
                     "details": "Annelids are abundant in temperate forests, breaking down organic matter and improving soil structure."
                   }
                   // More locations as needed
                 ],
                 "commonPoints": "Annelids are segmented worms found in various habitats, playing critical roles in nutrient cycling."
               },
               {
                 "name": "Pandas",
                 "locations": [
                   {
                     "name": "Sichuan Province, China",
                     "details": "This region is home to the giant panda's natural habitat, which consists mainly of bamboo forests."
                   },
                   {
                     "name": "Wolong National Nature Reserve, China",
                     "details": "A significant conservation area for giant pandas, supporting a breeding program and natural habitat preservation."
                   }
                   // More locations as needed
                 ],
                 "commonPoints": "Pandas are dependent on bamboo forests for survival, highlighting the importance of habitat conservation."
               }
             ]
           }
           """
    response=model.generate_content(prompt+inp)
    try:
        response_json = json.loads(response.text)
        return response_json
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON: {str(e)}")
