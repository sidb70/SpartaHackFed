from typing import Tuple, Dict, List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
graph = {}
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # This allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # This allows all HTTP methods
    allow_headers=["*"],  # This allows all headers
)

@app.post("/api/receive_graph")
def read_root(graph_data: Dict[str, dict]):
    global graph
    graph = graph_data
    print(graph_data)
    return {"Recieved": "Graph"}

@app.post("/api/recieve_model")
def recieve_model(model: dict):
    print(model)
    return {"Recieved": "Model"}