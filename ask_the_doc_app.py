from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

import os

from langchain_community.llms import HuggingFaceEndpoint
from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_community.embeddings import HuggingFaceHubEmbeddings

import streamlit as st


st.title("🦜🔗 Ask The Doc App")

HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")


def generate_response(uploaded_file, query_text):
    # Load document if file is uploaded
    if uploaded_file is not None:
        documents = [uploaded_file.read().decode()]
        # Split documents into chunks
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        texts = text_splitter.create_documents(documents)
        # Select embeddings
        embeddings = HuggingFaceHubEmbeddings(
            model="sentence-transformers/all-mpnet-base-v2",
            task="feature-extraction",
            huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN,
        )
        # Create a vectorstore from documents
        db = Chroma.from_documents(texts, embeddings)
        # Create retriever interface
        retriever = db.as_retriever()
        # Create QA chain
        llm = HuggingFaceEndpoint(
            repo_id="mistralai/Mistral-7B-Instruct-v0.2",
            max_length=128,
            temperature=0.5,
            token=HUGGINGFACEHUB_API_TOKEN,
        )
        qa = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
        )
        return qa.run(query_text)


if __name__ == "__main__":
    # File upload
    uploaded_file = st.file_uploader("Upload an article", type="txt")
    # Query text
    query_text = st.text_input(
        "Enter your question:",
        placeholder="Please provide a short summary.",
        disabled=not uploaded_file,
    )

    # Form input and query
    result = []
    with st.form("myform", clear_on_submit=True):
        submitted = st.form_submit_button(
            "Submit", disabled=not (uploaded_file and query_text)
        )
        if submitted:
            with st.spinner("Calculating..."):
                response = generate_response(uploaded_file, query_text)
                result.append(response)

    if len(result):
        st.info(response)
