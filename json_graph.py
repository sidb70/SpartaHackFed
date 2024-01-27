import json
import matplotlib.pyplot as plt
import networkx as nx

class UserNode:
    def __init__(self, user_number, ip, port):
        self.user_number = user_number
        self.ip = ip
        self.port = port

class UserGraph:
    def __init__(self):
        self.nodes = {}
        self.edges = []

    def add_user(self, user_number, ip, port):
        if user_number not in self.nodes:
            self.nodes[user_number] = UserNode(user_number, ip, port)

    def add_edge(self, user1, user2):
        if user1 in self.nodes and user2 in self.nodes:
            self.edges.append((user1, user2))

    def to_networkx_graph(self):
        G = nx.DiGraph()  # Use Directed Graph
        for user_number, user in self.nodes.items():
            G.add_node(user_number, ip=user.ip, port=user.port)
        G.add_edges_from(self.edges)
        return G

def read_json_and_create_graph(file_path):
    # with open(file_path, 'r') as file:
    #     data = json.load(file)

    data = [{"userNumber": 1, "ip": "", "port": ""}, {"userNumber": 2, "ip": "", "port": ""},{"userNumber": 3, "ip": "", "port": ""}]
    graph = UserGraph()
    for user in data:
        graph.add_user(user['userNumber'], user['ip'], user['port'])

    # Adding edges in a sequential order
    for i in range(1, len(data)):
        graph.add_edge(data[i-1]['userNumber'], data[i]['userNumber'])

    return graph

def visualize_graph(G):
    pos = nx.spring_layout(G)
    labels = {node: f"{node}" for node in G.nodes}
    nx.draw(G, pos, labels=labels, with_labels=True, node_size=700, node_color='skyblue', arrows=True)
    plt.show()

# Usage
#file_path = 'path/to/your/file.json'
user_graph = read_json_and_create_graph("")
nx_graph = user_graph.to_networkx_graph()
visualize_graph(nx_graph)
