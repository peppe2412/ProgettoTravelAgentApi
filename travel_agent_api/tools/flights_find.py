from dotenv import load_dotenv
from langchain_core.tools import tool
from serpapi import GoogleSearch
from pydantic import BaseModel , Field
from typing import Optional
import os

load_dotenv()

class FlightsInput(BaseModel):
    departure: str = Field(description="The departure airport code (IATA)")
    arrival: str = Field(description="The arrival airport code (IATA)")
    outbound_date: str = Field(description="The outbound date YYYY-MM-DD e.g. 2025-09-30")
    return_date: str = Field(description="The return date YYYY-MM-DD e.g. 2025-10-07")
    adults: Optional[int] = Field(1, description="The numbers of the adults. Default to 1")
    childrens: Optional[int] = Field(0, description="The numbers of the childrens. Default to 0")
    
class FlightsSchema(BaseModel):
    params : FlightsInput
    
@tool(args_schema=FlightsSchema)
def flight_finder(params:FlightsInput):
    """
    This tool uses the SerpApi Google Flights API to retrieve flights info.
    Parameters:
    Descrizione
    Questo script Python implementa uno strumento per la ricerca dei voli utilizzando l'API di Google Flights attraverso
    SerpAPI. Lo strumento è strutturato per essere utilizzato come componente di LangChain, un framework per
    applicazioni basate su AI.
    Il codice si articola in diverse parti fondamentali:
    Il sistema inizia caricando le variabili d'ambiente necessarie, in particolare la chiave API di SerpAPI, utilizzando la
    libreria dotenv.
    La struttura dei dati in ingresso è definita attraverso due classi Pydantic: FlightsInput e FlightsInputSchema.
    FlightsInput definisce tutti i parametri necessari per una ricerca voli:
    La funzione principale flights_finder è decorata come tool di LangChain e accetta questi parametri strutturati. La
    funzione:
    departure (str): The departure airport code (IATA).
    arrival (str): The arrival airport code (IATA).
    outbound_date (str): The outbound date (YYYY-MM-DD) e.g. 2025-09-30.
    return_date (str): The return date (YYYY-MM-DD) e.g. 2025-10-07.
    adults (int): The numbers of the adults. Default to 1.
    childrens (int): The numbers of the childrens. Default to 0.
    Returns:
    dict: A dictionary containing the flights info. If the API call fails, it returns the
    error message as a string."""
    
    try:
        params = {
            "api_key" : os.getenv('OPENAI_API_KEY'),
            "engine": "google_flights",
            "departure_id": params.departure,
            "arrival_id": params.arrival,
            "outbound_date": params.outbound_date,
            "return_date": params.return_date,
            "currency": "EUR",
            "hl": "it",
            "gl": "it",
            "stops": "1"                        
        }
        
        search = GoogleSearch(params)
        
        # print('*' * 80)
        # print('flight_finder')
        # print('*' * 80)
        return search.get_dict()
    
    except Exception as e:
        return str(e)