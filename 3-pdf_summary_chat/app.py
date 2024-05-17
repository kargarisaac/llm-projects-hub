from dotenv import load_dotenv
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

# Load environment variables from .env file
load_dotenv()

# Set the Hugging Face API token from the environment variables
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

# Page title
st.title("🦜🔗 Chat With The Paper")


def summarize_pdf(uploaded_file: UploadedFile, llm: HuggingFaceEndpoint) -> str:
    """
    Generates a summary of the uploaded PDF file.

    Args:
        - uploaded_file: The uploaded PDF file.
        - llm: The language model to use for summarization.

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
    uploaded_file: UploadedFile, query_text: str, llm: HuggingFaceEndpoint
) -> str:
    """
    Generates a response to a query using the uploaded PDF file and the query text.

    Args:
        - uploaded_file: The uploaded PDF file.
        - query_text: The query text.
        - llm: The language model to use for the QA chain.

    Returns:
        - The response to the query.
    """
    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name

        # Load the PDF
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


def main():
    """
    Main function to run the Streamlit UI.
    """
    # File upload
    uploaded_file = st.file_uploader("Upload a .pdf file.", type="pdf")

    # Initialize the language model
    llm = HuggingFaceEndpoint(
        repo_id="mistralai/Mistral-7B-Instruct-v0.2",
        max_length=128,
        temperature=0.5,
        token=HUGGINGFACEHUB_API_TOKEN,
    )

    # Summarization form
    with st.form("summary_form", clear_on_submit=True):
        submitted = st.form_submit_button("Summarize ...", disabled=not uploaded_file)
        if submitted:
            with st.spinner("Calculating..."):
                response = summarize_pdf(uploaded_file, llm)
                st.info(response)

    # Query text input
    query_text = st.text_input(
        "Enter your question:",
        placeholder="What is the core idea of the paper?",
        disabled=not uploaded_file,
    )

    # QA form
    result = []
    with st.form("chat_form", clear_on_submit=True):
        submitted = st.form_submit_button(
            "Ask PDF ...", disabled=not (uploaded_file and query_text)
        )
        if submitted:
            with st.spinner("Calculating..."):
                response = chat_with_pdf(uploaded_file, query_text, llm)
                result.append(response)

    # Display result
    if result:
        st.info(result[0])


if __name__ == "__main__":
    main()
