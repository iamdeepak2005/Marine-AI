import json
import re
import random
from typing import List
from fastapi import APIRouter, FastAPI, File, Form, HTTPException, Depends, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import mysql.connector
import uuid
from datetime import datetime, timedelta
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from fastapi.middleware.cors import CORSMiddleware
from bcrypt import hashpw, gensalt, checkpw
from image import text_classifier, text_classifier_combined
from news import fetch_latest_articles
from location import locationSuggest
from suggest import suggest
from generative import process_pdf_and_ask_question
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import uuid
from datetime import datetime, timedelta
from suggestStart import *



# FastAPI app instance
app = FastAPI()
# Secret key for encoding and decoding JWT tokens

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your Angular app's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def send_smtp_email(email: str, pin: str):
    from_email = "dkag709@gmail.com"
    password = "mgjq ljtk frir cvck"

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = email
    msg['Subject'] = 'Password Reset PIN'

    html_content = f'''
    <p>Hello,</p>
    <p>We received a request to reset your password. Here is your 4-digit PIN:</p>
    <h2>{pin}</h2>
    <p>If you did not request a password reset, please ignore this email.</p>
    <p>Thank you!</p>
    '''

    msg.attach(MIMEText(html_content, 'html'))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()  # Secure the connection
        server.login(from_email, password)
        server.sendmail(from_email, email, msg.as_string())# Database connection

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password='Deepak@2005',  # Store your DB password securely
        database="user_management"
    )

# Helper function to hash passwords using bcrypt
def hash_password(password: str) -> str:
    return hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')

# Helper function to verify passwords
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

# Models for signup, login, and password reset
class SignupModel(BaseModel):
    username: str
    email: str
    password: str

class LoginModel(BaseModel):
    email: str
    password: str

class ResetPasswordModel(BaseModel):
    email: str
    new_password: str

class RequestPasswordResetModel(BaseModel):
    email: str
class QuestionRequest(BaseModel):
    user_question: str
    user_answer: str
class Location(BaseModel):
    query: str

class VerifyPinRequest(BaseModel):
    email: str
    pin: str

# 1. Signup Route
@app.post("/signup")
async def signup(user: SignupModel):
    conn = get_db_connection()
    cursor = conn.cursor()

    hashed_password = hash_password(user.password)

    try:
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
            (user.username, user.email, hashed_password)
        )
        conn.commit()
    except mysql.connector.Error as err:
        raise HTTPException(status_code=400, detail="Error: " + str(err))
    finally:
        cursor.close()
        conn.close()

    return {"status": "User registered successfully"}

# 2. Login Route
@app.post("/login")
async def login(user: LoginModel):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT password FROM users WHERE email = %s", (user.email,))
    result = cursor.fetchone()

    if result is None:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    hashed_password = result[0]

    # Check for null or empty hashed_password
    if not hashed_password:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # Verify the password
    try:
        if not verify_password(user.password, hashed_password):
            raise HTTPException(status_code=400, detail="Invalid email or password")
    except ValueError as e:
        raise HTTPException(status_code=400, detail="Invalid password hash")
    
    import secrets
    secret_key = secrets.token_urlsafe(32)  # Generates a secure random key
    


    return {"status": secret_key}
def hash_password_login(password: str) -> str:
    return hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')
def generate_pin(length=4):
    """Generate a random PIN of specified length."""
    return ''.join(random.choices('0123456789', k=length))
# 3. Password Reset Request (Send Reset Link)


@app.post("/request-password-reset")
async def request_password_reset(request: RequestPasswordResetModel):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch user_id based on email
    cursor.execute("SELECT id FROM users WHERE email = %s", (request.email,))
    result = cursor.fetchone()

    if result is None:
        raise HTTPException(status_code=400, detail="Email not found")

    user_id = result[0]
    reset_pin = str(random.randint(1000, 9999))  # Generate a 4-digit PIN
    expires_at = datetime.now() + timedelta(minutes=10)  # PIN expires in 10 minutes

    # Insert into password_reset_tokens table
    cursor.execute(
        "INSERT INTO user_management.password_reset_tokens (user_id, pin, expires_at) VALUES (%s, %s, %s)",
        (user_id, reset_pin, expires_at)
    )      
    conn.commit()

    # Send the email with the reset PIN
    send_smtp_email(request.email, reset_pin)

    cursor.close()
    conn.close()

    return {"status": "Reset PIN sent to email"}

