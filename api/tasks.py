from crewai import Task
from tools import search_tool, image_tool
from agents import tourist_guide, travel_agent

# **Task 1: Find Places to Visit & Best Time**
places_task = Task(
    description=(
        "Research and list the top 5 places to visit in {destination}. "
        "For each place, provide a brief description, the best time to visit, "
        "and a direct image URL from Google Image Search."
    ),
    expected_output="A list of top 5 places to visit in {destination} with descriptions, best time to visit, and image URLs.",
    tools=[search_tool, image_tool],  # Uses both search + image search
    agent=tourist_guide,
)

# **Task 2: Find Travel Options**
travel_task = Task(
    description=(
        "Find the best travel options to {destination}. "
        "Provide details on flights, trains, and buses, including estimated travel time and cost."
    ),
    expected_output="A comparison of travel options to {destination}, including estimated costs.",
    tools=[search_tool],  # Uses only search tool
    agent=travel_agent,
)
