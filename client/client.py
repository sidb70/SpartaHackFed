from typing import Tuple, Dict, List
from fastapi import FastAPI, UploadFile, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import torch
import requests
from models.loan_defaulter import LoanDefaulterModel, get_loan_defaulter_data
import io

# Get external IP address using a third-party service (e.g., ifconfig.me)
my_public_ip = requests.get('https://ifconfig.me/ip').text.strip()
print(f"External IP Address: {my_public_ip}")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # This allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # This allows all HTTP methods
    allow_headers=["*"],  # This allows all headers
)

daniel_ip = "35.21.162.32"
sid_ip = "35.21.231.182"
server_ip = sid_ip

requests.post(f"http://{server_ip}:8000/api/add_node", json={"ip": my_public_ip, "port": 8001})

graph = {}

@app.get('/')
def read_root():
    return {"Hello": "World"}

@app.post("/api/receive_graph")
async def receive_graph(graph_data: dict):
    
    # load the graph
    global graph
    global my_public_ip
    graph = {int(k): v for k, v in graph_data.items()}
    print(graph)
    if graph[1]['ip'] == my_public_ip:
        print("I am the first node")
        await recieve_model(None)
    else:
        print("I am not the first node")
    return {"Recieved": "Graph"}


processing = False

@app.post("/api/recieve_model")
async def recieve_model(background_tasks: BackgroundTasks, file:UploadFile=None):
    global processing
    if processing:
        return {"Processing": "None"}

    processing = True

    print("Recieved model")

    file_bytes = None
    if (file):
        file_bytes = await file.read()
        file = io.BytesIO(file_bytes)
    
    print(type(file_bytes))

    node_hash = int(my_public_ip.split('.')[-1])
    model = LoanDefaulterModel(get_loan_defaulter_data(node_hash), file)
    new_model = model.train()
    torch.save(new_model, 'model.pth')

    if (background_tasks):
        background_tasks.add_task(forward, 'model.pth')
    else:
        forward('model.pth')

    processing = False
    return {"Recieved": "Model"}




def forward(model_path:str):
    # send the model to the next node
    global graph
    global my_public_ip
    print(f'graph: {graph}, external_ip: {my_public_ip}')
    for user_number, user_node in graph.items():
        if user_node['ip'] == my_public_ip:
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


