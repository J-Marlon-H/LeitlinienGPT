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
_es_cloud_id = os.environ['es_cloud_id']
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

# No_Doc = "Die hinterlegten Leitlinien Dokumente enthalten keine Informationen zu Ihrer Frage."
# If the context is not sufficient, say "In den Leitlinien stehen keine Informationen zu Ihrer Frage".
# If there is no information in the context relating to the question then say say that you did not find relevant information in the Leitlinien.

template = """
Only answer based on the context provided below. 
Provide all relevant details from the context provided below.
The answer should not exceed six sentences.
Memorize the language I ask you in my question.
context: {context}
question: {question}
Answer in the same language which I requested you to memorize. 
:"""
prompt = PromptTemplate.from_template(template)

def Init_model():
    qa = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(temperature=0, model="gpt-4-1106-preview"), # gpt-3.5-turbo
        retriever=elastic_vector_search.as_retriever(search_kwargs={"k": 3}),
        combine_docs_chain_kwargs={"prompt": prompt},
        # response_if_no_docs_found = No_Doc,
        return_source_documents=True,
        chain_type='stuff'
    )
    return qa 


class cbfs(param.Parameterized):
    chat_history = param.List([])
    count = param.List([])

    def __init__(self,  **params):
        super(cbfs, self).__init__( **params)
        self.qa = Init_model()
    
    def load_model(self,Database):
        if Database == "Nur aktuell gültige Leitlinien":
            self.qa = ConversationalRetrievalChain.from_llm(
                        llm=ChatOpenAI(temperature=0, model="gpt-4-1106-preview"), # gpt-3.5-turbo
                        retriever=elastic_vector_search.as_retriever(search_kwargs={"k": 3,'filter': [{"term": {"metadata.Gültigkeit.keyword": "Gültig"}}]}),
                        combine_docs_chain_kwargs={"prompt": prompt},
                        response_if_no_docs_found = No_Doc,
                        return_source_documents=True,
                        chain_type='stuff'
                        )
            self.count.append(1)

        else:
            self.qa = Init_model()
    
    def convchain(self, query):
        result = self.qa({"question": query, "chat_history": self.chat_history})
        self.chat_history.extend([(query, result["answer"])])
        return result

    def clr_history(self):
        self.chat_history = []