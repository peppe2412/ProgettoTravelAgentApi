from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel , Field
from typing import Optional

class TravelPlanInput(BaseModel):
    start_date: str = Field(description="The start date of the trip YYYY-MM-DD e.g. 2025-09-30")
    end_date: str = Field(description="The end date of the trip YYYY-MM-DD e.g. 2025-10-07")
    destination: str = Field(description="The destination of the trip")
    adults: Optional[int] = Field(1, description="The numbers of the adults. Default to 1")
    childrens: Optional[int] = Field(0, description="The numbers of the childrens. Default to 0")
    travel_style: str = Field(description="The style of travel. e.g. adventure, relax, culture, backpacking, luxury, family-friendly.")
    budget: Optional[int] = Field(description="The budget for the trip")
    activities: str = Field(description="The preferred activities. e.g. culture, nature, food, shopping")
    food_restriction: str = Field(description="Any food restrictions. e.g. vegetarian, gluten-free")
    
class TravelPlanSchema(BaseModel):
    params : TravelPlanInput
    
class TravelDayOutput(BaseModel):
    morning: str = Field(description="The activities for the morning.")
    afternoon: str = Field(description="The activities for the afternoon.")
    evening: str = Field(description="The activities for the evening.")
    
class TravelPlanOutput(BaseModel):
    travel_plan: list[TravelDayOutput]

@tool(args_schema=TravelPlanSchema)
def chain_travel_plan(params:TravelPlanInput) -> TravelPlanOutput:
    """
    Generates a comprehensive travel plan based on user input parameters.
    Parameters:
    params (TravelPlanInput): The input parameters for the travel plan
    including dates, destination, number of travelers, travel style, budget,
    preferred activities, and any food restrictions.
    Returns:
    TravelPlanOutput: The generated travel plan content.
    """
    model = ChatOpenAI(model_name="gpt-4o")
    
    system_prompt = f"""
    You are a travel expert.
    Your mission is to provide in-depth content on the topic to create a travel plan.
    The start date of the trip is {params.start_date}.
    The end date of the trip is {params.end_date}.
    The destination of the trip is {params.destination}.
    The number of adults is {params.adults}.
    The number of children is {params.childrens}.
    The style of travel is {params.travel_style}.
    The total budget for the trip is {params.budget}.
    The preferred activities are {params.activities}.
    Any food restrictions are {params.food_restriction}
    Use emojis to make your answers more engaging and friendly.
    Always strive to be approachable and helpful, offering the
    most accurate and useful information possible to users.
    """
    prompt = ChatPromptTemplate([("human", "{input}")])
    output_parser = PydanticOutputParser(pydantic_object=TravelPlanOutput)
    chain = prompt | model | output_parser
    result = chain.invoke(input=system_prompt)
    
    # print("*" * 80)
    # print("chain_travel_plan")
    # print("*" * 80)
    return result

