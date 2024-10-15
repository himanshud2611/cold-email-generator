import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException

from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

class myChain:
    def __init__(self):
        self.llm = ChatGroq(temperature= 0.25, groq_api_key = GROQ_API_KEY, model="llama-3.2-1b-preview")

    def extract_jobs_postings(self, cleaned_JD_page):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from the career's page of a website.
            Your job is to extract the job postings and return them in JSON format containing the following keys: `role`, `experience`, `skills` and `description`. The skills sections shouldn't be in dictionary format but in list.
            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
        )
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"page_data": cleaned_JD_page})
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("JD context too big. Unable to parse jobs.")
        return res if isinstance(res, list) else [res]


    
    def create_email(self, job, links):
        prompt_email = PromptTemplate.from_template(
        """
        ### JOB DESCRIPTION:
        {job_description}

        ### INSTRUCTION:
        You are [Candidate Name], a skilled professional seeking opportunities in [Industry/Field]. Your expertise includes [List of Relevant Skills/Technologies].
        You have a strong passion for [relevant interests related to the job or industry], and you are eager to contribute to innovative projects.

        Your job is to write a cold email to the hiring manager or recruiter at the company regarding the job mentioned above.
        Highlight your qualifications and explain how your skills align with the company's needs.
        Also add the most relevant ones from the following links to showcase your relevant projects. There should be project link with description for atmost 4 skills required by company: {link_list}
        Make sure to convey your enthusiasm for the opportunity and express your interest in discussing how you can add value to their team.

        ### EMAIL (NO PREAMBLE):
        """
        )
        chain_email = prompt_email | self.llm
        res = chain_email.invoke({"job_description": str(job), "link_list": links})
        return res.content

if __name__ == "__main__":
    print(os.getenv("GROQ_API_KEY"))