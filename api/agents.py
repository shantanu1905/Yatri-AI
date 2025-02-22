from crewai import Agent, LLM
from tools import search_tool, image_tool
from dotenv import load_dotenv
import os

load_dotenv()

# Load Google Gemini API Key
llm = LLM(
    model="gemini/gemini-1.5-flash",
    api_key=os.getenv("GOOGLE_API_KEY"),
)

# **Tourist Guide Agent** - Finds best places to visit
tourist_guide = Agent(
    role="Tourist Guide",
    goal="Discover the best tourist attractions and best time to visit {destination}.",
    verbose=True,
    memory=True,
    backstory="An experienced travel blogger who knows the best places to explore.",
    tools=[search_tool],  # Uses search
    llm=llm,
    allow_delegation=True
)

# **Travel Agent** - Finds travel options (bus, train, flight)
travel_agent = Agent(
    role="Travel Expert",
    goal="Find the best ways to travel to {destination} including buses, trains, and flights.",
    verbose=True,
    memory=True,
    backstory="A travel expert with deep knowledge of transport options and ticket pricing.",
    tools=[search_tool],  # Uses only search tool
    llm=llm,
    allow_delegation=False
)
