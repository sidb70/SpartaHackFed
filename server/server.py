import sys
sys.path.append("..")
from typing import Tuple, Dict, List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from util.graph import create_graph,  UserGraph, Topology, UserNode
import requests
import json
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # This allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # This allows all HTTP methods
    allow_headers=["*"],  # This allows all headers
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
    graph_json = json.dumps(graph_dict)
    
    headers = {'Content-type': 'application/json'}
    
    for user_number, user_node in graph.nodes.items():
        requests.post(f"http://{user_node.ip}:{user_node.port}/api/receive_graph", 
                      data=graph_json, headers=headers)
    return {"Recieved": "Graph"}

def graph_to_json(graph: UserGraph):
    json = {}
    for user_number, user_node in graph.nodes.items():
        json[user_number] = {
            "ip": user_node.ip,
            "port": user_node.port,
            "edges": user_node.edges
        }
    return json
    
