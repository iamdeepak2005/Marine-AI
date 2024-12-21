# Marine AI Project with Gemini Text and Image Recognition

## Overview

This project integrates AI-based text and image recognition capabilities with a focus on the marine industry. Using **Gemini Text** and **Image Recognition Models**, the system is designed to extract important information from documents, images, and handwritten texts. It leverages **Angular** for the frontend and **FastAPI** and **Python** for the backend, ensuring a robust and efficient AI-driven solution.

## Technologies Used

- **AI Models**: Gemini Text and Image Recognition
- **Frontend**: Angular
- **Backend**: FastAPI (Python)
- **OCR**: Integration with EasyOCR and other recognition tools for extracting text from images
- **Database**: [Add your database technology here, if applicable]
- **Deployment**: [Mention your deployment platforms and CI/CD pipeline, if any]

## Features

- **Marine Document Recognition**: The system can process images and documents related to marine activities, extracting text such as bill details, item descriptions, customer information, and other relevant fields.
- **Text and Image Extraction**: AI models accurately recognize and extract handwritten or printed text from images, enabling seamless integration with Angular for real-time interaction.
- **FastAPI Backend**: The FastAPI server handles API requests from the frontend and interacts with AI models, ensuring fast and efficient data processing.
- **Angular Frontend**: The Angular application provides a user-friendly interface for displaying the extracted information and interacting with the system.
- **AI-Powered Search**: Enables searching and filtering of extracted data such as customer names, bill numbers, and more.

## Installation

To run this project locally, follow the steps below:

### Prerequisites

- Python 3.11 or later
- Node.js (for Angular)
- FastAPI
- EasyOCR or any OCR tool of your choice
- Gemini AI API credentials (for integration with the Gemini text and image recognition models)

### Setup Instructions

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/marine-ai-project.git
   cd marine-ai-project
2.**Backend Setup (FastAPI and Python):**

Create a virtual environment and install the required Python packages:

      ```bash
      python -m venv venv
      source venv/bin/activate  # On Windows use venv\Scripts\activate
      pip install -r requirements.txt

**Obtain the Gemini AI API Key and save it as an environment variable.**

For Linux/macOS:

      ```bash
      Copy code
      export GEMINI_API_KEY="your_api_key_here"
      For Windows (in Command Prompt):

      ```bash
      Copy code
      set GEMINI_API_KEY=your_api_key_here
Note: Replace "your_api_key_here" with the actual Gemini API key you receive.

**Frontend Setup (Angular):**

Install Node.js and Angular CLI if not already installed:

      ```bash
      npm install -g @angular/cli
      Navigate to the frontend directory:

      ```bash
      
      cd frontend
      Install the necessary dependencies:

      ```bash
      npm install
**Run the Backend (FastAPI Server):**

In the backend directory, run the FastAPI server:

      ```bash
      uvicorn main:app --reload
      This will start the FastAPI server at http://localhost:8000.

**Run the Frontend (Angular Application):**

In the frontend directory, run the Angular development server:

      ```bash
      ng serve
The Angular app will be available at http://localhost:4200.

**(Optional) Deploy Using NGINX:**

If you're deploying this project with NGINX, follow these steps:

Build the Angular application:

      ```bash
      ng build --prod
This will create a dist/ folder with production-ready files.

Configure NGINX to serve the Angular app:

Update your NGINX configuration file (/etc/nginx/nginx.conf or /etc/nginx/sites-available/default) to point to the dist/ folder where Angular files are built. Example configuration:

nginx
server {
    listen 80;
    server_name yourdomain.com;

    root /path/to/your/project/frontend/dist/;

    location / {
        try_files $uri $uri/ /index.html;
    }
}
Restart NGINX:

      ```bash
      sudo systemctl restart nginx
Ensure FastAPI is running as a background service using a tool like Gunicorn or Uvicorn in a production environment.

Usage
Text and Image Recognition: Upload images or documents related to marine activities, and the AI will extract relevant text, which can be displayed in the Angular frontend.
Search and Filter: Use the search functionality to find specific records based on customer names, bill numbers, etc.
API Endpoints: Use FastAPI endpoints to interact with the backend for extracting data, triggering recognition, and accessing recognized text.
Contributing
Contributions are welcome! Feel free to fork the repository, open issues, and submit pull requests. Please follow the coding standards and include tests for new features.

License
This project is licensed under the MIT License - see the LICENSE file for details.

markdown
Copy code

### Key Steps for Copying:
- Clone the repository.
- Set up your **Gemini API key** as an environment variable.
  - On **Linux/macOS**, use `export GEMINI_API_KEY="your_api_key_here"`.
  - On **Windows**, use `set GEMINI_API_KEY=your_api_key_here` in the Command Prompt.
- Follow the instructions for setting up the backend and frontend, including installing dependencies and running both servers.
- Optionally, configure **NGINX** for deployment if you need to host the project on a server.
