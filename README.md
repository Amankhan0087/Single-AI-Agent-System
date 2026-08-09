# Single AI Agent System

A simple ReAct-style AI agent built with LangChain, powered by Google's Gemini model and equipped with Tavily web search.

## Features

- ReAct agent (`create_react_agent`) using `langchain`
- Google Gemini (`gemini-1.5-flash`) as the LLM
- Tavily web search tool for real-time information

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
   ```

   - Get a Google API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Get a Tavily API key from [tavily.com](https://tavily.com)

   **Never commit your `.env` file** — it is already excluded via `.gitignore`.

## Usage

```bash
python agent.py
```

## Project Structure

```
.
├── agent.py           # Main agent definition and entry point
├── requirements.txt   # Python dependencies
├── .env.example        # Template for required environment variables
└── .gitignore
```
