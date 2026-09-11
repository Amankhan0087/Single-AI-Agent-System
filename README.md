# Single AI Agent System

A ReAct-style AI agent built with LangChain, powered by Google's Gemini model, equipped with Tavily web search and a live weather lookup tool.

## Features

- ReAct agent (`create_react_agent`) using `langchain`
- Google Gemini (`gemini-3.5-flash-lite`) as the LLM in both [main.py](main.py) and [agent.py](agent.py)
- Tavily web search tool for real-time information
- Custom `get_weather_data` tool backed by the Weatherstack API (in [main.py](main.py))
- Exploratory notebook in [research/agent_demo.ipynb](research/agent_demo.ipynb)

## Setup

1. Create and activate the environment:

   ```bash
   conda create -n langagent python=3.11 -y
   conda activate langagent
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables:

   Copy `.env.example` to `.env` and fill in your own API keys:

   ```bash
   cp .env.example .env
   ```

   ```
   GOOGLE_API_KEY=your_google_api_key_here
   TAVILY_API_KEY=your_tavily_api_key_here
   WEATHERSTACK_API_KEY=your_weatherstack_api_key_here
   ```

   - Get a Google API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Get a Tavily API key from [tavily.com](https://tavily.com)
   - Get a Weatherstack API key from [weatherstack.com](https://weatherstack.com) (required for `main.py`)

   **Never commit your `.env` file** — it is already excluded via `.gitignore`.

## Usage

Run the main agent (search + weather tools):

```bash
python main.py
```

Run the minimal agent (search only):

```bash
python agent.py
```

## Project Structure

```
.
├── main.py                    # Gemini-powered ReAct agent with search + weather tools
├── agent.py                   # Gemini-powered ReAct agent (search only)
├── research/
│   └── agent_demo.ipynb       # Exploratory notebook for agent development
├── requirements.txt           # Python dependencies
├── .env.example                # Template for required environment variables
└── .gitignore
```
