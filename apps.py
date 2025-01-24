import streamlit as st
from pydantic import BaseModel, EmailStr, ValidationError
from langchain.document_loaders import PyPDFLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool
from dotenv import load_dotenv
from pydantic import BaseModel, EmailStr
from typing import Optional
import json

# Load environment variables
load_dotenv()

# ---- Document Querying Setup ----
loader = PyPDFLoader("uploads\shushilshah_dataanalyst.pdf")
documents = loader.load()
index_creator = VectorstoreIndexCreator(
    embedding=OpenAIEmbeddings(),
    vectorstore_cls=FAISS
)
index = index_creator.from_documents(documents)

# Initialize ChatOpenAI
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)


class UserInfo(BaseModel):
    name: str
    phone: str
    email: Optional[EmailStr] = None  # optional
    appointment_date: Optional[str] = None  # optional


def validate_phone(phone: str):
    if len(phone) != 10 or not phone.isdigit():
        raise ValueError("Phone number must be a 10-digit number.")
    return phone


# ---- Streamlit App ----
st.title("Chatbot with Document Querying and Appointment Booking")

options = st.sidebar.selectbox(
    "Choose an action", ["Query Document", "Book Appointment", "Call User"])

if options == "Query Document":
    st.header("Query the Document")
    question = st.text_input("Enter your question:")
    if st.button("Get Answer"):
        try:
            response = index.query(question, llm=llm)
            st.success(f"Answer: {response}")
        except Exception as e:
            st.error(f"Error: {str(e)}")

elif options == "Book Appointment":
    st.header("Book an Appointment")
    name = st.text_input("Name")
    phone = st.text_input("Phone Number")
    email = st.text_input("Email")
    date_query = st.date_input("select date")

    if st.button("Book Appointment"):
        try:
            phone = validate_phone(phone)
            normalized_date = date_query.strftime("%Y-%m-%d")
            user_info = UserInfo(name=name, phone=phone,
                                 email=email, appointment_date=normalized_date)

            st.success(f"Appointment booked successfully! {user_info}")
        except ValidationError as e:
            st.error(f"Validation Error: {e.errors()}")
        except Exception as e:
            st.error(f"Error: {str(e)}")

elif options == "Call User":
    st.header("Call a User")
    name = st.text_input("Name")
    phone = st.text_input("Phone Number")

    if st.button("Call User"):
        try:
            if phone:
                import re
                pattern = r"^\+?[0-9\s\-]+$"
                if re.match(pattern, phone):
                    st.success(f"Phone number {phone} is valid")
                else:
                    st.error("Invalid phone number format.")
            else:
                st.warning("Please enter a phone number")

            user_info = UserInfo(name=name, phone=phone)
            user_info_dict = user_info.model_dump()

            tools = [
                Tool(
                    name="CallUser",
                    func=lambda input_data: process_input(input_data),
                    description="Schedules a call with the user."
                )
            ]

            def process_input(input_data):
                if isinstance(input_data, str):
                    input_data = json.loads(input_data)
                return f"Calling {input_data['name']} at {input_data['phone']}."

            agent = initialize_agent(tools,
                                     llm, agent="zero-shot-react-description")

            response = agent.run({"input": json.dumps(user_info_dict)})
            st.success("Your call has been scheduled successfully!")
        except Exception as e:
            st.error(f"Error: {str(e)}")
