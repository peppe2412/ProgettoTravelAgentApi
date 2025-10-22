from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import List, Literal
from travel_agent_api.services.agent_service import Agent

router = APIRouter()

class Message(BaseModel):
    role: Literal["user", "system", "assistant"] = Field(..., example="user")
    content: str = Field(..., example="Voglio organizzare un viaggio a Venezia")

class ChatRequestCompletion(BaseModel):
    messages: List[Message]
    model_config = {
        "json_schema_extra":{
            "example":{
                "messages": [
                    {
                        "role":"user",
                        "content":"Voglio organizzare un viaggio a Venezia"
                    },
                    {
                        "role":"user",
                        "content":"Mi interessa The Venice Venice Hotel, per l'hotel"
                    }
                ]
            }
        }
    }

@router.post('/travel-agent')
def chat_completion(request: ChatRequestCompletion):
    """
    Endpoint per la gestione delle richieste di chat.
    Processa i messaggi ricevuti e restituisce una risposta dall'agente di viaggio.
    Args:
    request (ChatRequestCompletion): La richiesta contenente i messaggi della
    conversazione
    Returns:
    dict: La risposta elaborata dall'agente di viaggio
    Raises:
    HTTPException: In caso di errori durante l'elaborazione della richiesta
    """    
    agent = Agent()
    messages_dict = [{"role": msg.role, "content": msg.content} for msg in request.messages]
    response = agent.run(messages=messages_dict)
    
    ai_response = [msg.content for msg in response if msg.__class__.__name__ == 'AIMessage']
    text_response = ai_response[-1] if ai_response else 'Nessuna risposta'
    
    # print('*' * 80)
    # print('chat_completion')
    # print('*' * 80)
    return {'response':text_response}