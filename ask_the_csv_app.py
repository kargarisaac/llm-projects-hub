from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

import os

import streamlit as st
import pandas as pd
from langchain.chat_models import ChatOpenAI
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain.agents.agent_types import AgentType

# Page title
st.set_page_config(page_title="🦜🔗 Ask the Data App")
st.title("🦜🔗 Ask the Data App")

openai_api_key = os.getenv("OPENAI_API_KEY")


# Load CSV file
def load_csv(input_csv):
    df = pd.read_csv(input_csv)
    with st.expander("See DataFrame"):
        st.write(df)
    return df


# Generate LLM response
def generate_response(csv_file, input_query):
    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo-0613", temperature=0.2, openai_api_key=openai_api_key
    )
    df = load_csv(csv_file)
    # Create Pandas DataFrame Agent
    agent = create_pandas_dataframe_agent(
        llm, df, verbose=True, agent_type=AgentType.OPENAI_FUNCTIONS
    )
    # Perform Query using the Agent
    response = agent.run(input_query)
    return st.success(response)


if __name__ == "__main__":
    # Input widgets
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    question_list = [
        "How many rows are there?",
        "What are the column names in the csv?",
        "Other",
    ]
    query_text = st.selectbox(
        "Select an example query:", question_list, disabled=not uploaded_file
    )

    # App logic
    if query_text is "Other":
        query_text = st.text_input(
            "Enter your query:",
            placeholder="Enter query here ...",
            disabled=not uploaded_file,
        )
    if uploaded_file is not None:
        st.header("Output")
        res = generate_response(uploaded_file, query_text)
        st.info(res)
