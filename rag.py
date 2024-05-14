from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain.schema.output_parser import StrOutputParser
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema.runnable import RunnablePassthrough
from langchain.prompts import PromptTemplate
from langchain.vectorstores.utils import filter_complex_metadata
import os
from prompt import *

class ChatPDF:
	vector_store = None
	retriever = None
	chain = None

	def __init__(self):
			self.model = ChatOllama(model="mistral")
			self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=100)
			self.prompt = PromptTemplate.from_template(
				'''
				{context}
				# you are a teacher assistante answer precicely :
				{question}
				'''
			)

			
	def ingest(self, pdf_file_path: str):
		docs = PyPDFLoader(file_path=pdf_file_path).contentload()
		chunks = self.text_splitter.split_documents(docs)
		chunks = filter_complex_metadata(chunks)

		vector_store = Chroma.from_documents(documents=chunks, embedding=FastEmbedEmbeddings())
		self.retriever = vector_store.as_retriever(
				search_type="similarity_score_threshold",
				search_kwargs={
						"k": 3,
						"score_threshold": 0.5,
				},
		)

		self.chain = ({"context": self.retriever, "question": RunnablePassthrough()}
									| self.prompt
									| self.model
									| StrOutputParser())
	
	def ingests(self, pdf_paths: set[str],f_string=""):
		vector_store_chunks =  []
		i = 0
		# Iterate over each PDF file path
		for pdf_path in pdf_paths:
			try:
				docs = PyPDFLoader(file_path=pdf_path).load()
				chunks = self.text_splitter.split_documents(docs)
				chunks = filter_complex_metadata(chunks)
				if i == 0 :
					i+=1
					vector_store_chunks = chunks
				else :
					vector_store_chunks.extend(chunks)  # Add chunks from this PDF to the list
			except FileNotFoundError:
				print(f"Error: File not found: {pdf_path}")  # Handle file not found error

		# Create a single vector store from all processed chunks
		vector_store = Chroma.from_documents(documents=vector_store_chunks, embedding=FastEmbedEmbeddings())

		# Configure retrieval component as before using the combined vector store
		self.retriever = vector_store.as_retriever(
				search_type="similarity_score_threshold",
				search_kwargs={
						"k": 3,
						"score_threshold": 0.5,
				},
		)
		#use default prompt or use user prompt
		if f_string != "":
			self.prompt = PromptTemplate.from_template(f_string)
		# Rest of your chain definition remains the same
		self.chain = ({"context": self.retriever, "question": RunnablePassthrough()}|self.prompt|self.model| StrOutputParser())


	def ask(self, query: str):
			if not self.chain:
					return "Please, add a PDF document first."

			return self.chain.invoke(query)

	def clear(self):
			self.vector_store = None
			self.retriever = None
			self.chain = None
