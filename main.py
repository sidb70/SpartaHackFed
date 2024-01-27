from typing import Tuple, Dict, List
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/api/network_config")
def get_network_config(user_data: List[dict]):
    # user_data will be a list of dictionaries containing userNumber, ip, and port
    print(user_data)
    return {"message": "Data received successfully"}

