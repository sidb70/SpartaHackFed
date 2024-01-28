from typing import Tuple, Dict, List
from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import torch
import requests
from models.loan_defaulter import LoanDefaulterModel, get_loan_defaulter_data
import json
import time
import asyncio

# Get external IP address using a third-party service (e.g., ifconfig.me)
external_ip = requests.get('https://ifconfig.me/ip').text.strip()
print(f"External IP Address: {external_ip}")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # This allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # This allows all HTTP methods
    allow_headers=["*"],  # This allows all headers
)

@app.get('/')
def read_root():
    return {"Hello": "World"}

@app.post("/api/receive_graph")
async def receive_graph(graph_data: dict):
    
    # load the graph
    global graph
    global external_ip
    graph = {int(k): v for k, v in graph_data.items()}
    print(graph)
    if graph[1]['ip'] == external_ip:
        print("I am the first node")
        await recieve_model(None)
    else:
        print("I am not the first node")
    return {"Recieved": "Graph"}

@app.post("/api/recieve_model")
async def recieve_model(file:UploadFile=None):
    print("Recieved model")

    file_bytes = None
    if (file):
        file_bytes = await file.read()

    node_hash = 1
    model = LoanDefaulterModel(get_loan_defaulter_data(node_hash), file_bytes)
    new_model = model.train()
    torch.save(new_model, 'model.pth')

    forward('model.pth')

    return {"Recieved": "Model"}


def forward(model_path:str):
    # send the model to the next node
    global graph
    global external_ip
    for user_number, user_node in graph.items():
        if user_node['ip'] == external_ip:
            edges = user_node['edges']
            break
    print(edges)

    file = open(model_path, 'rb')

    with open(model_path, "rb") as file:
        files = {"file": file}

        for edge in edges:
            edge_node = graph[edge]
            print(f"http://{edge_node['ip']}:{edge_node['port']}/api/recieve_model")
            requests.post(f"http://{edge_node['ip']}:{edge_node['port']}/api/recieve_model", files=files)

# def aggregate_models(state_dict1, state_dict2) -> dict:
#     # average the weights of the two models
#     if not state_dict1 or not state_dict2:
#         return
#     state_dict1_keys = state_dict1.keys()
#     state_dict2_keys = state_dict2.keys()
#     assert state_dict1_keys == state_dict2_keys

#     new_state_dict = {}
#     for key in state_dict1_keys:
#         new_state_dict[key] = (state_dict1[key] + state_dict2[key]) / 2.0
#     return new_state_dict


