from fastapi import FastAPI
from routers import teams
from routers import users
from routers import matches
from routers import bets

app = FastAPI()

app.include_router(teams.router)
app.include_router(users.router)
app.include_router(matches.router)
app.include_router(bets.router)


@app.get("/")
def root():
    return {"message": "World Cup Pronostics API"}
