from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

import os
import tempfile

from langchain_community.llms import HuggingFaceEndpoint
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_community.embeddings import HuggingFaceHubEmbeddings
from langchain.chains.summarize import load_summarize_chain
from langchain.document_loaders import PyPDFLoader

import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile

st.title("🦜🔗 Chat With The Paper.")

HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")


def summarize_pdf(uploaded_file: UploadedFile, llm: HuggingFaceEndpoint) -> str:
    """
    This function generates a summary of the uploaded PDF file.

    It first loads the PDF file and splits it into documents. Then, it creates a summarization chain and runs it on the documents.

    Args:
        - uploaded_file: The uploaded PDF file.

    Returns:
        - The summary of the PDF file.
    """
    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name

    loader = PyPDFLoader(tmp_file_path)
    docs = loader.load_and_split()
    chain = load_summarize_chain(llm, chain_type="map_reduce")
    summary = chain.run(docs)
    return summary


def chat_with_pdf(
    uploaded_file: UploadedFile,
    query_text: str,
    llm: HuggingFaceEndpoint,
) -> str:
    """
    This function generates a response to a query using the uploaded PDF file and the query text.

    It first loads the PDF file and creates a vectorstore from the documents. Then, it creates a retriever interface and a QA chain. Finally, it runs the QA chain on the query text.

    Args:
        - uploaded_file: The uploaded PDF file.
        - query_text: The query text.

    Returns:
        - The response to the query.
    """
    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name

        # Load the pdf
        loader = PyPDFLoader(file_path=tmp_file_path)
        data = loader.load()

        # Select embeddings
        embeddings = HuggingFaceHubEmbeddings(
            model="sentence-transformers/all-mpnet-base-v2",
            task="feature-extraction",
            huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN,
        )

        # Create a vectorstore from documents
        db = Chroma.from_documents(data, embeddings)

        # Create retriever interface
        retriever = db.as_retriever()

        # Create QA chain
        qa = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
        )
        return qa.run(query_text)


if __name__ == "__main__":
    # File upload
    uploaded_file = st.file_uploader("Upload a .pdf file.", type="pdf")

    llm = HuggingFaceEndpoint(
        repo_id="mistralai/Mistral-7B-Instruct-v0.2",
        max_length=128,
        temperature=0.5,
        token=HUGGINGFACEHUB_API_TOKEN,
    )

    # Form input and query
    with st.form("summary_form", clear_on_submit=True):
        submitted = st.form_submit_button("Summarize ...", disabled=not (uploaded_file))
        if submitted:
            with st.spinner("Calculating..."):
                response = summarize_pdf(uploaded_file, llm)
                st.info(response)

    # Query text
    query_text = st.text_input(
        "Enter your question:",
        placeholder="What is the core idea of the paper?",
        disabled=not uploaded_file,
    )

    # Form input and query
    result = []
    with st.form("chat_form", clear_on_submit=True):
        submitted = st.form_submit_button(
            "Ask PDF ...", disabled=not (uploaded_file and query_text)
        )
        if submitted:
            with st.spinner("Calculating..."):
                response = chat_with_pdf(uploaded_file, query_text, llm)
                result.append(response)

    if len(result):
        st.info(response)
