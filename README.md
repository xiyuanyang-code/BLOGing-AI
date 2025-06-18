# RAG blog content retrieval

> [!IMPORTANT] To be refactored!!!

## 😊Introduction

This is a simple application for blog content retrieval implemented using RAG as the core technology.

## 🚀Installation

### Requirements

- Make sure you have **OpenAI API Key** and **LangSmith** API key!

#### Install Python requirements

After cloning the project, run:

```bash
pip install -r requirements.txt
```

#### Set up `.env` file

Set up a file named `.env` in your current directory:

```bash
touch .env
```

Fill in your keys and other information in the `.env` file, a demo is shown below:

```
API_KEY=123456
BASE_URL=123456
Langchain_api=123456
```

**Remember to replace your api key value into the key value**!

## 💓Usage

**Make sure you have passed through the `installation` section successfully.** 

### Run `Streamlit` code Locally

run following commands:

```bash
streamlit run ./main.py
```

Then you can see the webpages like this:

![demo](https://s1.imagehub.cc/images/2025/03/29/e78604608a8deae5a20b687fd9f65689.png)

Then you can run this locally in your computer, enjoy RAG now!

A demo:

![demo2](https://s1.imagehub.cc/images/2025/03/29/b736eb5e2afe5029a2c2f1b4011605ca.png)

You can freely search send queries regarding the blog passage and get answers.

### Run `Streamlit` demo online

I will finish it later...

But actually I don't recommend this for it is unsafe to input your secret key to the internet!

## 🤖Discussion

Just for fun, don't be serious.

If you have any issues, don't hesitate to contact the author.

## 👍Advertisement

My personal Blog: [Xiyuan Yang's Blog](https://xiyuanyang-code.github.io/)