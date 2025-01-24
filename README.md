# Chatbot with Document Querying and Appointment Booking

This is a chatbot application built using **Streamlit** and **LangChain** to query documents, book appointments, and validate phone numbers. It integrates the OpenAI GPT model for conversational AI, and utilizes Pydantic for input validation.

## Features

1. **Document Querying**: Allows the user to query a document (in PDF format) for specific information.
2. **Appointment Booking**: Enables users to book appointments by providing their name, phone number, email, and date.
3. **User Call Scheduling**: Validates phone numbers and schedules a call with the user.

## Requirements

Ensure you have the following Python packages installed:

- `streamlit`
- `pydantic`
- `langchain`
- `faiss-cpu`
- `openai`
- `python-dotenv`
- `json`

How It Works

1. Document Querying:
   The app allows the user to query a loaded document using the GPT-3.5 model. It uses LangChain's PyPDFLoader to load a PDF and FAISS for indexing, allowing fast document querying.

2. Appointment Booking:
   Users can enter their name, phone number, email (optional), and appointment date. The phone number is validated to ensure it is a 10-digit number. Upon successful input, the appointment is confirmed.

3. Call Scheduling:
   The user can input their name and phone number. The phone number is validated for format correctness. The application then schedules a call with the user via a LangChain agent, which can be customized to connect with other services.

# Usage

## Query Document:

In the sidebar, select "Query Document" to ask questions related to the document content. Enter your question and click the "Get Answer" button to retrieve a response.

## Book Appointment:

Select "Book Appointment" from the sidebar. Enter your details (name, phone number, email, and appointment date) and click "Book Appointment" to schedule it.

## Call User:

In this section, enter the user's name and phone number to schedule a call. It will validate the phone number and return success or error messages accordingly.

# Code Explanation

## Key Components:

1. PyPDFLoader: Loads PDF documents for querying.
2. LangChain Vectorstore: Uses FAISS for indexing and searching the document.
3. Pydantic: Validates user input (such as phone numbers and email).
4. ChatOpenAI: Uses OpenAI GPT-3.5 model to handle document queries and natural language responses.
5. Streamlit: Provides the user interface for interacting with the chatbot and booking appointments.

## Key Functions:

1. validate_phone: Ensures the phone number is 10 digits long.
2. process_input: Handles user input for call scheduling and generates a response.
3. initialize_agent: Initializes a LangChain agent for call scheduling.

# Contributing

Feel free to open an issue or pull request if you'd like to contribute to the project.
