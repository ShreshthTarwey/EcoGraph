from flask import Flask, request, jsonify, render_template
import heapq

app = Flask(__name__)

# ---- Graph Definition for Dijkstra ----
graph = {
    'T1': {'J1': 2.1},
    'J1': {'T1': 2.1, 'J2': 1.8, 'H1': 1.2, 'J4': 3.2},
    'J2': {'J1': 1.8, 'H2': 1.5, 'J3': 2.3, 'J5': 2.7},
    'J3': {'J2': 2.3, 'H3': 1.7, 'J4': 1.9, 'J6': 2.9},
    'J4': {'J3': 1.9, 'H4': 1.4, 'J5': 2.2, 'J1': 3.2, 'J7': 3.1},
    'J5': {'J4': 2.2, 'H5': 1.6, 'J6': 1.8, 'J2': 2.7},
    'J6': {'J5': 1.8, 'H6': 1.3, 'J7': 2.4, 'J3': 2.9},
    'J7': {'J6': 2.4, 'B1': 1.1, 'B2': 1.5, 'J8': 1.7, 'J4': 3.1},
    'J8': {'J7': 1.7, 'B3': 1.2, 'B4': 1.8, 'B5': 1.4, 'B6': 1.9},

    # Homes
    'H1': {'J1': 1.2, 'J2': 2.1},
    'H2': {'J2': 1.5, 'J3': 1.9},
    'H3': {'J3': 1.7, 'J4': 2.2},
    'H4': {'J4': 1.4, 'J5': 1.8},
    'H5': {'J5': 1.6, 'J6': 2.0},
    'H6': {'J6': 1.3, 'J7': 1.6},

    # Bins
    'B1': {'J7': 1.1},
    'B2': {'J7': 1.5},
    'B3': {'J8': 1.2},
    'B4': {'J8': 1.8},
    'B5': {'J8': 1.4},
    'B6': {'J8': 1.9}
}

# ---- Render Frontend ----
def compute_distance(start, end):
    path = run_dijkstra(start, end)
    distance = 0.0
    for i in range(len(path) - 1):
        u, v = path[i], path[i + 1]
        distance += graph[u][v]
    return distance

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/fifo_collect_all_first", methods=["POST"])
def fifo_collect_all_first():
    data = request.json
    queue = data.get("queue")

    if not queue or len(queue) == 0:
        return jsonify({"error": "Queue is empty"}), 400

    full_path = []
    current_node = "T1"
    collected = []

    # Phase 1: Collect from all homes
    for item in queue:
        home = item.get("home")
        waste = item.get("waste")
        bin_id = classify_waste(waste)
        collected.append((home, bin_id))

        path_to_home = run_dijkstra(current_node, home)
        if full_path:
            path_to_home = path_to_home[1:]  # remove duplicate
        full_path.extend(path_to_home)
        current_node = home

    # Phase 2: Visit bins
    for _, bin_id in collected:
        path_to_bin = run_dijkstra(current_node, bin_id)
        if full_path:
            path_to_bin = path_to_bin[1:]
        full_path.extend(path_to_bin)
        current_node = bin_id

    return jsonify({"path": full_path})


@app.route("/priority_immediate_dispose", methods=["POST"])

def priority_immediate_dispose():
    data = request.json
    queue = data.get("queue")

    if not queue or len(queue) == 0:
        return jsonify({"error": "Queue is empty"}), 400

    # Sort queue by distance from T1 (simulate priority)
    queue_with_dist = []
    for item in queue:
        home = item.get("home")
        waste = item.get("waste")
        dist = compute_distance("T1", home)
        queue_with_dist.append((dist, home, waste))

    queue_with_dist.sort()  # shortest distance first

    full_path = []
    current_node = "T1"

    for _, home, waste in queue_with_dist:
        bin_id = classify_waste(waste)

        path1 = run_dijkstra(current_node, home)
        path2 = run_dijkstra(home, bin_id)

        if full_path:
            path1 = path1[1:]

        full_path.extend(path1)
        full_path.extend(path2[1:])
        current_node = bin_id

    return jsonify({"path": full_path})



# ---- Route Optimization Based on Queue ----
@app.route("/optimize_and_route", methods=["POST"])
def optimize_and_route():
    data = request.json
    queue = data.get("queue")

    if not queue or len(queue) == 0:
        return jsonify({"error": "Queue is empty"}), 400

    full_path = []
    current_node = "T1"  # Start from truck depot

    for item in queue:
        home = item.get("home")
        waste = item.get("waste")

        bin_id = classify_waste(waste)

        # From current location to home
        path_to_home = run_dijkstra(current_node, home)

        # From home to bin
        path_to_bin = run_dijkstra(home, bin_id)

        if not path_to_home or not path_to_bin:
            return jsonify({"error": f"Route not found for {home} to {bin_id}"}), 500

        # Merge paths while avoiding duplicate node at join
        if full_path:
            path_to_home = path_to_home[1:]
        full_path.extend(path_to_home)

        path_to_bin = path_to_bin[1:]
        full_path.extend(path_to_bin)

        # Next leg starts from current bin
        current_node = bin_id

    return jsonify({
        "path": full_path,
        "message": "Optimized route generated successfully"
    })


# ---- Waste Classifier ----
def classify_waste(waste):
    w = waste.lower()
    if "plastic" in w:
        return "B1"
    elif "organic" in w:
        return "B2"
    elif "paper" in w:
        return "B3"
    elif "metal" in w:
        return "B4"
    elif "glass" in w:
        return "B5"
    elif "electronic" in w or "phone" in w:
        return "B6"
    return "B2"  # Default fallback


# ---- Dijkstra Shortest Path Algorithm ---- for web hosting-----
def run_dijkstra(start, end):
    heap = [(0, start, [])]
    visited = set()

    while heap:
        cost, node, path = heapq.heappop(heap)
        if node in visited:
            continue
        visited.add(node)
        path = path + [node]

        if node == end:
            return path

        for neighbor, weight in graph.get(node, {}).items():
            if neighbor not in visited:
                heapq.heappush(heap, (cost + weight, neighbor, path))

    return []  # No path found

# This part is for offline meachines not for hosted webApp
# import subprocess

# def run_dijkstra(start, end):
#     try:
#         # Run the compiled C++ program with start and end as arguments
#         result = subprocess.run(
#             ["./logic", start, end],      # Command
#             capture_output=True,          # Capture stdout and stderr
#             text=True,                    # Decode as string instead of bytes
#             check=True                    # Raise error if return code != 0
#         )

#         # The output from C++ (stdout)
#         output = result.stdout.strip()

#         # Example C++ output format:
#         # Shortest Path Cost: 10
#         # T1 -> J1 -> J2 -> J5 -> J6 -> J7 -> J8 -> B3

#         lines = output.splitlines()
#         if len(lines) < 2:
#             return []  # Something went wrong

#         path_line = lines[1]  # "T1 -> J1 -> ... -> B3"
#         path = [node.strip() for node in path_line.split("->")]

#         return path

#     except subprocess.CalledProcessError as e:
#         print("Error running C++ program:", e.stderr)
#         return []



# ---- Run App ----
if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=10000)
