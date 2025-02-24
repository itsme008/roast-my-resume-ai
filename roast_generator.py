import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.chains import LLMChain
from langchain_groq import ChatGroq

load_dotenv()

# Retrieve API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    max_completion_tokens=600,
    api_key=GROQ_API_KEY,
    temperature=0.4,
)

roast_prompt = PromptTemplate(
    input_variables=["resume_text"],
    template="""
    You are a roast master. Given a resume, your job is to brutally roast it while making it funny.
    Highlight unnecessary buzzwords, cliché phrases, and weak descriptions.
    
    Be sarcastic, witty, and brutally honest about the resume.
    
    Resume:
    {resume_text}
    
    Roast this resume in a funny way.
    Make sure to end the roast with a punchline or a final statement that sounds complete.
    Keep it within the limit:
    """
)

# 🎯 Second Prompt: Constructive Feedback
constructive_feedback_prompt = PromptTemplate(
    input_variables=["resume_text"],
    template="""
    You are a professional career advisor. Given a resume, provide **concise and actionable** feedback to improve it.
    Focus on **3-5 key points** about structure, word choice, and how to make it appealing to recruiters.

    Resume:
    {resume_text}

    🔹 Provide a short, structured response with **bullet points**.
    🔹 Prioritize the most **important** improvements.
    🔹 Ensure your response **ends properly** and doesn't get cut off.

    Keep it **concise** and **within the token limit**.
    """
)

summary_roast_prompt = PromptTemplate(
    input_variables=["roast_prompt"],
    template="""
    You are a savage roast master who excels at delivering short, witty, and brutal summaries.
    
    Given a detailed roast of a resume, your job is to **compress it into a single hilarious, punchy paragraph**.
    
    🔥 Keep it funny, ruthless, and brutally honest.
    ⚡ Maintain sarcasm and wit.
    🎯 Highlight key weaknesses but in **a savage, meme-worthy way**.
    
    Here's the full roast:
    {roast_prompt}

    Now, **summarize it into a short, punchy roast** (max 10 sentences):
    """
)


roast_chain = roast_prompt | llm | StrOutputParser()

constructive_feedback_chain = constructive_feedback_prompt | llm | StrOutputParser()

summary_roast_promt_chain = summary_roast_prompt | llm | StrOutputParser()



def generate_roast(resume_text):
    """Takes resume text as input and returns a brutally funny AI-generated roast."""
    roast_result = roast_chain.invoke({"resume_text": resume_text})
    feedback_result = constructive_feedback_chain.invoke({"resume_text": resume_text})
    summary_result = summary_roast_promt_chain.invoke({"roast_prompt": roast_result})

    return roast_result, feedback_result, summary_result