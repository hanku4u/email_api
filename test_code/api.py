# Create FastAPI app
from fastapi import FastAPI
app = FastAPI()

# Import the Rocketry app
from scheduler import app as app_rocketry
session = app_rocketry.session

@app.get("/my-route")
async def get_tasks():
    return session.tasks

@app.post("/my-route")
async def manipulate_session():
    for task in session.tasks:
        ...

if __name__ == "__main__":
    app.run()