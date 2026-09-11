import logging
import os

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

# ==========================================
# LOGGING
# ==========================================
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

REQUIRED_ENV_VARS = {
    "GOOGLE_API_KEY": GOOGLE_API_KEY,
    "TAVILY_API_KEY": TAVILY_API_KEY,
}

missing_vars = [name for name, value in REQUIRED_ENV_VARS.items() if not value]
if missing_vars:
    raise RuntimeError(
        f"Missing required environment variable(s): {', '.join(missing_vars)}. "
        "Copy .env.example to .env and fill in your API keys."
    )

# Initialize the Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    google_api_key=GOOGLE_API_KEY
)

# Define tools (Tavily web search)
tools = [TavilySearchResults(max_results=3)]

# ReAct prompt template, hardcoded locally (matches the "hwchase17/react"
# LangChain Hub prompt) to avoid the deprecated langchainhub client and the
# runtime dependency on an external hub fetch on every startup.
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

# Create the ReAct agent
agent = create_react_agent(llm, tools, prompt)

# Create the agent executor
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=os.getenv("LOG_LEVEL", "INFO").upper() == "DEBUG",
    handle_parsing_errors=True,
)

# Test the agent
if __name__ == "__main__":
    query = "What is the current weather in Karachi?"

    try:
        response = agent_executor.invoke({"input": query})
    except Exception:
        logger.exception("Agent execution failed")
        raise

    logger.info("Agent run complete")
    print("\n\nFinal Answer:", response["output"])
