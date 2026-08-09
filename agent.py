from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain import hub
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize the Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# Define tools (Tavily web search)
tools = [TavilySearchResults(max_results=3)]

# Pull the ReAct prompt template from LangChain Hub
prompt = hub.pull("hwchase17/react")

# Create the ReAct agent
agent = create_react_agent(llm, tools, prompt)

# Create the agent executor
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

# Test the agent
if __name__ == "__main__":
    query = "What is the current weather in Karachi?"
    response = agent_executor.invoke({"input": query})
    print("\n\nFinal Answer:", response["output"])