from flask import Flask, render_template, request, jsonify
import heapq 
from collections import deque

# Initilize the flask app
app = Flask(__name__, static_folder='interface')

def create_graph():
    graph = {
        "AD" : {"LH": {"distance":92, "time": 1, "accessibility": True}, "SGMH": {"distance":528, "time": 3, "accessibility": True}, "CJ": {"distance": 482, "time": 2, "accessibility": True}, "GH": {"distance": 528, "time": 2, "accessibility": True}, "MC": {"distance": 266, "time": 1, "accessibility": True }},
        "B"  : {"KHS": {"distance": 1056, "time": 3, "accessibility": True}, "PL": {"distance": 1584, "time": 6, "accessibility": True}, "TSU": {"distance": 1056, "time": 4, "accessibility": True}, "CPAC": {"distance": 1056, "time": 4, "accessibility": True}, "SRC": {"distance": 384, "time": 2, "accessibility": True}},
        "CC" : {"TS": {"distance": 1056, "time": 5, "accessibility": True}, "TTF": {"distance": 2112, "time": 9, "accessibility": True}},
        "CPAC" : {"B": {"distance": 1056, "time": 4, "accessibility": True}, "PL": {"distance": 1056, "time": 5, "accessibility": True}, "H": {"distance": 1584, "time": 6, "accessibility": True}, "MH": {"distance": 528, "time": 3, "accessibility": True}, "GC": {"distance": 1056, "time": 4, "accessibility": True}, "NPS": {"distance": 528, "time": 2, "accessibility": True}, "TSU": {"distance": 1056, "time": 4, "accessibility": True}, "VA": {"distance": 404, "time": 2, "accessibility": True}},
        "CS" : {"E": {"distance": 236, "time": 1, "accessibility": True}, "GAS": {"distance": 2640, "time": 11, "accessibility": True}, "ENPS": {"distance": 1584, "time": 6, "accessibility": True}},
        "E" : {"CS": {"distance": 236, "time": 1, "accessibility": True}, "RG": {"distance": 528, "time": 3, "accessibility": True}, "SHCC": {"distance": 276, "time": 1, "accessibility": True}, "EC": {"distance": 1056, "time": 4, "accessibility": True}},
        "DBH" : {"MH": {"distance": 528, "time": 3, "accessibility": True}, "MC": {"distance": 528 , "time": 3, "accessibility": True}, "LH": {"distance": 528, "time": 2, "accessibility": True}, "GC": {"distance": 528, "time": 2, "accessibility": True}},
        "EC" : {"PL": {"distance": 1056, "time": 4, "accessibility": True}, "H": {"distance": 528, "time": 3, "accessibility": True}, "E": {"distance": 1056, "time": 4, "accessibility": True}, "SHCC": {"distance": 1056, "time": 4, "accessibility": True}},
        "ENPS" : {"CS": {"distance": 1584, "time": 6, "accessibility": True}, "ESPS": {"distance": 381, "time": 2, "accessibility": True}},
        "ESPS" : {"ENPS": {"distance": 381, "time": 2, "accessibility": True}, "H": {"distance": 1056, "time": 5, "accessibility": True}, "CJ": {"distance": 1056, "time": 5, "accessibility": True}},
        "GAH" : {"UP": {"distance": 528, "time": 3, "accessibility": True}, "SCPS": {"distance": 190, "time": 1, "accessibility": True}, "TSU": {"distance": 128, "time": 1, "accessibility": True}},
        "GAS": {"CS": {"distance": 259, "time": 1, "accessibility": True}, "RG": {"distance": 528, "time": 3, "accessibility": True}, "RH": {"distance": 528, "time": 2, "accessibility": True}, "HRE": {"distance": 233, "time": 1, "accessibility": True}},
        "GC" : {"CPAC": {"distance": 1056, "time": 4, "accessibility": True}, "DBH": {"distance": 528, "time": 2, "accessibility": True}, "MH": {"distance": 2112, "time": 8, "accessibility": True}, "NPS": {"distance": 3168, "time": 12, "accessibility": True}},
        "GF" : {"TS": {"distance": 1584, "time": 6, "accessibility": True}, "AF": {"distance": 1056, "time": 5, "accessibility": True}, "TSC": {"distance": 374, "time": 2, "accessibility": True}},
        "GH" : {"H": {"distance": 285, "time": 1, "accessibility": True}, "MH": {"distance": 449, "time": 2, "accessibility": True}, "AD": {"distance": 528, "time": 2, "accessibility": True}, "LH": {"distance": 528, "time": 3, "accessibility": True}, "CJ": {"distance": 1056, "time": 3, "accessibility": True}},
        "H" : {"CPAC": {"distance": 1584, "time": 6, "accessibility": True}, "EC": {"distance": 528, "time": 3, "accessibility": True}, "ESPS": {"distance": 1056, "time": 5, "accessibility": True}, "GH": {"distance": 285, "time": 1, "accessibility": True}, "PL": {"distance": 528, "time": 3, "accessibility": True}, "MH": {"distance": 528, "time": 3, "accessibility": True}},
        "HRE": {"GAS": {"distance": 233, "time": 1, "accessibility": True}, "RH": {"distance": 1584, "time": 7, "accessibility": True}},
        "KHS": {"B": {"distance": 1056, "time": 3, "accessibility": True}, "SRC": {"distance": 213, "time": 1, "accessibility": True}, "TG": {"distance": 7, "time": 1, "accessibility": True}, "PL": {"distance": 1584, "time": 6, "accessibility": True}},
        "LH" : {"AD": {"distance": 92, "time": 1, "accessibility": True}, "DBH": {"distance": 528, "time": 2, "accessibility": True}, "GH": {"distance": 528, "time": 3, "accessibility": True}, "MH": {"distance": 528, "time": 3, "accessibility": True}, "MC": {"distance": 390, "time": 2, "accessibility": True}},
        "MC" : {"DBH":{"distance": 528, "time": 3, "accessibility": True} , "LH": {"distance": 390, "time": 2, "accessibility": True}, "AD": {"distance": 266, "time": 1, "accessibility": True}, "SGMH": {"distance": 1056, "time": 4, "accessibility": True}},
        "MH" : {"CPAC": {"distance": 528, "time": 3, "accessibility": True}, "DBH": {"distance": 528, "time": 3, "accessibility": True}, "GC": {"distance": 2112, "time": 8, "accessibility": True}, "GH": {"distance": 449, "time": 2, "accessibility": True}, "H": {"distance": 528, "time": 3, "accessibility": True}, "LH": {"distance": 528, "time": 3, "accessibility": True}},
        "MS" : {"TSF": { "distance": 1584, "time" : 6, "accessibility" : True}, "T": { "distance": 295, "time" : 1, "accessibility" : True}},
        "NPS" : {"GC": { "distance": 528, "time" : 3, "accessibility" : True}, "CPAC": { "distance": 1056, "time" : 2, "accessibility" : True}, "VA": { "distance": 1056, "time" : 5, "accessibility" : True}},
        "PL" : {"B": { "distance": 1584, "time" : 6, "accessibility" : True}, "CPAC": { "distance": 1056, "time" : 5, "accessibility" : True}, "EC": { "distance": 384, "time" : 2, "accessibility" : True}, "H": { "distance": 528, "time" : 2, "accessibility" : True}, "KHS": { "distance": 528, "time" : 3, "accessibility" : True}, "SHCC": { "distance": 1056, "time" : 4, "accessibility" : True}},
        "RG" : {"E": { "distance": 528, "time" : 3, "accessibility" : True}, "GAS": { "distance": 528, "time" : 3, "accessibility" : True}, "SHCC": { "distance": 463, "time" : 2, "accessibility" : True}, "RH": { "distance": 528, "time" : 3, "accessibility" : True}},
        "RH" : {"GAS": { "distance": 528, "time" : 2, "accessibility" : True}, "HRE": { "distance": 528, "time" : 2, "accessibility" : True}, "RG": { "distance": 528, "time" : 3, "accessibility" : True}},
        "SCPS" : {"GAH": { "distance": 171, "time" : 1, "accessibility" : True}, "UP": { "distance": 285, "time" : 1, "accessibility" : True}, "SRC": { "distance": 410, "time" : 2, "accessibility" : True}, "TSU": { "distance": 318, "time" : 1, "accessibility" : True}, "CY": { "distance": 1584, "time" : 6, "accessibility" : True}},
        "SGMH" : {"AD": { "distance": 528, "time" : 3, "accessibility" : True}, "MC": { "distance": 1056, "time" : 4, "accessibility" : True}, "CJ": { "distance": 528, "time" : 2, "accessibility" : True}},
        "SHCC" : {"E": { "distance": 295, "time" : 1, "accessibility" : True}, "TG": { "distance": 1056, "time" : 4, "accessibility" : True}, "PL": { "distance": 1056, "time" : 4, "accessibility" : True}, "RG": { "distance": 463, "time" : 2, "accessibility" : True}, "EC": { "distance": 528, "time" : 2, "accessibility" : True}, "T": { "distance": 1056, "time" : 4, "accessibility" : True}},
        "SRC" : {"KHS": { "distance": 528, "time" : 3, "accessibility" : True}, "SCPS": { "distance": 410, "time" : 2, "accessibility" : True}, "TG": { "distance": 207, "time" : 1, "accessibility" : True}, "B": { "distance": 384, "time" : 2, "accessibility" : True}, "TTC": { "distance": 250, "time" : 1, "accessibility" : True}},
        "T" : {"MS": { "distance": 295, "time" : 1, "accessibility" : True}, "SHCC": { "distance": 1056, "time" : 4, "accessibility" : True}, "TG": { "distance": 528, "time" : 3, "accessibility" : True}},
        "TG" : {"KHS": { "distance": 125, "time" : 1, "accessibility" : True}, "SHCC": { "distance": 1056, "time" : 4, "accessibility" : True}, "SRC": { "distance": 207, "time" : 1, "accessibility" : True}, "T": { "distance": 528, "time" : 3, "accessibility" : True}, "TTC": { "distance": 459, "time" : 2, "accessibility" : True}},
        "TH" : {"ASC": { "distance": 528, "time" : 2, "accessibility" : True}, "VA": { "distance": 1056, "time" : 4, "accessibility" : True}, "TSU": { "distance": 528, "time" : 3, "accessibility" : True}},
        "TS" : {"CC": { "distance": 1056, "time" : 5, "accessibility" : True}, "GF": { "distance": 1584, "time" : 6, "accessibility" : True}, "TSC": { "distance": 466, "time" : 2, "accessibility" : True},
        "TTF": { "distance": 1056, "time" : 4, "accessibility" : True}, "AF": { "distance": 528, "time" : 2, "accessibility" : True}},
        "TSC" : {"GF": { "distance": 374, "time" : 2, "accessibility" : True}, "TS": { "distance": 466, "time" : 2, "accessibility" : True}, "AF": { "distance": 528, "time" : 3, "accessibility" : True}, "TTF": { "distance": 1056, "time" : 5, "accessibility" : True}, "TSF": { "distance": 262, "time" : 1, "accessibility" : True}},
        "TSF" : {"MS": { "distance": 1584, "time" : 6, "accessibility" : True}, "TSC": { "distance": 262, "time" : 1, "accessibility" : True}, "AF": { "distance": 243, "time" : 1, "accessibility" : True}, "TTF": { "distance": 250, "time" : 1, "accessibility" : True}},
        "TSU" : {"B": { "distance": 1056, "time" : 4, "accessibility" : True}, "GAH": { "distance": 125, "time" : 1, "accessibility" : True}, "SCPS": { "distance": 318, "time" : 1, "accessibility" : True}, "TH": { "distance": 528, "time" : 3, "accessibility" : True}, "VA": { "distance": 1056, "time" : 4, "accessibility" : True}, "CPAC": { "distance": 1056, "time" : 4, "accessibility" : True}},
        "TTC" : {"TG": { "distance": 459, "time" : 2, "accessibility" : True}, "TTF": { "distance": 1056, "time" : 5, "accessibility" : True}, "SRC": { "distance": 250, "time" : 1, "accessibility" : True}},
        "TTF": {"CC": { "distance": 2112, "time" : 9, "accessibility" : True}, "TS": { "distance": 1056, "time" : 4, "accessibility" : True}, "TSC": { "distance": 1056, "time" : 5, "accessibility" : True}, "TSF": { "distance": 250, "time" : 1, "accessibility" : True}, "TTC": { "distance": 1056, "time" : 5, "accessibility" : True}, "AF": { "distance": 417, "time" : 2, "accessibility" : True}},
        "UP" : {"GAH": { "distance": 463, "time" : 2, "accessibility" : True}, "SCPS": { "distance": 285, "time" : 1, "accessibility" : True}, "CY": { "distance": 2112, "time" : 9, "accessibility" : True}},
        "VA" : {"TH": { "distance": 1056, "time" : 4, "accessibility" : True}, "TSU": { "distance": 1056, "time" : 4, "accessibility" : True}, "CPAC": { "distance": 404, "time" : 2, "accessibility" : True}, "NPS": { "distance": 1056, "time" : 5, "accessibility" : True}},
        "AF" : {"GF": { "distance": 1056, "time" : 5, "accessibility" : True}, "TS": { "distance": 528, "time" : 2, "accessibility" : True}, "TSC": { "distance": 528, "time" : 3, "accessibility" : True}, "TSF": { "distance": 243, "time" : 1, "accessibility" : True}, "TTF": { "distance": 417, "time" : 2, "accessibility" : True}},
        "ASC" : {"TH": { "distance": 528, "time" : 2, "accessibility" : True}},
        "CJ" : {"AD": { "distance": 482, "time" : 2, "accessibility" : True}, "GH": { "distance": 1056, "time" : 3, "accessibility" : True}, "SGMH": { "distance": 528, "time" : 2, "accessibility" : True}, "ESPS":{ "distance": 1056, "time" : 3, "accessibility" : True}, },
        "CY" : {"SCPS":{ "distance": 1584, "time" : 6, "accessibility" : True}, "UP": { "distance": 2112, "time" : 9, "accessibility" : True}},
        }
    return graph

