# import os
# from langchain import PromptTemplate
# from langchain.chains.question_answering import load_qa_chain
# from langchain.document_loaders import PyPDFDirectoryLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.vectorstores import Chroma
# from dotenv import load_dotenv
# import google.generativeai as genai
# from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI

# # Load the API key from the .env file
# load_dotenv()
# GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# # Configure the generative AI
# genai.configure(api_key=GOOGLE_API_KEY)

# # Load PDF documents
# loader = PyPDFDirectoryLoader("path/to/your/pdf_directory")  # Update this path
# data = loader.load()

# # Split the text into chunks
# text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
# content = "\n\n".join(str(page.page_content) for page in data)
# texts = text_splitter.split_text(content)
# print(len(texts))
# print(texts[0])

# # Create embeddings and vector store
# embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
# vector_store = Chroma.from_texts(texts, embeddings).as_retriever()

# # Define the prompt template
# prompt_template = """
#   Please answer the question in as much detail as possible based on the provided context.
#   Ensure to include all relevant details. If the answer is not available in the provided context,
#   kindly respond with "The answer is not available in the context." Please avoid providing incorrect answers.
# \n\n
#   Context:\n {context}?\n
#   Question: \n{question}\n

#   Answer:
# """

# prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

# # Initialize the chat model
# model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)

# # Load the QA chain
# chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

# # Get the user's question
# question = input("Enter your question: ")

# # Retrieve relevant documents
# docs = vector_store.get_relevant_documents(question)

# # Generate the response
# response = chain({"input_documents": docs, "question": question}, return_only_outputs=True)
# print(response)