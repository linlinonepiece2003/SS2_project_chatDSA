import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.chains.question_answering import load_qa_chain
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template
# from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
                    
import json

load_dotenv()
os.getenv("GOOGLE_API_KEY")
# api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
# if not api_key:
#     st.error("GOOGLE_API_KEY not found. Please set the correct API key in your environment variables.")
#     st.stop()

def get_pdf_text(pdf_docs):
    text=""
    for pdf in pdf_docs:
        pdf_reader= PdfReader(pdf)
        for page in pdf_reader.pages:
            text+= page.extract_text()
    return  text



def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks


def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    # vector_store.save_local("faiss_index")
    return vector_store


def get_conversational_chain(vector_store):
    try:
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest", temperature=0.3)
    except Exception as e:
        st.error(f"Failed to initialize ChatGoogleGenerativeAI: {e}")
        return None
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    retriever = vector_store.as_retriever()
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory
    )
    return conversation_chain

def save_data(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f)

def load_data(filename):
    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        with open(filename, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                # Log error or handle empty/invalid JSON file
                return []
    else:
        return []
def user_input(user_question):
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Ensure the conversation chain is not None
    if st.session_state.conversation is None:
        st.error("Conversation chain is not initialized. Please process the documents first.")
        return

    response = st.session_state.conversation({'question': user_question})
    
    # Debugging: Print the structure of response
    # st.write("Response structure:", response)
    
    st.session_state.chat_history.append({'content': user_question, 'is_user': True})
    
    # Ensure response structure is as expected
    if 'answer' in response:
        st.session_state.chat_history.append({'content': response['answer'], 'is_user': False})
    else:
        st.write("Unexpected response format:", response)
        st.session_state.chat_history.append({'content': "Error: Unexpected response format.", 'is_user': False})
     # Create a markdown element to display the chat history
    chat_history_md = st.markdown("", unsafe_allow_html=True)

    # Update the chat history markdown element
    chat_history_html = ""
    for message in reversed(st.session_state.chat_history):
        if message['is_user']:
            chat_history_html += user_template.replace("{{MSG}}", message['content'])
        else:
           chat_history_html += bot_template.replace("{{MSG}}", message['content'])
    chat_history_md.markdown(chat_history_html, unsafe_allow_html=True)
    # Save the chat history after each interaction
    save_data(st.session_state.chat_history, "chat_history.json")
    
def clear_chat_history():
    st.session_state.chat_history = []
    save_data(st.session_state.chat_history, "chat_history.json")
    
def save_processed_files(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f)

def load_processed_files(filename):
    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        with open(filename, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    else:
        return {}   
def clear_processed_files():
    st.session_state.processed_files = {}
    save_processed_files(st.session_state.processed_files, "processed_files.json")
    
    
def main():
    load_dotenv()
    st.set_page_config(page_title="Data structure Algorithms botmaster",
                       page_icon=":computer:")
    st.write(css, unsafe_allow_html=True)

    processed_files_filename = "processed_files.json"  # Định nghĩa biến

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = load_data("chat_history.json")
    if "processed_files" not in st.session_state:
        st.session_state.processed_files = load_processed_files(processed_files_filename)

    st.header("Data structure Algorithms Botmaster :computer:")

    with st.container():
        col1, col2 = st.columns([4, 1])
        user_question = col1.text_input("Ask a question about your documents:")
        send_button = col2.button("Send", key="send_button")
        st.markdown("<style>.stButton{margin-top: 25px;}</style>", unsafe_allow_html=True)

        if send_button or st.session_state.get("user_question") != user_question:
            user_input(user_question)
            st.session_state.user_question = user_question

    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader(
            "Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing"):
                raw_text = get_pdf_text(pdf_docs)
                if not raw_text.strip():
                    st.error("No text could be extracted from the provided PDFs.")
                    return

                text_chunks = get_text_chunks(raw_text)
                vectorstore = get_vector_store(text_chunks)
                st.success("Done")
                st.session_state.processed_files = {
                    "raw_text": raw_text,
                    "text_chunks": text_chunks
                }
                save_processed_files(st.session_state.processed_files, processed_files_filename)
                st.session_state.conversation = get_conversational_chain(vectorstore)
                if not st.session_state.conversation:
                    st.error("Failed to create conversational chain. Please check the model configuration.")

        # Check if there are processed files in the session state
        if "processed_files" in st.session_state and st.session_state.processed_files:
            vectorstore = get_vector_store(st.session_state.processed_files['text_chunks'])
            st.session_state.conversation = get_conversational_chain(vectorstore)

            st.markdown("<br><br><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)  # Add some space before the buttons

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Delete history"):
                clear_chat_history()
                st.success("Chat history cleared successfully.")
        with col2:
            if st.button("Delete files"):
                clear_processed_files()
if __name__ == "__main__":
    main()
    
