from crewai import Crew, Process
from tasks import places_task, travel_task
from agents import tourist_guide, travel_agent
from dotenv import load_dotenv
import os

load_dotenv()

# Verify API Key is loaded
if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("GOOGLE_API_KEY is missing. Check your .env file.")

# Create the AI Crew
crew = Crew(
    agents=[tourist_guide,],
    tasks=[places_task],
    process=Process.sequential,  # Tasks run one after another
)

# Run Trip Planner for Rishikesh
result = crew.kickoff(inputs={'destination': 'Rishikesh'})
print(result)
