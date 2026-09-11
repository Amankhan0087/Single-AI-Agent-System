import logging
import os

import certifi
import requests
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults

from langchain.agents import (
    create_react_agent,
    AgentExecutor
)
from langchain_core.prompts import PromptTemplate

# ==========================================
# LOGGING
# ==========================================
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

# ==========================================
# LOAD ENV VARIABLES
# ==========================================
os.environ["SSL_CERT_FILE"] = certifi.where()
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
WEATHERSTACK_API_KEY = os.getenv("WEATHERSTACK_API_KEY")

REQUIRED_ENV_VARS = {
    "GOOGLE_API_KEY": GOOGLE_API_KEY,
    "TAVILY_API_KEY": TAVILY_API_KEY,
    "WEATHERSTACK_API_KEY": WEATHERSTACK_API_KEY,
}

missing_vars = [name for name, value in REQUIRED_ENV_VARS.items() if not value]
if missing_vars:
    raise RuntimeError(
        f"Missing required environment variable(s): {', '.join(missing_vars)}. "
        "Copy .env.example to .env and fill in your API keys."
    )

REQUEST_TIMEOUT_SECONDS = 10

# ==========================================
# SEARCH TOOL
# ==========================================

search_tool = TavilySearchResults(max_results=2)

# ==========================================
# WEATHER TOOL
# ==========================================

@tool
def get_weather_data(city: str) -> str:
    """
    Fetch current weather information for a city.
    """
    url = "https://api.weatherstack.com/current"
    params = {"access_key": WEATHERSTACK_API_KEY, "query": city}

    try:
        response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT_SECONDS)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as exc:
        logger.error("Weather request failed for %s: %s", city, exc)
        return f"Could not fetch weather data for {city}: request failed."

    if data.get("success") is False:
        error_info = data.get("error", {}).get("info", "unknown error")
        logger.error("Weatherstack error for %s: %s", city, error_info)
        return f"Could not fetch weather data for {city}: {error_info}"

    if "current" not in data:
        return f"Could not fetch weather data for {city}"

    return (
        f"City: {city}\n"
        f"Temperature: {data['current']['temperature']}°C\n"
        f"Weather: {data['current']['weather_descriptions'][0]}\n"
        f"Humidity: {data['current']['humidity']}%"
    )

# ==========================================
# LLM
# ==========================================

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    temperature=0,
    google_api_key=GOOGLE_API_KEY
)

# ==========================================
# PROMPT
# ==========================================
# Hardcoded locally (matches the "hwchase17/react" LangChain Hub prompt) to
# avoid the deprecated langchainhub client and the runtime dependency on an
# external hub fetch on every startup.

prompt = PromptTemplate.from_template(
    "Answer the following questions as best you can. You have access to the "
    "following tools:\n\n{tools}\n\nUse the following format:\n\nQuestion: "
    "the input question you must answer\nThought: you should always think "
    "about what to do\nAction: the action to take, should be one of "
    "[{tool_names}]\nAction Input: the input to the action\nObservation: "
    "the result of the action\n... (this Thought/Action/Action Input/"
    "Observation can repeat N times)\nThought: I now know the final answer"
    "\nFinal Answer: the final answer to the original input question\n\n"
    "Begin!\n\nQuestion: {input}\nThought:{agent_scratchpad}"
)

# ==========================================
# TOOLS
# ==========================================

tools = [
    search_tool,
    get_weather_data
]

# ==========================================
# CREATE AGENT
# ==========================================

agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)

# ==========================================
# EXECUTOR
# ==========================================

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=os.getenv("LOG_LEVEL", "INFO").upper() == "DEBUG",
    handle_parsing_errors=True,
)

# ==========================================
# RUN
# ==========================================

if __name__ == "__main__":
    query = (
        "Find the capital of India "
        "and then find its current weather."
    )

    try:
        response = agent_executor.invoke({"input": query})
    except Exception:
        logger.exception("Agent execution failed")
        raise

    logger.info("Agent run complete")
    print("\n========================")
    print("FINAL OUTPUT")
    print("========================\n")
    print(response["output"])
