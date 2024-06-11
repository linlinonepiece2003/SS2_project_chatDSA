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
    memory = ConversationBufferMemory( memory_key ='chat_history', return_messages = True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm = llm,
        retriever = vector_store.as_retriever(),
        memory = memory
    )
    return conversation_chain
    # prompt_template = """
    # Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
    # provided context just say, "answer is not available in the context", don't provide the wrong answer\n\n
    # Context:\n {context}?\n
    # Question: \n{question}\n

    # Answer:
    # """

    # model = ChatGoogleGenerativeAI(model="gemini-pro",
    #                          temperature=0.3)

    # prompt = PromptTemplate(template = prompt_template, input_variables = ["context", "question"])
    # chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

    # return chain



# def user_input(user_question):
    # response = st.session_state.conversation({'question': user_question})
    # st.session_state.chat_history = response['chat_history']

    # for i, message in enumerate(st.session_state.chat_history):
    #     if i % 2 == 0:
    #         st.write(user_template.replace(
    #             "{{MSG}}", message.content), unsafe_allow_html=True)
    #     else:
    #         st.write(bot_template.replace(
    #             "{{MSG}}", message.content), unsafe_allow_html=True)
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

    # Display chat history in reverse order
    for message in reversed(st.session_state.chat_history):
        if message['is_user']:
            st.write(user_template.replace("{{MSG}}", message['content']), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace("{{MSG}}", message['content']), unsafe_allow_html=True)

def main():
    load_dotenv()
    st.set_page_config(page_title="Data structure Algorithms botmaster",
                       page_icon=":computer:")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    

    st.header("Data structure Algorithms Botmaster :computer:")
   # Custom HTML and CSS for input box with button
    st.markdown("""
    <style>
    .input-container {
        display: flex;
        align-items: center;
    }
    .input-container input[type='text'] {
        flex: 1;
        padding: 10px;
        border: 1px solid #ccc;
        border-radius: 5px 0 0 5px;
    }
    .input-container button {
        padding: 10px;
        border: none;
        background-color: #007bff;
        color: white;
        border-radius: 0 5px 5px 0;
        cursor: pointer;
    }
    .input-container button:hover {
        background-color: #0056b3;
    }
    </style>
    <div class="input-container">
        <input id="user_question" type="text" placeholder="Ask a question about your documents:"/>
        <button onclick="sendQuestion()">Send 🛩️</button>
    </div>
    <script>
    function sendQuestion() {
        const question = document.getElementById('user_question').value;
        if (question) {
            fetch('/submit_question', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ question: question }),
            }).then(response => {
                if (response.ok) {
                    const urlParams = new URLSearchParams(window.location.search);
                    urlParams.set('question', question);
                    window.location.search = urlParams.toString();
                }
            });
        }
    }
    </script>
    """, unsafe_allow_html=True)

    query_params = st.experimental_get_query_params()
    if query_params and 'question' in query_params:
        user_question = query_params['question'][0]
        if user_question:
            user_input(user_question)
    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader(
            "Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing"):
                # get pdf text
                raw_text = get_pdf_text(pdf_docs)
                # Ensure text was extracted
                if not raw_text.strip():
                    st.error("No text could be extracted from the provided PDFs.")
                    return

                # get the text chunks
                text_chunks = get_text_chunks(raw_text)

                # create vector store
                vectorstore = get_vector_store(text_chunks)
                st.success("Done")

                # create conversation chain
                st.session_state.conversation = get_conversational_chain(vectorstore)
                if not st.session_state.conversation:
                    st.error("Failed to create conversational chain. Please check the model configuration.")


if __name__ == "__main__":
    main()