# 4. Verify 4-digit PIN
@app.post("/verify-pin")
async def verify_pin(request: VerifyPinRequest):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Use the email and pin from the request body
    email = request.email
    pin = request.pin

    cursor.execute(
        "SELECT user_id FROM password_reset_tokens WHERE pin = %s AND expires_at > NOW() AND is_used = 0",
        (pin,)
    )
    result = cursor.fetchone()

    if result is None:
        raise HTTPException(status_code=400, detail="Invalid or expired PIN")

    # Mark the PIN as used
    cursor.execute("UPDATE password_reset_tokens SET is_used = 1 WHERE pin = %s", (pin,))
    conn.commit()

    cursor.close()
    conn.close()

    return {"status": "PIN verified successfully"}
# 5. Reset Password after PIN verification
@app.post("/reset-password-with-pin")
async def reset_password_with_pin(request: ResetPasswordModel):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Use request.email and request.new_password instead of separate parameters
    cursor.execute("SELECT id FROM users WHERE email = %s", (request.email,))
    result = cursor.fetchone()

    if result is None:
        raise HTTPException(status_code=400, detail="User not found")

    user_id = result[0]
    hashed_password = hash_password_login(request.new_password)

    cursor.execute("UPDATE users SET password = %s WHERE id = %s", (hashed_password, user_id))
    conn.commit()

    cursor.close()
    conn.close()

    return {"status": "Password has been reset successfully"}

def hash_password(password: str):
    # Implement password hashing logic (e.g., bcrypt)
    return password

# 5. Question Request Route (PDF-related functionality)
class QuestionRequest(BaseModel):
    user_question: str

@app.post("/ask-question/")
async def ask_question(request: QuestionRequest):
    try:
        # Call the function to process the PDF and ask the question
        answer = process_pdf_and_ask_question(request.user_question)
        questions=suggest(request.user_question,answer)
        return {"answer": answer,'question':questions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.post("/suggest")
async def suggestQuestion(user_question: str, user_answer: str):
    try:
        # Call the function to process the conversation and ask the question
        answer = suggest(user_question, user_answer)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    
@app.get("/suggestStart")
async def suggestStart123():
    try:
        # Call the function to process the conversation and ask the question
        answer = suggestStart()
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
@app.post("/suggest-locations")
async def suggest_locations(request:Location):
    try:
        response = locationSuggest(request.query)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.get("/news")
async def news():
    try:
        response = fetch_latest_articles()
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.post("/image")
async def upload_images_for_classification(
    text: str = Form(...),  # Single text input
    files: List[UploadFile] = File(...)  # Multiple files
):
    try:
        # Read all image files and convert them to bytes
        image_data_list = [await file.read() for file in files]

        # Call the text classifier with the provided images and text
        result = text_classifier(image_data_list, text)

        # Parse the classifier result
        parsed_result = json.loads(result)

        # Check for individual responses and a final conclusion in the parsed result
        if (
            isinstance(parsed_result, dict)
            and "individual_responses" in parsed_result
            and "final_conclusion" in parsed_result
        ):
            # Valid result format, return as a response
            return JSONResponse(content={
                "individual_responses": parsed_result["individual_responses"],
                "final_conclusion": parsed_result["final_conclusion"]
            }, status_code=200)

        elif "error" in parsed_result:
            # Handle errors returned by the classifier
            return JSONResponse(content={
                "error": "Classifier returned an error.",
                "details": parsed_result["error"]
            }, status_code=400)

        else:
            # Unexpected result format
            return JSONResponse(content={
                "error": "Unexpected result format from classifier.",
                "details": parsed_result  # Include raw result for debugging purposes
            }, status_code=400)

    except json.JSONDecodeError as e:
        # Handle JSON parsing errors
        return JSONResponse(content={
            "error": "Failed to parse classifier response.",
            "details": str(e)
        }, status_code=500)

    except Exception as e:
        # Handle all other exceptions
        return JSONResponse(content={"error": str(e)}, status_code=500)
