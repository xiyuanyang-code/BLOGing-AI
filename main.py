'''
Author: Xiyuan Yang   xiyuan_yang@outlook.com
Date: 2025-03-29 15:17:02
LastEditors: Xiyuan Yang   xiyuan_yang@outlook.com
LastEditTime: 2025-03-29 16:26:27
FilePath: /RAG_try/RAG/main.py
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



# getting environments done
dotenv.load_dotenv()
openai.api_key = os.getenv("API_KEY")
openai.base_url = os.getenv("BASE_URL")

# langchain api
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_ENDPOINT'] = 'https://api.smith.langchain.com'
os.environ['LANGCHAIN_API_KEY'] = os.getenv("Langchain_api")

# Define LLMs and prompts
LLM = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0,
                    api_key = openai.api_key,
                    base_url = openai.base_url)

prompt = hub.pull("rlm/rag-prompt")

# load documents:
def loader_documents(url):
    loader = WebBaseLoader(
    web_paths=(url,),

    )
    docs = loader.load()
    return docs



def text_splitter(docs):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)

    return splits

def embedding(splits):
    '''Embeding the vector'''
    vectorstore = Chroma.from_documents(documents=splits, 
                                        embedding=OpenAIEmbeddings(
                                            base_url="https://api.zhizengzeng.com/v1",
                                            api_key=os.environ["OPENAI_API_KEY"]
                                        ))

    retriever = vectorstore.as_retriever()

    return vectorstore, retriever

# Post-processing
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def get_answer(retriever, prompt, llm, question):
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    answer = rag_chain.invoke(question)

    return answer 

def getstreamlit_UI(prompt, LLM):
    
    st.title("RAG-Based Blog System")
    st.subheader("Author: Xiyuan Yang (xiyuanyang-code)")
    st.session_state["Prompt"] = prompt
    st.session_state["LLM"] = LLM

    # Introduction Part
    st.write("## About this website")
    st.write("This website is my **RAG implementation** for searching and retrieving my own blog posts, you can see my own blog posts\
                and choose the blog url down here!")
    st.write("My Blog posts: [xiyuanyang-code](https://xiyuanyang-code.github.io)")

    # Choose website
    st.write("default url: https://xiyuanyang-code.github.io/posts/Algorithm-BinaryTree/")
    st.write("**Make sure your url is valid!**")
    url = st.text_input("Choose your website: ")




    default_url = "https://xiyuanyang-code.github.io/posts/Algorithm-BinaryTree/"
    if st.button("Scrape Blog Content"):
        with st.spinner("Scraping blog content..."):
            blog_content = loader_documents(url)
            if blog_content:
                st.success("Blog content scraped successfully!")
                st.session_state["blog_content"] = blog_content
            else:
                st.error("Failed to scrape blog content.",icon="🚨")
                st.write("Using the default url")
                blog_content = loader_documents(default_url)


    if "blog_content" in st.session_state:
        blog_content = st.session_state["blog_content"]
        if st.button("Process and Store Content"):
            with st.spinner("Processing and storing content..."):
                splits = text_splitter(blog_content)
                vectorstore, retriever = embedding(splits)
                st.session_state["vectorstore"] = vectorstore
                st.session_state["retriever"] = retriever
                st.success("Content processed and stored in Chroma!")


    if "vectorstore" in st.session_state:
        vectorstore = st.session_state["vectorstore"]
        retriever = st.session_state["retriever"]
        prompt = st.session_state["Prompt"]
        LLM = st.session_state["LLM"]

        query = st.text_input("Ask a question about the blog:")
        if query:
            with st.spinner("Generating answer..."):
                answer = get_answer(retriever=retriever, prompt=prompt, llm=LLM, question=query)
                st.write("**Answer:**")
                st.write(answer)
    
if __name__ == "__main__":
    getstreamlit_UI(prompt=prompt, LLM=LLM)