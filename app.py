import streamlit as st
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.chat_models import ChatOpenAI
from langchain_community.utilities import SQLDatabase
import os

# Set the OpenAI API key
OPENAI_API_KEY = "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"
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

# Streamlit UI
st.title("Database Query Chatbot")
st.write("Ask a question about the database, and the chatbot will generate an SQL query to answer it.")

# User input
user_input = st.text_input("Your question:")

# Process input when the user submits a query
if st.button("Submit"):
    if user_input:
        with st.spinner('Processing...'):
            try:
                # Setting up the SQL Database Connection
                db = SQLDatabase.from_uri("postgresql://sqluser:s$6vGw^MQfN9@rg-pgsql-sandbox-cae.postgres.database.azure.com:5432/mk-multi-table")

                # Configuring the OpenAI Language Model
                model = ChatOpenAI(
                    temperature=0,
                    max_tokens=512,
                    openai_api_key=os.getenv("OPENAI_API_KEY")
                )

                # Creating SQL Database Toolkit
                toolkit = SQLDatabaseToolkit(db=db, llm=model)

                # Creating the SQL Agent
                agent_executor = create_sql_agent(
                    llm=model,
                    toolkit=toolkit,
                    verbose=True,
                    handle_parsing_errors=True
                )

                # Get the response
                response = agent_executor.invoke({"input": user_input})

                # Display the response
                st.success("Response:")
                st.write(response)

            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a question.")

