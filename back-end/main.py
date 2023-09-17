from fastapi import FastAPI
from mangum import Mangum
from pydantic import BaseModel, Field
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import CommaSeparatedListOutputParser, ResponseSchema, StructuredOutputParser
from fastapi.middleware.cors import CORSMiddleware

llm = OpenAI(openai_api_key="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", max_tokens=4000)
chat_model = ChatOpenAI(openai_api_key="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")
output_parser = CommaSeparatedListOutputParser()
format_instructions = output_parser.get_format_instructions()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class Email(BaseModel):
    name: str

class Industry(BaseModel):
    industry: str

@app.post("/competitors/")
async def competitors(data: Industry):
    companies = get_competitors(data)
    research = research_competitors(competitors=companies)
    return {"message": research}

@app.post("/email")
async def email(data: Email):
    email = generate_email(data)
    return {"message": email}

def generate_email(data):
    # Generates email sequences using one prompt for speed
    prompt = PromptTemplate(
        template = "Write up a personalized email outreach towards someone named {name}, prepare a few email sequences following this.\n{format_instructions}",
        input_variables=["name"],
        partial_variables={"format_instructions": format_instructions}
    )
    input = prompt.format(name=data.name)
    return llm(input)

def get_competitors(data):
    # Prompts largest competitors in specified industry
    # Creating a SequentialChain would have a faster response, however I could not figure out how to format the data to my needs
    # Formats companies into a List
    prompt = PromptTemplate(
        template = "List five of the largest companies within the {industry} industry.\n{format_instructions}",
        input_variables=["industry"],
        partial_variables={"format_instructions": format_instructions}
    )
    input = prompt.format(industry=data.industry)
    output = llm(input)
    return output_parser.parse(output)

def research_competitors(competitors):
    research = []
    # This function takes the List created from the previous prompt to append the research data properly into another List
    # This allows me to format the data to my liking to easily propagate the data on the front-end application
    # For this reason, I did not use a SequentialChain
    for company in competitors:
        prompt = PromptTemplate(
            template = "You are a market analyst that conducts complex competitive research. Conduct extensive research on your competitor {company}, gathering key competitive intelligence data. \n{format_instructions}",
            input_variables=["company"],
            partial_variables={"format_instructions": format_instructions}
        )
        input = prompt.format(company=company)
        output = llm(input)
        # output = output.replace("\n", " ")
        research.append({"company": company, "research": output})
    
    return research

handler = Mangum(app)