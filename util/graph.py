from enum import Enum
class Topology(Enum):
    LINE = 1
    RING = 3
    MESH = 4
    HYBRID = 6

class UserNode:
    def __init__(self, user_number, ip, port):
        self.user_number = user_number
        self.ip = ip
        self.port = port
        self.edges = []
    def add_edge(self, user_number):
        self.edges.append(user_number)

class UserGraph:
    def __init__(self):
        self.nodes = {}

    def add_user(self, user_number, ip, port):
        if user_number not in self.nodes:
            self.nodes[user_number] = UserNode(user_number, ip, port)

    def add_edge(self, user1, user2, directed=True):
        if user1 in self.nodes and user2 in self.nodes:
            self.nodes[user1].add_edge(user2)
            if not directed:
                self.nodes[user2].add_edge(user1)


def create_graph(data, topology: Topology = Topology.LINE):
    graph = UserGraph()
    for user in data:
        graph.add_user(user['userNumber'], user['ip'], user['port'])
    print("USERS", len(data))

    # Adding edges in a sequential order
    if topology == Topology.RING:
        for i in range(1, len(data)):
            graph.add_edge(data[i-1]['userNumber'], data[i]['userNumber'], directed=True)
        graph.add_edge(data[-1]['userNumber'], data[0]['userNumber'], directed=True)
    
    elif topology == Topology.MESH:
        # fully connected graph
        for i in range(len(data)):
            for j in range(len(data)):
                if i != j:
                    graph.add_edge(data[i]['userNumber'], data[j]['userNumber'], directed=False)

    return graph


def graph_to_json(graph: UserGraph):
    json = {}
    for user_number, user_node in graph.nodes.items():
        json[user_number] = {
            "ip": user_node.ip,
            "port": user_node.port,
            "edges": user_node.edges
        }
    return json
if __name__ == '__main__':
    userData =[
        {"userNumber": 1, "ip": "141.151.661.013", "port": "2352"},
        {"userNumber": 2, "ip": "169.151.101.013", "port": "1512"},
        {"userNumber": 3, "ip": "", "port": ""},
    ]
    user_graph = create_graph(userData, topology=Topology.RING
    )
    print(graph_to_json(user_graph))