import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from mychain import myChain
from myportfolio import myPortfolio
from utils import cleaned_JD_page


def create_streamlit_app(llm, portfolio, cleaned_JD_page):
    st.title("🖋️ cold-email-crafter")
    url_input = st.text_input("Enter the JD Page URL: ", value = "")
    submit_button = st.button("Generate Email")

    if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            data = cleaned_JD_page(loader.load().pop().page_content)
            portfolio.load_portfolio()
            jobs = llm.extract_jobs_postings(data)
            for job in jobs:
                skills = job.get('skills', [])
                links = portfolio.query_links(skills)
                email = llm.create_email(job, links)
                st.code(email, language='markdown')
        except Exception as e:
            st.error(f"An Error Occurred: {e}")
           
if __name__ == "__main__":
    chain = myChain()
    portfolio = myPortfolio()
    st.set_page_config(layout="wide", page_title="cold-email-crafter", page_icon="🖋️")
    create_streamlit_app(chain, portfolio, cleaned_JD_page)