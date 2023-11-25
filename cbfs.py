from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.elasticsearch import ElasticsearchStore
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationalRetrievalChain
import param
from dotenv import load_dotenv
import os
import openai

dotenv_path = 'KEYs.env'  
_ = load_dotenv(dotenv_path)

openai.api_key = os.environ['OPENAI_API_KEY']
# _es_cloud_id = os.environ['OPENAI_API_KEY']
_es_cloud_id = os.environ['es_cloud_id']
# _es_user = os.environ['OPENAI_API_KEY']
# _es_password = os.environ['OPENAI_API_KEY']
_es_user = os.environ['es_user']
_es_password = os.environ['es_password']


embedding = OpenAIEmbeddings()


elastic_vector_search = ElasticsearchStore(
    es_cloud_id=_es_cloud_id,
    index_name="leitliniengpt",
    embedding=embedding,
    es_user=_es_user,
    es_password=_es_password,
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
        llm=ChatOpenAI(temperature=0, model="gpt-4-1106-preview"), # gpt-3.5-turbo
        # vectordb as a retriever
        retriever=elastic_vector_search.as_retriever(search_kwargs={"k": 3}),
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