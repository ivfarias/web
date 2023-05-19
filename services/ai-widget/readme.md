This is a Python script that serves as the main entrypoint for a chatbot application built with FastAPI. The chatbot uses LangChain, a language model developed by the same team, to generate responses to user input. The script sets up a WebSocket endpoint that accepts incoming messages from clients and sends back chatbot responses.

## Dependencies
This script has the following dependencies:

```
fastapi
uvicorn
jinja2
langchain (which in turn depends on transformers, torch, and numpy)
dotenv
```

## Installation and Setup
To use this script, follow these steps:

1. Clone the repository or download the files.
2. Install the dependencies using pip: pip install -r requirements.txt
3. Run the ingest.py script to create a vectorstore.pkl file that the chatbot uses to generate responses. The script expects the input data in data/input.txt.
4. Create a .env file with the following variables:
5. LANGCHAIN_API_URL - the URL of the LangChain API server
6. LANGCHAIN_API_KEY - the API key to use when accessing the LangChain API
7. Run the script using the following command: python main.py
8. The script will start a server on http://0.0.0.0:9000/ that can be accessed using a web browser or a WebSocket client.

## Usage
The chatbot accepts messages through a WebSocket connection to ws://localhost:9000/chat. Clients should send messages in plain text format. The chatbot responds with JSON objects that have the following fields:

sender - a string indicating who sent the message (you for client, bot for chatbot)
message - a string containing the message text
type - a string indicating the type of message (stream for client messages, start for the beginning of a chatbot response, end for the end of a chatbot response, error for error messages)
