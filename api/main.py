from fastapi import FastAPI
from api.database import create_db_and_tables
from api.routers import travel
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

# Allow CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Initialize database tables
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Register Routers
app.include_router(travel.router)
