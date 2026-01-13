import os
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_community.llms import HuggingFacePipeline
from transformers import pipeline
from langchain.prompts import PromptTemplate

class RAGEngine:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.vector_store = None
        self.qa_chain = None

    def load_documents(self):
        documents = []
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            
        for filename in os.listdir(self.data_dir):
            if filename.endswith(".txt"):
                file_path = os.path.join(self.data_dir, filename)
                loader = TextLoader(file_path, encoding='utf-8')
                documents.extend(loader.load())
        return documents

    def create_vector_store(self):
        print("Loading documents...")
        docs = self.load_documents()
        if not docs:
            return None

        print("Splitting documents...")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
        chunks = text_splitter.split_documents(docs)

        print("Creating embeddings...")
        item_embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        
        print("Building FAISS index...")
        self.vector_store = FAISS.from_documents(chunks, item_embeddings)
        return self.vector_store

    def get_qa_chain(self):
        if self.qa_chain:
            return self.qa_chain

        if not self.vector_store:
            self.create_vector_store()
            
        # Setup LLM - using flan-t5-small for lightweight CPU usage
        # You can change to 'google/flan-t5-base' for better quality if resources allow
        pipe = pipeline(
            "text2text-generation", 
            model="google/flan-t5-small", 
            max_length=512
        )
        llm = HuggingFacePipeline(pipeline=pipe)

        # Custom prompt to enforce strict verification
        prompt_template = """Use the following pieces of context to answer the question at the end. 
If the context does not contain enough information to verify the claim, say "Unverified". 
Do not guess.
If the claim is supported by the context, classify it as "Safe".
If the claim contradicts the context, classify it as "Unsafe".
Provide a brief explanation after the classification.

Context:
{context}

Question: {question}

Answer:"""
        
        PROMPT = PromptTemplate(
            template=prompt_template, 
            input_variables=["context", "question"]
        )

        retriever = self.vector_store.as_retriever(search_kwargs={"k": 3})
        
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            chain_type_kwargs={"prompt": PROMPT}
        )
        
        return self.qa_chain

# Singleton instance to be used by the app
rag_engine = RAGEngine()
