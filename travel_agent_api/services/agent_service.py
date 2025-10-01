from datetime import datetime
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from travel_agent_api.tools.flights_find import flight_finder
from travel_agent_api.tools.hotels_find import hotel_finder
from travel_agent_api.tools.chain_historical_expert import chain_historical_expert
from travel_agent_api.tools.chain_travel_plan import chain_travel_plan

FLIGHTS_OUTPUT = """
    format: markdown
        ##Miglior Opzione
        
        ### Andata:
        - Compagnia aerea: Ryanair
        - Data di partenza: 2025-09-30
        - Ora di partenza: 9:00
        - Durata volo: 1h 30m
        
        ### Ritorno:
        - Compagnia aerea: Ryanair
        - Data di partenza: 2025-10-07
        - Ora di partenza: 11:00
        - Durata volo: 1h 30m
        
        Se è disponibile, inserisci il link di google per la prenotazione
        
        #### Altri opzioni disponibili:
        - Compagnia aerea: Ryanair
        - Data di partenza: 2025-10-02
        - Ora di partenza: 10:00
        - Durata del volo: 1h 30m
        - Compagnia aerea: Ryanair
        - Data di ritorno: 2025-10-09
        - Ora di ritorno: 14:30
        - Durata del volo: 1h 30m

        Se è disponibile, inserisci il link di google per la prenotazione
        """
    
HOTELS_OUTPUT = """
    format: markdown
    
        #### Hotel 1        
        Se è disponibile, inserire la foto dell'hotel.
        
        *Descrizione:* Camere e suite eleganti, a volte con vista sulla città, in hotel esclusivo
        con piscina panoramica e spa.
        
        *Prezzo per notte:* €296 (prima delle tasse e spese: €260)
        
        *Prezzo totale:* €1,660 (prima delle tasse e spese: €1,336)
        
        *Check-in:* 15:00, Check-out: 12:00
        
        *Valutazione complessiva:* 4.5 su 5
        
        *Servizi Inclusi:* Spa, Piscina, Parcheggio gratuito
        
        
        #### Hotel 2        
        Se è disponibile, inserire la foto dell'hotel.
        
        Descrizione: Hotel in stile Liberty con alloggi arredati in maniera artistica, ristorante
        elegante, bar e spa.
        
        *Prezzo per notte:* €380 (prima delle tasse e spese: €333)
        
        *Prezzo totale:* €3,418 (prima delle tasse e spese: €3,000)
        
        *Check-in:* 15:00, Check-out: 12:00
        
        *Valutazione complessiva:* 4.5 su 5
        
        *Servizi Inclusi:* Spa, Piscina, Parcheggio gratuito

    """
    
TRAVEL_PLAN_OUTPUT = """
    format: markdown

        ### Giorno 1 - 2025-10-01
        
        *Mattina:* Descrizione dell'attivita' da svolgere la mattina
        
        *Pomeriggio:* Descrizione dell'attivita' da svolgere il pomeriggio
        
        *Sera:* Descrizione dell'attivita' da svolgere la sera
        
        ### Giorno 2 - 2025-10-02
        
        *Mattina:* Descrizione dell'attivita' da svolgere la mattina
        
        *Pomeriggio:* Descrizione dell'attivita' da svolgere il pomeriggio
        
        *Sera:* Descrizione dell'attivita' da svolgere la sera
        
        ### Giorno 3 - 2025-10-03
        
        *Mattina:* Descrizione dell'attivita' da svolgere la mattina
        
        *Pomeriggio:* Descrizione dell'attivita' da svolgere il pomeriggio
        
        *Sera:* Descrizione dell'attivita' da svolgere la sera
        
        ### Giorno 4 - 2025-10-04
        
        *Mattina:* Descrizione dell'attivita' da svolgere la mattina
        
        *Pomeriggio:* Descrizione dell'attivita' da svolgere il pomeriggio
        
        *Sera:* Descrizione dell'attivita' da svolgere la sera
        
        ### Giorno 5 - 2025-10-05
        
        *Mattina:* Descrizione dell'attivita' da svolgere la mattina
        
        *Pomeriggio:* Descrizione dell'attivita' da svolgere il pomeriggio
        
        *Sera:* Descrizione dell'attivita' da svolgere la sera
        
        ### Giorno 6 - 2025-10-06
        
        *Mattina:* Descrizione dell'attivita' da svolgere la mattina
        
        *Pomeriggio:* Descrizione dell'attivita' da svolgere il pomeriggio
        
        *Sera:* Descrizione dell'attivita' da svolgere la sera
        
        ### Giorno 7 - 2025-10-07
        
        *Mattina:* Descrizione dell'attivita' da svolgere la mattina
        
        *Pomeriggio:* Descrizione dell'attivita' da svolgere il pomeriggio
        
        *Sera:* Descrizione dell'attivita' da svolgere la sera
        
    """
    
class Agent:
    def __init__(self):
        self.current_datetime = datetime.now()
        self.model = ChatOpenAI(model_name="gpt-4o")
        self.tools = [
            flight_finder,
            chain_historical_expert,
            hotel_finder,
            chain_travel_plan
        ]
        self.agent_exe = create_react_agent(self.model, self.tools)
        pass
    
    def run(self, messages : list):
        SYSTEM_PROMPT = f"""
            Sei un travel planner. Il tuo compito e' organizzare il viaggio per l'utente.
            Aggiungi delle emojis per rendere il tuo output piu' interessante.
            La data di oggi e' {self.current_datetime}
            Usa le seguenti istruzioni per creare un output:
            Esempio Ouput Voli:
            {FLIGHTS_OUTPUT}
            Esempio Output Hotel:
            {HOTELS_OUTPUT}
            Esempio di Output Viaggio:
            {TRAVEL_PLAN_OUTPUT}
            """
        conversation_history = [{'role':'system', 'content': SYSTEM_PROMPT}] + messages
        response = self.agent_exe.invoke({'messages':conversation_history})
        return response.get('messages', []) [1:]