from typing import Tuple, Dict, List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import torch
from train import train_model
import requests

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

@app.post("/api/receive_graph")
def receive_graph(graph_data: dict):
    # load the graph
    global graph
    global external_ip
    graph = {int(k): v for k, v in graph_data.items()}
    print(graph)
    if graph[1]['ip'] == external_ip:
        print("I am the first node")
        recieve_model(None)
    else:
        print("I am not the first node")
    return {"Recieved": "Graph"}

@app.post("/api/recieve_model")
def recieve_model(model: dict):
    print("Recieved model")
    try:
        state_dict = torch.load('model.pth')
        if not model:
            new_state_dict = train_model(state_dict)
        else:
            new_state_dict = train_model(aggregate_models(state_dict, model))
    except FileNotFoundError:
        new_state_dict = train_model(None)
    torch.save(new_state_dict, 'model.pth')
    forward()
    return {"Recieved": "Model"}
def forward():
    # send the model to the next node
    global graph
    global external_ip
    for user_number, user_node in graph.items():
        if user_node['ip'] == external_ip:
            edges = user_node['edges']
            break
    #print(edges)
    for edge in edges:
        edge_node = graph[edge]
        print(f"http://{edge_node['ip']}:{edge_node['port']}/api/recieve_model")
        requests.post(f"http://{edge_node['ip']}:{edge_node['port']}/api/recieve_model", data=torch.load('model.pth'))
def aggregate_models(state_dict1, state_dict2) -> dict:
    # average the weights of the two models
    if not state_dict1 or not state_dict2:
        return
    state_dict1_keys = state_dict1.keys()
    state_dict2_keys = state_dict2.keys()
    assert state_dict1_keys == state_dict2_keys

    new_state_dict = {}
    for key in state_dict1_keys:
        new_state_dict[key] = (state_dict1[key] + state_dict2[key]) / 2.0
    return new_state_dict


