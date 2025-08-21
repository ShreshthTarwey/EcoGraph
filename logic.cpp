#include <bits/stdc++.h>
using namespace std;

// Graph data (adjacency list)
map<string, vector<pair<string, int>>> graphData;

// Dijkstra's algorithm
vector<string> run_dijkstra(const string& start, const string& target) {
    priority_queue<
        tuple<int, string, vector<string>>, 
        vector<tuple<int, string, vector<string>>>, 
        greater<tuple<int, string, vector<string>>>
    > pq;

    set<string> visited;
    pq.push(make_tuple(0, start, vector<string>()));

    while (!pq.empty()) {
        auto top = pq.top();
        pq.pop();

        int cost = get<0>(top);
        string node = get<1>(top);
        vector<string> path = get<2>(top);

        if (visited.count(node)) continue;
        visited.insert(node);

        path.push_back(node);

        if (node == target) {
            cout << "Shortest Path Cost: " << cost << endl;
            return path;
        }

        for (size_t i = 0; i < graphData[node].size(); i++) {
            string neighbor = graphData[node][i].first;
            int weight = graphData[node][i].second;
            if (!visited.count(neighbor)) {
                pq.push(make_tuple(cost + weight, neighbor, path));
            }
        }
    }

    return {};
}

int main(int argc, char* argv[]) {
    if (argc < 3) {
        cerr << "Usage: " << argv[0] << " start end\n";
        return 1;
    }

    string start = argv[1];
    string end   = argv[2];

    // ---- Graph initialization ----
    graphData = {
        {"T1", {{"J1", 2.1}}},
        {"J1", {{"T1", 2.1}, {"J2", 1.8}, {"H1", 1.2}, {"J4", 3.2}}},
        {"J2", {{"J1", 1.8}, {"H2", 1.5}, {"J3", 2.3}, {"J5", 2.7}}},
        {"J3", {{"J2", 2.3}, {"H3", 1.7}, {"J4", 1.9}, {"J6", 2.9}}},
        {"J4", {{"J3", 1.9}, {"H4", 1.4}, {"J5", 2.2}, {"J1", 3.2}, {"J7", 3.1}}},
        {"J5", {{"J4", 2.2}, {"H5", 1.6}, {"J6", 1.8}, {"J2", 2.7}}},
        {"J6", {{"J5", 1.8}, {"H6", 1.3}, {"J7", 2.4}, {"J3", 2.9}}},
        {"J7", {{"J6", 2.4}, {"B1", 1.1}, {"B2", 1.5}, {"J8", 1.7}, {"J4", 3.1}}},
        {"J8", {{"J7", 1.7}, {"B3", 1.2}, {"B4", 1.8}, {"B5", 1.4}, {"B6", 1.9}}},
        
        // Homes
        {"H1", {{"J1", 1.2}, {"J2", 2.1}}},
        {"H2", {{"J2", 1.5}, {"J3", 1.9}}},
        {"H3", {{"J3", 1.7}, {"J4", 2.2}}},
        {"H4", {{"J4", 1.4}, {"J5", 1.8}}},
        {"H5", {{"J5", 1.6}, {"J6", 2.0}}},
        {"H6", {{"J6", 1.3}, {"J7", 1.6}}},
        
        // Bins
        {"B1", {{"J7", 1.1}}},
        {"B2", {{"J7", 1.5}}},
        {"B3", {{"J8", 1.2}}},
        {"B4", {{"J8", 1.8}}},
        {"B5", {{"J8", 1.4}}},
        {"B6", {{"J8", 1.9}}}
    };

    // Run Dijkstra
    vector<string> path = run_dijkstra(start, end);

    if (path.empty()) {
        cout << "No path found\n";
    } else {
        for (size_t i = 0; i < path.size(); i++) {
            cout << path[i];
            if (i != path.size() - 1) cout << " -> ";
        }
        cout << endl;
    }

    return 0;
}
