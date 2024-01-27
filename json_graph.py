import json
import networkx as nx
import matplotlib.pyplot as plt


# def read_json_file(file_path):
#     with open(file_path, 'r') as file:
#         data = json.load(file)
#     return data
#
#
# def create_graph_from_json(data):
#     G = nx.Graph()
#     for user in data:
#         G.add_node(user['userNumber'], ip=user['ip'], port=user['port'])
#     return G
#
#
# def visualize_graph(G):
#     pos = nx.spring_layout(G)  # positions for all nodes
#     nx.draw_networkx_nodes(G, pos)
#     nx.draw_networkx_labels(G, pos)
#
#     labels = nx.get_node_attributes(G, 'ip')
#     nx.draw_networkx_labels(G, pos, labels=labels, font_size=10, font_color='blue')
#
#     plt.show()
#
#
# # Example usage
# # json_data = read_json_file('path/to/your/file.json')
# print("x")
# json_data = [{"userNumber": 1, "ip": "", "port": ""}, {"userNumber": 2, "ip": "", "port": ""},{"userNumber": 3, "ip": "", "port": ""}]
# graph = create_graph_from_json(json_data)
# visualize_graph(graph)
#
#
#
# class UserNode:
#     def __init__(self, user_number, ip, port):
#         self.user_number = user_number
#         self.ip = ip
#         self.port = port

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
        G = nx.Graph()
        for user_number, user in self.nodes.items():
            G.add_node(user_number, ip=user.ip, port=user.port)
        G.add_edges_from(self.edges)
        return G

def read_json_and_create_graph(file_path):
    # with open(file_path, 'r') as file:
    #     data = json.load(file)

    data = [{"userNumber": 1, "ip": "", "port": ""}, {"userNumber": 2, "ip": "", "port": ""},
                 {"userNumber": 3, "ip": "", "port": ""}]

    graph = UserGraph()
    for user in data:
        graph.add_user(user['userNumber'], user['ip'], user['port'])

    # Example: Adding edges (modify as per your data or requirements)
    # This is just an example. You'll need to adjust it based on your JSON structure or other criteria.
    for i in range(1, len(data)):
        graph.add_edge(data[i-1]['userNumber'], data[i]['userNumber'])

    return graph

def visualize_graph(G):
    pos = nx.spring_layout(G)
    labels = {node: G.nodes[node]['ip'] for node in G.nodes}
    nx.draw(G, pos, labels=labels, with_labels=True, node_size=700, node_color='skyblue')
    plt.show()

# Usage
#file_path = 'path/to/your/file.json'
user_graph = read_json_and_create_graph("")
nx_graph = user_graph.to_networkx_graph()
visualize_graph(nx_graph)
