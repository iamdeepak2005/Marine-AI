import json
import os
from PyPDF2 import PdfReader
from fastapi import HTTPException
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from functools import lru_cache
from groq import Groq
import os


# Set localhost proxy with the appropriate port (adjust as needed)
os.environ['NO_PROXY'] = 'localhost,127.0.0.1'


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'c:\Users\deepa\Downloads\orbital-stream-426213-r2-6040f858ab8b.json'
def configure_api():
    # Load API keys if needed
    pass

def get_pdf_text(pdf_path):
    """Extract text from a PDF file."""
    text = ""
    pdf_reader = PdfReader(pdf_path)
    for page in pdf_reader.pages:
        text += page.extract_text() or ""  # Ensure text extraction is handled
    return text

def get_text_chunks(text, chunk_size=5000, chunk_overlap=1000):
    """Split text into manageable chunks."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks):
    """Create and save the FAISS vector store from text chunks."""
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")  # Save to disk once for reuse
    return vector_store

def get_conversational_chain():
    """Setup the conversational chain with Google Generative AI."""
    genai.configure(api_key='AIzaSyCivb2rBfdp-xP-nU7xCszkpOo5JdJM-24')
    
    # Define the prompt template for generating answers
    prompt_template = """
    Provide a detailed answer to the question. You should refer to the provided context where relevant, but you are also allowed to use your general knowledge to provide a comprehensive answer. If the context does not provide relevant information, give an informed answer based on what you know. If you cannot provide an answer based on both the context and your knowledge, clearly state that.

    Context:\n {context}\n
    Question: \n{question}\n
    Answer:
    """
    # Initialize the Google Generative AI model with desired parameters
    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=1)
    
    # Create a prompt template with specified input variables
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    
    # Load the QA chain with the specified model and prompt template
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

    return chain
def contains_insufficient_information(sentence):
    insufficient_phrases = [
        "not able",
        "couldn't understand",
        "cannot be answered",
        "not answerable",
        "does not contain any information",
        "not available in the context",
        "insufficient information",
        "no relevant details",
        "unable to provide an answer",
        "does not provide any insights",
        "insufficient context available",
        "not mentioned in the provided material",
        "lacking necessary details",
        "cannot be resolved with the given information",
        "information is not present",
        "no data available",
        "the context fails to address",
        "the question is beyond the provided context",
        "unanswerable",
        "does not mention",
        "do not provide any information",
        "cannot answer",
        "does not have",
        "not addressed"
    ]
    
    # Check if any of the insufficient phrases are in the sentence
    for phrase in insufficient_phrases:
        if phrase in sentence:
            return True
            
    return False


# def get_conversational_chain2(inp):
#     pass
    # # Initialize the Groq client with API key
    # client = Groq(
    #     api_key='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',
    # )

    # # Define the message format and other parameters
    # chat_completion = client.chat.completions.create(
    #     model="llama3-groq-70b-8192-tool-use-preview",
    #     messages=[{
    #         "role": "user",
    #         "content": inp
    #     }],
    #     temperature=0.5,         # Adjust temperature for creativity (0.0 to 1.0)
    #     max_tokens=1024,        # Adjust max tokens to control response length
    #     top_p=0.65,             # Top-p sampling parameter
    #     stream=True,            # Enable streaming to get incremental updates
    #     stop=None               # Set stop sequences if necessary
    # )

    # # Iterate over the streaming response to print or process the output incrementally
    # response_content = ""
    # for chunk in chat_completion:
    #     # Concatenate each chunk of content as it arrives
    #     response_content += chunk.choices[0].delta.content or ""

    # # Return the full response content
    # return response_content
def get_conversational_chain2(inp):
    api_key='AIzaSyCivb2rBfdp-xP-nU7xCszkpOo5JdJM-24'
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash-001",generation_config={"response_mime_type": "application/json"})
    prompt = (f"""
You are an expert in biology and ecology, specializing in identifying and explaining information about animals.

When given information about an organism, your task is to:

Identify the organism and provide its scientific name (genus and species).
Share detailed taxonomic information, especially emphasizing the family it belongs to.
Describe its key characteristics, including physical traits, habitat, and any unique features that distinguish it.
Highlight its ecological roles and notable behaviors in a clear and structured way.
Formatting requirements:

Use plain text with bold headings (e.g., Scientific Name, Family, Habitat, etc.).
Include line breaks (\n) or HTML <br> tags where necessary for clarity.
Avoid returning JSON-like output. Instead, present information in natural, well-structured text, easy to understand by both experts and enthusiasts.
The user has provided the following input: "{inp}"

Please respond with accurate, clear, and well-formatted text that adheres to the above guidelines.""")

    response=model.generate_content(prompt)
    try:
        print(response.text)
        # response_json = json.loads(response.text)
        return response.text
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON: {str(e)}")


@lru_cache(maxsize=128)  # Cache results to speed up repeated queries
def load_vector_store():
    """Load the FAISS vector store once for efficiency."""
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    return new_db

def user_input(user_question):
    """Handle user questions and return answers from the vector store."""
    new_db = load_vector_store()
    docs = new_db.similarity_search(user_question)

    chain = get_conversational_chain()
    
    response = chain({"input_documents": docs, "question": user_question}, return_only_outputs=True)
    return response["output_text"]

def process_pdf_and_ask_question(user_question):
    """Process PDF and handle user question."""
    raw_text = get_pdf_text(r"C:\Users\deepa\Downloads\Systematics_and_Diversity_of_Annelids.pdf")
    text_chunks = get_text_chunks(raw_text)
    
    # Generate and save vector store only if it doesn't exist
    if not os.path.exists("faiss_index"):
        get_vector_store(text_chunks)
    
    answer = user_input(user_question)
    if(contains_insufficient_information(answer)):
        answer=get_conversational_chain2(user_question)
        print(answer)
    return answer
