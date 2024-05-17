from dotenv import load_dotenv
import os
from langchain_community.llms import HuggingFaceEndpoint
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_community.embeddings import HuggingFaceHubEmbeddings
import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile

# Load environment variables from .env file
load_dotenv()

# Set the Hugging Face API token from the environment variables
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

st.title("🦜🔗 Ask The Doc App")


def generate_response(uploaded_file: UploadedFile, query_text: str) -> str:
    """
    Generates a response to a query using the uploaded document and the query text.

    Args:
        - uploaded_file: The uploaded document.
        - query_text: The query text.

    Returns:
        - The response to the query.
    """
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
    return "No file uploaded."


def main():
    """
    Main function to run the Streamlit UI.
    """
    # File upload
    uploaded_file = st.file_uploader("Upload an article in txt format", type="txt")

    # Query text input
    query_text = st.text_input(
        "Enter your question:",
        placeholder="Please provide a short summary.",
        disabled=not uploaded_file,
    )

    # Form for input and query submission
    result = []
    with st.form("myform", clear_on_submit=True):
        submitted = st.form_submit_button(
            "Submit", disabled=not (uploaded_file and query_text)
        )
        if submitted:
            with st.spinner("Calculating..."):
                response = generate_response(uploaded_file, query_text)
                result.append(response)

    # Display result
    if len(result):
        st.info(result[0])


if __name__ == "__main__":
    main()
