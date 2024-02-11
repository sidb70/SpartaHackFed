import sys
sys.path.append("..")
from typing import Tuple, Dict, List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from util.graph import create_graph,  UserGraph, Topology, UserNode
import requests
import json
import asyncio 
import aiohttp
import uvicorn

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # This allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # This allows all HTTP methods
    allow_headers=["*"],  # This allows all headers
)
graph = {}
user_topology = None
@app.get("/")
def read_root():
    return {"Hello": "World"}


async def send_request_async(url, data, headers):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data, headers=headers) as response:
            # Assuming you want to print the response status code
            pass

@app.get("/api/get_graph")
async def get_graph():
    global graph
    global user_topology
    graph_list=[]
    if not graph:
        return {"Graph": []}
    if type(graph) != UserGraph:
        ips = list(graph.keys())
        for i in range(len(ips)):
            ip = ips[i]
            port = graph[ip]
            graph_list.append({
                "userNumber": i+1,
                "ip": ip,
                "port": port
            })
        user_topology = create_graph(graph_list, topology=Topology.RING)


    return {"Graph": graph_list}


@app.post("/api/add_node")
async def add_node(user_data: dict):
    # add the node to the graph
    global graph
    graph[user_data['ip']] = user_data['port']
    print(graph)
    


@app.post("/api/network_config")
async def get_network_config():
    # user_data will be a list of dictionaries containing userNumber, ip, and port
    #print(user_data)
    # Create a graph
    global user_topology
    
    # convert graph to json
    graph_dict = graph_to_json(user_topology)
    graph_json = json.dumps(graph_dict)
    
    headers = {'Content-type': 'application/json'}

    print(f'Graph: {graph_dict}')
    
    # for user_number, user_node in graph.nodes.items():
    #     print(f"{user_number}, http://{user_node.ip}:{user_node.port}/api/receive_graph")

    #     requests.post(f"http://{user_node.ip}:{user_node.port}/api/receive_graph", 
    #                   data=graph_json, headers=headers)

    tasks = []
    for user_number, user_node in user_topology.nodes.items():
        tasks.append(send_request_async(f"http://{user_node.ip}:{user_node.port}/api/receive_graph", graph_json, headers))
    await asyncio.gather(*tasks)

    # await asyncio.gather(*[requests.post(f"http://{user_node.ip}:{user_node.port}/api/receive_graph",
    #     data=graph_json, headers=headers) for user_number, user_node in graph.nodes.items()])

    return {"Recieved": "Graph"}

def graph_to_json(user_topology: UserGraph):
    json = {}
    for user_number, user_node in user_topology.nodes.items():
        json[user_number] = {
            "ip": user_node.ip,
            "port": user_node.port,
            "edges": user_node.edges
        }
    return json

if __name__ == "__main__":
    # Get external IP address using a third-party service (e.g., ifconfig.me)
    my_public_ip = requests.get('https://ifconfig.me/ip').text.strip()
    print(f"External IP Address: {my_public_ip}")
    uvicorn.run(app, host = my_public_ip, port=8000)
