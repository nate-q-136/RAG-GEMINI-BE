from abc import ABC, abstractmethod
from langchain.document_loaders import CSVLoader, PyPDFLoader, Docx2txtLoader
from utils.gemini_agent.config_v2 import gemini
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain.docstore.in_memory import InMemoryDocstore
from langchain.schema.runnable import RunnableSequence
from utils.urls import UrlHandler
import os

import faiss




class BaseGemini(ABC):
    @abstractmethod
    def generate_answer(self, *args, **kwargs):
        pass

class GeminiLLMChain(BaseGemini):
    def __init__(self):
        self.gemini = gemini
        self.prompt_template = PromptTemplate(
            template="You are an expert QA system. Answer the question based on your knowledge.\nQuestion: {question}\nAnswer:",
            input_variables=["question"]
        )

        self.qa_chain = RunnableSequence(self.prompt_template | self.gemini)

    def generate_answer(self, query):
        response = self.qa_chain.invoke({"question": query})
        return response.content

class GeminiRetrievalQA(BaseGemini):
    def __init__(self):
        self.gemini = gemini
        self.embedding_model = HuggingFaceEmbeddings(model_name='sentence-transformers/paraphrase-MiniLM-L6-v2')

        self.prompt_template = PromptTemplate(
            template="You are an expert QA system. Use the context below to answer the question.\nContext: {context}\nQuestion: {question}\nAnswer:",
            input_variables=["context", "question"]
        )

    def _create_user_vector_store(self):
        dimension = 384
        index = faiss.IndexFlatL2(dimension)

        docstore = InMemoryDocstore()
        index_to_docstore_id = {}

        user_vector_store = FAISS(
            index=index,
            docstore=docstore,
            index_to_docstore_id=index_to_docstore_id,
            embedding_function=self.embedding_model
        )

        return user_vector_store
    
    def generate_answer(self, query, attachments=None, user_dir=None):
        vector_store = self._create_user_vector_store()
        if os.path.exists(user_dir):
            vector_store = FAISS.load_local(user_dir, self.embedding_model, allow_dangerous_deserialization=True)
        else:
            vector_store.save_local(user_dir)
        handled_attachments = []
        if attachments:
            loader = None
            for attachment in attachments:
                file_name = attachment.get("file_name")
                handled_attachments.append(file_name)
                url = attachment.get("url")
                file_path = UrlHandler.download_file(url, file_name)

                if file_name.endswith(".csv"):
                    loader = CSVLoader(file_path=file_path)
                elif file_name.endswith(".pdf"):
                    loader = PyPDFLoader(file_path=file_path)
                elif file_name.endswith(".docx"):
                    loader = Docx2txtLoader(file_path=file_path)
                
                # Add to FAISS vector store
                if loader:
                    data = loader.load()
                    vector_store.add_documents(data)
                    vector_store.save_local(user_dir)
                    os.remove(file_path)

        qa_chain = RetrievalQA.from_chain_type(
            llm=self.gemini,
            chain_type="stuff",
            retriever=vector_store.as_retriever(),
            chain_type_kwargs={"prompt": self.prompt_template}
        )
        response = qa_chain.run(query)
        return response, handled_attachments
