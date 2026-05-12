from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import teams
from routers import users
from routers import matches
from routers import bets

app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(teams.router)
app.include_router(users.router)
app.include_router(matches.router)
app.include_router(bets.router)


@app.get("/")
def root():
    return {"message": "World Cup Pronostics API"}
