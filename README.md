# Single AI Agent System

A ReAct-style AI agent built with LangChain, equipped with Tavily web search and a live weather lookup tool. The project includes both an OpenAI-powered entry point and a Google Gemini variant used during research.

## Features

- ReAct agent (`create_react_agent`) using `langchain`
- Pluggable LLM backend: OpenAI (`gpt-3.5-turbo`) in [main.py](main.py) or Google Gemini (`gemini-1.5-flash`) in [agent.py](agent.py)
- Tavily web search tool for real-time information
- Custom `get_weather_data` tool backed by the Weatherstack API
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
   OPENAI_API_KEY=your_openai_api_key_here
   GOOGLE_API_KEY=your_google_api_key_here
   TAVILY_API_KEY=your_tavily_api_key_here
   WEATHERSTACK_API_KEY=your_weatherstack_api_key_here
   ```

   - Get an OpenAI API key from [OpenAI Platform](https://platform.openai.com/api-keys) (required for `main.py`)
   - Get a Google API key from [Google AI Studio](https://aistudio.google.com/app/apikey) (required for `agent.py`)
   - Get a Tavily API key from [tavily.com](https://tavily.com)
   - Get a Weatherstack API key from [weatherstack.com](https://weatherstack.com)

   **Never commit your `.env` file** — it is already excluded via `.gitignore`.

## Usage

Run the OpenAI-powered agent (default entry point):

```bash
python main.py
```

Run the Gemini-powered agent:

```bash
python agent.py
```

## Project Structure

```
.
├── main.py                    # OpenAI-powered ReAct agent with search + weather tools
├── agent.py                   # Gemini-powered ReAct agent (search only)
├── research/
│   └── agent_demo.ipynb       # Exploratory notebook for agent development
├── requirements.txt           # Python dependencies
├── .env.example                # Template for required environment variables
└── .gitignore
```
