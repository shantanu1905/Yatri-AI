from crewai import Agent, LLM
from api.tools import search_tool
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
    goal=(
        "Discover the best tourist attractions and the best time to visit {destination}. "
        "Provide tailored recommendations based on the traveler's details, including start date ({start_date}), "
        "end date ({end_date}), budget ({budget}, optional), traveler type ({traveler_type}), "
        "and preferred activities ({activities})."
    ),
    verbose=True,
    memory=True,
    backstory=(
        "An experienced travel blogger with extensive knowledge of destinations worldwide. "
        "Provides personalized travel recommendations based on user preferences."
    ),
    tools=[search_tool],  # Uses both search and image search for better results
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
