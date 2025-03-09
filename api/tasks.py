from crewai import Task
from api.tools import search_tool
from api.agents import tourist_guide, travel_agent 
from api.schemas import *
# **Task 1: Discover Top Attractions & Best Time to Visit (Day-wise Itinerary)**
places_task = Task(
    description=(
        "Generate a travel itinerary for {destination} by listing top attractions to visit, "
        "including descriptions, best visiting times, and nearby points of interest. "
        "Take into account user inputs such as start date ({start_date}), end date ({end_date}), "
        "budget ({budget}, optional), traveler type ({traveler_type}), and preferred activities ({activities})."
    ),
    expected_output=(
        "A structured JSON containing:\n"
        "- location_name: The name of the destination.\n"
        "- location_description: A brief overview of the place.\n"
        "- ideal_visit_time: Recommended time to visit based on weather and attractions.\n"
        "- itinerary: A list of must-visit attractions including:\n"
        "  - place_name: Name of the attraction.\n"
        "  - description: A short description of the site.\n"
        "  - best_time_to_visit: Ideal time to explore this attraction.\n"
        "  - nearby_points_of_interest: Other notable places in the vicinity.\n"
        "- other_stuff_to_do: List of additional activities such as yoga, meditation, rafting, etc."
    ),
    tools=[search_tool],  # Uses only search tool
    agent=tourist_guide,
    output_json=TravelPlan
    
)



# **Task 2: Find Travel Options**
travel_task = Task(
    description=(
        "Find the best travel options to {destination}. "
        "Provide details on flights, trains, and buses, including estimated travel time and cost."
    ),
    expected_output="A comparison of travel options to {destination}, including estimated costs.",
    tools=[search_tool, ],  # Uses only search tool
    agent=travel_agent,
)
