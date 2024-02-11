from typing import Tuple, Dict, List
from fastapi import FastAPI, UploadFile, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import torch
import requests
from models.loan_defaulter import LoanDefaulterModel, get_loan_defaulter_data
import io
import uvicorn
import argparse
import asyncio
from aiohttp import ClientSession, FormData
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # This allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # This allows all HTTP methods
    allow_headers=["*"],  # This allows all headers
)

graph = {}
my_public_ip=None
training=False
defaulterModel = LoanDefaulterModel()


async def send_files_async(url, file, filename, headers):
    data = FormData()
    data.add_field('file', file, filename=filename)
    async with ClientSession() as session:
        async with session.post(url, data=data, headers=headers) as response:
            pass # dont care if the request was successful or not. TODO: use UDP

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
    train()


def train():
    global training
    global defaulterModel
    training = True

    defaulterModel.train()
    training=False
    forward()

def forward(model_path:str = 'model_state_dict.pth'):
    # send the model to the next node
    global graph
    global my_public_ip
    print(f'graph: {graph}, external_ip: {my_public_ip}')
    for user_number, user_node in graph.items():
        if user_node['ip'] == my_public_ip:
            edges = user_node['edges']
            break

    print(edges)
    tasks = []
    with open(model_path, "rb") as file:
        files = {"file": file}
        for edge in edges:
            edge_node = graph[edge]
            print('queuing', edge_node['ip'])
            url = f"http://{edge_node['ip']}:{edge_node['port']}/api/recieve_model"
            tasks.append(send_files_async(url, files['file'], model_path, {}))
    asyncio.run(asyncio.wait(tasks))
@app.post("/api/recieve_model")
async def recieve_model(background_tasks: BackgroundTasks, file:UploadFile=None):
    '''    
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
        '''


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

def run():
    global my_public_ip

    parser = argparse.ArgumentParser(description="Run the client")
    parser.add_argument("--server_ip", type=str, help="The IP address of the server")
    args = parser.parse_args()
    server_ip = args.server_ip

    # Get external IP address using a third-party service (e.g., ifconfig.me)
    my_public_ip = requests.get('https://ifconfig.me/ip').text.strip()
    print(f"External IP Address: {my_public_ip}")
    requests.post(f"http://{server_ip}:8000/api/add_node", json={"ip": my_public_ip, "port": 8001})
     
    uvicorn.run(app, host = my_public_ip, port=8001)

if __name__=='__main__':
    run()