# Implement Dijkstra's algorithm
def dijkstra(graph, source, destination):
    distances = {node: float('inf') for node in graph}
    distances[source] = 0
    priority_queue = [(0, source)]
    previous_nodes = {node: None for node in graph}
    
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        if current_node == destination:
            break
        if current_distance > distances[current_node]:
            continue
        
        for neighbor, attributes in graph[current_node].items():
            weight = attributes["distance"]
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))
    
    path = []
    current = destination
    while current is not None:
        path.append(current)
        current = previous_nodes[current]
    path.reverse()
    
    return distances[destination], path

# Implement Breadth First Search algorithm
def bfs(graph, start, destination):
    queue = deque([[start]]) #Queue for BFS paths to explore
    #set to track visited intersections
    visited = set()
    
    #continue BFS until all the paths a re explored
    while queue:
        path = queue.popleft()
        #Get the current intersection (last node in path)
        current_intersection = path[-1]
        
        #Check if we have reached the destination
        if current_intersection == destination:
            return path
        
        #check if we have reached the destination
        if current_intersection not in visited:
            visited.add(current_intersection)
            
            for neighbor in graph.get(current_intersection, {}):
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)
                
    return None

# Implement Depth First Search algorithm
def dfs(graph, start, destination, path=None, visited=None):
    if path is None:
        path = [start]
    if visited is None:
        visited = set()
        
    visited.add(start)
    
    if start == destination:
        return path
        
    for neighbor in graph.get(start, {}):
        if neighbor not in visited:
            result_path = dfs(graph, neighbor, destination, path + [neighbor], visited)
            if result_path:
                return result_path
    return None

#Define the route for the homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route for finding the path
@app.route('/find_path', methods=['POST'])
def find_path():
    data = request.get_json()  # Use request.get_json() to parse JSON data
    start = data['start']
    end = data['end']
    algorithm = data['algorithm']
    graph = create_graph()

    if algorithm == 'dijkstra':
        _, path = dijkstra(graph, start, end)
    elif algorithm == 'bfs':
        path = bfs(graph, start, end)
    elif algorithm == 'dfs':
        path = dfs(graph, start, end)
    else:
        path = None

    return jsonify({"path": path})

#Run the app
if __name__ == '__main__':
    app.run(debug=True)