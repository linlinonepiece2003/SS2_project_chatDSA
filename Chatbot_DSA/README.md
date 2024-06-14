1. INTRODUCTION 
A Python software called DSA Tutor Chatbot enables you to have conversations with many PDF documents related to DSA subjects. It is an API-based Germini assistant created to aid students facing difficulties in a specific subject. This chatbot offers prompt responses to students' study-related inquiries. It functions as a personalized ChatGPT chatbot, tailored and trained with data from the relevant PDF documents.

2. How it works 

2.1 PDF Loading: The app reads multiple PDF documents and extracts their text content. 

2.2 Text Chunking: The extracted text is divided into smaller chunks that can be processed effectively. 

2.3 Language Model: The application utilizes a language model to generate vector representations (embeddings) of the text chunks. 

2.4 Similarity Matching: When you ask a question, the app compares it with the text chunks and identifies the most semantically similar ones. 

2.5 Response Generation: The selected chunks are passed to the language model, which generates a response based on the relevant content of the PDFs.

3. Dependencies & install 
Dependencies and Installation
*****************************
To run the DSA Tutor Chatbot please follow these steps:

- Clone the repository to your local machine.

- Type: >Select python -> enter create virtual Environment -> choose Venv (type at search bar in Visual Studio code)

- Install the required dependencies by running the following command:

pip install -r requirements.txt

pip install -U langchain community

- Obtain an API key from OpenAI and add it to the .env file in the project directory.

OPENAI_API_KEY=your_secret_api_key


- Ensure that you have installed the required dependencies and added the OpenAI API key to the .env file.

- Run the bot.py file using the Streamlit CLI. Execute the following command:
  
streamlit run bot.py

The application will launch in your default web browser, displaying the user interface.

Load PDF documents relating DSA subject into the app by following the provided instructions.

Ask questions in natural language about the loaded PDFs using the chat interface.


