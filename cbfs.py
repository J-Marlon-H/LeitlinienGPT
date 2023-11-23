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

embedding = OpenAIEmbeddings()


elastic_vector_search = ElasticsearchStore(
    es_cloud_id="LeitlinienGPT:ZXUtY2VudHJhbC0xLmF3cy5jbG91ZC5lcy5pbzo0NDMkYjQ2M2U4MmFhMTU3NDk0MWE2YTZlMjkxNzRmY2FjYjYkNzJlMDU1NzEyZjM5NDU3NTgxNTUyZDFlODFiMDE0YmY=",
    index_name="leitliniengpt",
    embedding=embedding,
    es_user="enterprise_search",
    es_password="-VwsG8mt-TELfRQ",
    # strategy=ElasticsearchStore.ApproxRetrievalStrategy(
    #     hybrid=True,
    # )
)

No_Doc = "Die hinterlegten Leitlinien Dokumente enthalten keine Informationen zu Ihrer Frage."

template = """Beantworten Sie die Frage am Ende des Textes anhand der folgenden Informationen. 
Geben Sie bei der Antwort so viele relevante Hintergrundinformationen mit wie Möglich.
Die Antwort sollte nicht länger als 8 Sätze sein.
Kontext:
{context}
Frage: {question}
Hilfreiche Antwort:"""
prompt = PromptTemplate.from_template(template)

def load_model():
    qa = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(temperature=0, model="gpt-4-1106-preview"), # gpt-3.5-turbo
        retriever=elastic_vector_search.as_retriever(search_kwargs={"k": 3}),
        combine_docs_chain_kwargs={"prompt": prompt},
        response_if_no_docs_found = No_Doc,
        return_source_documents=True,
        chain_type='stuff'
    )
    return qa 


class cbfs(param.Parameterized):
    chat_history = param.List([])
    print("chat_history XXX")

    def __init__(self,  **params):
        super(cbfs, self).__init__( **params)
        self.qa = load_model()
    
    def convchain(self, query):
        result = self.qa({"question": query, "chat_history": self.chat_history})
        self.chat_history.extend([(query, result["answer"])])
        return result

    def clr_history(self):
        self.chat_history = []