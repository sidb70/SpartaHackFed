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

@app.post("/api/receive")
def read_root(graph_data: Dict[str, dict]):
    global graph
    if not graph:
        graph = graph_data
    train()
    print(graph_data)
    return {"Hello": "World"}

def train():
    print("Training...")