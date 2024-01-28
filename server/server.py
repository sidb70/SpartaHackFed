from typing import Tuple, Dict, List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from util.graph import create_graph,  UserGraph, Topology, UserNode
import requests
import json
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
    #print(user_data)
    # Create a graph
    graph = create_graph(user_data, topology=Topology.LINE)
    
    # convert graph to json
    graph_dict = graph_to_json(graph)
    # send graph_json to all users ip:port

    headers = {'Content-type': 'application/json'}
    graph_json = json.dumps(graph_dict)
    print(graph_json)
    for user_number, user_node in graph.nodes.items():
        requests.post(f"http://{user_node.ip}:{user_node.port}/api/receive", 
                      data=graph_json, headers=headers)
    return graph_json

def graph_to_json(graph: UserGraph):
    json = {}
    for user_number, user_node in graph.nodes.items():
        json[user_number] = {
            "ip": user_node.ip,
            "port": user_node.port,
            "edges": user_node.edges
        }
    return json
    
