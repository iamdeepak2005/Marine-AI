import json
from fastapi import HTTPException
import google.generativeai as genai
import os
import json 
os.environ['GOOGLE_APPLICATION_CREDENTIALS']=r'c:\Users\deepa\Downloads\orbital-stream-426213-r2-6040f858ab8b.json'

from PIL import Image
import google.generativeai as genai
import os
import json
import io
def text_classifier_combined(image_data_list, user_text, previous_response=""):
    try:
        # Initialize the generative model
        model = genai.GenerativeModel("gemini-1.5-pro")

        # Prepare a list to store individual image responses
        image_responses = []

        # Process each image individually
        for idx, image_data in enumerate(image_data_list):
            # Convert image data into a readable format
            image_stream = io.BytesIO(image_data)
            image = Image.open(image_stream)

            # Dummy description generation (replace this with OCR or ML-based image analysis)
            image_summary = f"Image {idx + 1}: [description of content based on actual analysis]"

            # Define a prompt for this image
            prompt = (f"""
            You are a marine biology expert. Analyze the following image content and user input to identify the annelid species:
            - User Input: {user_text}
            - Previous Response: {previous_response}
            - Image Context: {image_summary}
            
            Provide details about the species name, identifying features, habitat, and ecological roles. Conclude with how this image relates to the other inputs if possible.""")
            
            # Generate content using the model
            response = model.generate_content([prompt], stream=False)

            # Extract and save the response for this image
            if response.candidates and response.candidates[0].content.parts:
                image_response = "\n".join([part.text for part in response.candidates[0].content.parts])
            else:
                image_response = "No meaningful content generated for this image."

            # Append the response for this image to the list
            image_responses.append(f"Image {idx + 1} Analysis:\n{image_response}\n")

        # Combine all image responses
        combined_image_responses = "\n".join(image_responses)

        # Define the final prompt for concluding response
        final_prompt = (f"""
        Based on the analysis of the following images and user input, provide a comprehensive conclusion:
        - User Input: {user_text}
        - Previous Response: {previous_response}
        - Combined Image Analyses:\n{combined_image_responses}
        
        Conclude with the identified species, its characteristics, and how it connects to the overall input.""")
        
        # Generate the final cohesive response
        final_response = model.generate_content([final_prompt], stream=False)

        # Extract the final content
        if final_response.candidates and final_response.candidates[0].content.parts:
            conclusion = "\n".join([part.text for part in final_response.candidates[0].content.parts])
        else:
            conclusion = "No final conclusion could be generated."

        return {
            "individual_responses": image_responses,
            "final_conclusion": conclusion
        }

    except Exception as e:
        print(f"Error in text_classifier_combined: {e}")
        return {"error": str(e)}


def text_classifier(image_data_list, user_text):
    try:
        # Initialize the model
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash-001",
            # generation_config={"response_mime_type": "application/json"}
        )

        individual_responses = []

        # Process each image in the list
        for image_data in image_data_list:
            try:
                # Open the image from the byte stream
                image_stream = io.BytesIO(image_data)
                image = Image.open(image_stream)

                # Generate content for the image
                image_response = model.generate_content(
                    [f"Analyze the contents of this image and provide insights.", image],
                    stream=False
                )

                if image_response.candidates and image_response.candidates[0].content.parts:
                    extracted_text = image_response.candidates[0].content.parts[0].text
                    individual_responses.append(extracted_text)
                else:
                    individual_responses.append("No meaningful content extracted from this image.")
            except Exception as e:
                individual_responses.append(f"Error processing image: {str(e)}")

        # Combine analyses into a single conclusion
        combined_analysis = "\n".join(individual_responses)

        final_prompt = f"""
        Based on the analysis of the provided images, generate a comprehensive conclusion:
        - User Input: {user_text}
        - Combined Image Analyses:\n{combined_analysis}
        
        Provide a detailed conclusion, identifying species, characteristics, and how they connect to the input.
        """

        # Generate the final response
        final_response = model.generate_content([final_prompt], stream=False)

        if final_response.candidates and final_response.candidates[0].content.parts:
            final_conclusion = final_response.candidates[0].content.parts[0].text
            return json.dumps({
                "individual_responses": individual_responses,
                "final_conclusion": final_conclusion
            })
        else:
            return json.dumps({"error": "No content found in final conclusion."})

    except Exception as e:
        return json.dumps({"error": str(e)})