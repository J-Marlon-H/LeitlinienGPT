from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationalRetrievalChain
import param
from dotenv import load_dotenv
import os
import openai
# explanation

# environment setup
# dotenv_path is set to the path of an environment file KEYs.env
# environment variables are key-value pairs that can be used to store configuration setting and sensitive info

# Question: Where can I find this file?
# the .env file is a simple text file. Each line in the file is a key-value pair 
# API_KEY=yourapikey123
dotenv_path = 'KEYs.env'  
# environment variables are loaded from this file
_ = load_dotenv(dotenv_path)

# OpenAI API key is set using an environment variable
# critical for accessing OpenAIs services
openai.api_key = os.environ['OPENAI_API_KEY']

# Chroma vector database setup
persist_directory = 'docs/chroma/'
# embedding object is created 
embedding = OpenAIEmbeddings()
# for soring and retrieving vector representations of the text data
vectordb = Chroma(
    persist_directory=persist_directory,
    embedding_function=embedding
)

# PROMPT TEMPLATE
# No_Doc is a string to be used when no relevant documents are found
No_Doc = "Die hinterlegten Leitlinien Dokumente enthalten keine Informationen zu Ihrer Frage."

# defines a prompt template in a structured format, guiding how the AI should format its responses
template = """Beantworten Sie die Frage am Ende des Textes anhand der folgenden Informationen. 
Geben Sie bei der Antwort so viele relevante Hintergrundinformationen mit wie Möglich.
Die Antwort sollte nicht länger als 8 Sätze sein.
Kontext:
{context}
Frage: {question}
Hilfreiche Antwort:"""
prompt = PromptTemplate.from_template(template)

# MODEL LOADING FUNCTION
# This function initializes a conversational retrieval chain model


def load_model():
    qa = ConversationalRetrievalChain.from_llm(
        # ChatOpenAI as the language model
        llm=ChatOpenAI(temperature=0), 
        # vectordb as a retriever
        retriever=vectordb.as_retriever(search_type= 'similarity',search_kwargs={"k": 3}),
        # It specifies parameters like the prompt template, the response if no documents are found,
        # and returns both the answer and source documents.
        combine_docs_chain_kwargs={"prompt": prompt},
        response_if_no_docs_found = No_Doc,
        return_source_documents=True,
        chain_type='stuff'
    )
    return qa 

# CLASS DEFINITION
# cbfs is a class with a chat_history 
class cbfs(param.Parameterized):
    chat_history = param.List([])
    print("chat_history XXX")

# __init__ initializes the model using 'load_model'
    def __init__(self,  **params):
        super(cbfs, self).__init__( **params)
        self.qa = load_model()

# convchain is a method to process a query and update the chat history with the query and its reponse
    def convchain(self, query):
        result = self.qa({"question": query, "chat_history": self.chat_history})
        self.chat_history.extend([(query, result["answer"])])
        return result

# is a method to clear the chat history
    def clr_history(self):
        self.chat_history = []