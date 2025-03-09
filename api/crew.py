# from crewai import Crew, Process
# from api.tasks import places_task 
# from api.agents import tourist_guide
# from dotenv import load_dotenv
# import os

# load_dotenv()

# # Verify API Key is loaded
# if not os.getenv("GOOGLE_API_KEY"):
#     raise ValueError("GOOGLE_API_KEY is missing. Check your .env file.")

# # Define user inputs
# trip_inputs = {
#     'destination': 'Leh Ladakh',  # Example destination
#     'start_date': '2024-06-10',  # Example start date
#     'end_date': '2024-06-12',  # Example end date
#     'budget': 500,  # Optional, remove if not provided
#     'traveler_type': 'solo',  # Example: solo, friends, family, etc.
#     'activities': ['adventure', 'spirituality']  # Example preferences
# }

# # Create the AI Crew
# crew = Crew(
#     agents=[tourist_guide],
#     tasks=[places_task],
#     process=Process.sequential,  # Tasks run one after another
# )

# # Run Trip Planner with updated inputs
# result = crew.kickoff(inputs=trip_inputs)
# print(result)
