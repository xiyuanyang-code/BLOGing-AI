'''
Author: Xiyuan Yang   xiyuan_yang@outlook.com
Date: 2025-03-29 15:17:02
LastEditors: Xiyuan Yang   xiyuan_yang@outlook.com
LastEditTime: 2025-03-30 11:44:39
FilePath: /RAG/main.py
Description: 
Do you code and make progress today?
Copyright (c) 2025 by Xiyuan Yang, All Rights Reserved. 
'''

# Several Requirements
import bs4
import dotenv
import openai
import os
import streamlit as st
from langchain import hub
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings


# Helper Functions
def load_env_variables():
    """Load environment variables from .env file.
    only be used when the file is running locally
    """
    if os.path.exists(".env"):
        dotenv.load_dotenv()
        st.success("Environment variables loaded successfully!")
    else:
        st.error("No .env file found. Please ensure you're in offline mode or create a .env file.", icon="🚨")


def get_api_key(mode):
    """Get API key based on the selected mode.
    return three varialble: OPENAI API KEY, OPENAI BASE URL and LangSmith API KEY
    """

    # For offline mode (read the openai key from the .env file)
    if mode == "Offline":
        api_key = os.getenv("OPENAI_API_KEY")
        base_url = os.getenv("BASE_URL")
        langsmith_api_key = os.getenv("Langchain_api")
        if not api_key or not base_url:
            st.error("Missing API_KEY or BASE_URL in .env file for offline mode.", icon="🚨")
            return None, None
        return api_key, base_url, langsmith_api_key
    
    # Online mode, let the user to input the API key and base_url
    elif mode == "Online":
        api_key = st.text_input("Enter your OpenAI API Key:", type="password")
        base_url = st.text_input("Enter your OpenAI Base URL:")
        langsmith_api_key = st.text_input("Enter your Langsmith API Key", type="password")
        if not api_key or not base_url or not langsmith_api_key:
            st.error("API Key and Base URL are required for online mode.", icon="🚨")
            return None, None, None
        return api_key, base_url, langsmith_api_key


def initialize_llm(api_key, base_url):
    """Initialize the LLM with the given API key and base URL."""
    try:
        llm = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            temperature=0,
            api_key=api_key,
            base_url=base_url
        )
        st.success("LLM initialized successfully!")
        return llm
    except Exception as e:
        st.error(f"Failed to initialize LLM: {e}", icon="🚨")
        return None


def loader_documents(url):
    """Load documents from the given URL."""
    try:
        loader = WebBaseLoader(web_paths=(url,))
        docs = loader.load()
        st.success("Documents loaded successfully!")
        return docs
    except Exception as e:
        st.error(f"Failed to load documents: {e}", icon="🚨")
        return None


def text_splitter(docs):
    """Split documents into smaller chunks."""
    try:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(docs)
        st.success("Documents split successfully!")
        return splits
    except Exception as e:
        st.error(f"Failed to split documents: {e}", icon="🚨")
        return None


def embedding(splits, api_key):
    """Embed documents into a vector store."""
    try:
        vectorstore = Chroma.from_documents(
            documents=splits,
            embedding=OpenAIEmbeddings(
                base_url="https://api.zhizengzeng.com/v1",
                api_key=api_key
            )
        )
        retriever = vectorstore.as_retriever()
        st.success("Documents embedded successfully!")
        return vectorstore, retriever
    except Exception as e:
        st.error(f"Failed to embed documents: {e}", icon="🚨")
        return None, None


def format_docs(docs):
    """Format documents for display."""
    return "\n\n".join(doc.page_content for doc in docs)


def get_answer(retriever, prompt, llm, question):
    """Generate an answer using the RAG chain."""
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    answer = rag_chain.invoke(question)
    return answer


def getstreamlit_UI(prompt):
    """Streamlit UI for the RAG application."""
    st.title("RAG-Based Blog System")
    st.subheader("Author: Xiyuan Yang (xiyuanyang-code)")

    # Mode Selection
    mode = st.selectbox("Select Mode", ["Offline", "Online"])
    st.session_state["mode"] = mode

    if mode == "Offline":
        load_env_variables()
        api_key, base_url, langchainAPI = get_api_key(mode)
    else:
        api_key, base_url, langchainAPI = get_api_key(mode)

    if not api_key or not base_url or not langchainAPI:
        st.stop()

    # load langhchain API
    os.environ['LANGCHAIN_TRACING_V2'] = 'true'
    os.environ['LANGCHAIN_ENDPOINT'] = 'https://api.smith.langchain.com'
    os.environ['LANGCHAIN_API_KEY'] = langchainAPI

    # Initialize LLM
    llm = initialize_llm(api_key, base_url)
    if not llm:
        st.stop()

    # Introduction Part
    st.write("## About this website")
    st.write("This website is my **RAG implementation** for searching and retrieving my own blog posts.")
    st.write("My Blog posts: [xiyuanyang-code](https://xiyuanyang-code.github.io)")

    # Choose Website
    default_url = "https://xiyuanyang-code.github.io/posts/Algorithm-BinaryTree/"
    url = st.text_input("Choose your website:", value=default_url)
    st.write("**Make sure your URL is valid!**")

    if st.button("Scrape Blog Content"):
        with st.spinner("Scraping blog content..."):
            blog_content = loader_documents(url)
            if not blog_content:
                st.error("Failed to scrape blog content. Using the default URL.", icon="🚨")
                blog_content = loader_documents(default_url)
            st.session_state["blog_content"] = blog_content

    if "blog_content" in st.session_state:
        blog_content = st.session_state["blog_content"]

        if st.button("Process and Store Content"):
            with st.spinner("Processing and storing content..."):
                splits = text_splitter(blog_content)
                if splits:
                    vectorstore, retriever = embedding(splits, api_key)
                    st.session_state["vectorstore"] = vectorstore
                    st.session_state["retriever"] = retriever

    if "vectorstore" in st.session_state:
        retriever = st.session_state["retriever"]
        query = st.text_input("Ask a question about the blog:")
        if query:
            with st.spinner("Generating answer..."):
                answer = get_answer(retriever=retriever, prompt=prompt, llm=llm, question=query)
                st.write("**Answer:**")
                st.write(answer)


if __name__ == "__main__":
    prompt = hub.pull("rlm/rag-prompt")
    getstreamlit_UI(prompt=prompt)