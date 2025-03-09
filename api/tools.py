from dotenv import load_dotenv
import os
from crewai_tools import SerperDevTool

load_dotenv()

# Load API Keys
os.environ['SERPER_API_KEY'] = os.getenv('SERPER_API_KEY')

# **Search Tool** - Uses Serper.dev to search Google for travel info
search_tool = SerperDevTool()


