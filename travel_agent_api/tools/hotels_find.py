from dotenv import load_dotenv
from langchain_core.tools import tool
from serpapi import GoogleSearch
from pydantic import BaseModel , Field
from typing import Optional
from enum import IntEnum
import os

load_dotenv()

class HotelsEnum(IntEnum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    
class HotelsInput(BaseModel):
    q: str = Field(description="The location of the hotels")
    check_in_date: str = Field(description="The check in date YYYY-MM-DD e. g. 2025-09-30")
    check_out_date: str = Field(description="The check out date YYYY-MM-DD e. g. 2025-10-07")
    adults: Optional[int] = Field(1, description="The numbers of the adults. Default to 1")
    childrens: Optional[int] = Field(0, description="The numbers of the childrens. Default to 0")
    hotel_class: Optional[int] = Field(2, description="The class of the hotel avaible from 2 to 5. Default to 2")
    
class HotelSchema(BaseModel):
    params : HotelsInput
    
@tool(args_schema=HotelSchema)
def hotel_finder(params:HotelsInput):
    """
    This tool uses the SerpApi Google Hotels API to retrieve hotels info.
    Parameters:
    q (str): Location of the hotel.
    check_in_date (str): The check in date (YYYY-MM-DD) e.g. 2025-09-30.
    check_out_date (str): The check out date (YYYY-MM-DD) e.g. 2025-10-07.
    adults (int): The number of adults. Defaults to 1.
    children (int): The number of children. Defaults to 0.
    hotel_class (int): The hotel class available from 2 to 5. Defaults to 2.
    Returns:
    dict: A dictionary containing the hotels info. If the API call fails, it returns the
    error message as a string"""
    
    params = {
        "api_key" : os.getenv('SERPAPI_API_KEY'),
        "engine": "google_hotels",
        "q": params.q,
        "check_in_date": params.check_in_date,
        "check_out_date": params.check_out_date,
        "adults": params.adults,
        "childrens": params.childrens,
        "hotel_class": params.hotel_class,
        "num": 5,
        "currency": "EUR",
        "gl": "it",
        "hl": "it",
    }
    
    try:
        search = GoogleSearch(params)
        result = search.get_dict()["properties"]
    except Exception as e:
        print('Error:', e)
        result = (str(e))
    
    # print('*' * 80)
    # print('hotel_finder')
    # print('*' * 80)
    return search.get_dict()
