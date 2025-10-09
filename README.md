# Travel AI Assistant
### Travel AI Assistant è un assistente intelligente basato su AI pensato per aiutarti a pianificare viaggi, escursioni e vacanze senza stress. Fornisce suggerimenti su voli, hotel e itinerari personalizzati, tutto in un unico strumento.

## Caratteristiche principali
#### - Pianificazione voli ✈️: trova le migliori opzioni di volo per le tue date e preferenze.
#### - Suggerimenti hotel 🏨: scopri hotel con foto, prezzi, servizi e valutazioni.
#### - Itinerari di viaggio 🗺️: crea piani dettagliati giorno per giorno, con    attività consigliate.
#### - Consigli storici e culturali 🏛️: approfondimenti su luoghi e monumenti da visitare.
#### - Output ricco e leggibile: markdown, emoji e link utili per prenotazioni e informazioni

## Tecnologie utilizzate
- Python 
- Langchain per: orchestrazione AI
- OpenAi gpt-4o: per generazione dei contenuti
- SerpApi: per dati aggiornati su voli, hotel e attrazioni


# Comandi principali:
### - Comando di run:
```bash
poetry run uvicorn nome_progetto.main:app --reload --port 8080
```
### - Creare progetto:
```bash
poetry new nome_progetto
```
### - Installare le dipendenze:
```bash
poetry install
```
### - Attivare l'ambiente virtuale:
```bash
poetry env activate
```
### - Aggiungere libreria:
```bash
poetry add nome_libreria
