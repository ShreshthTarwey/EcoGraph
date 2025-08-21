# EcoGraph — Animated Smart Waste Routing (with C++ + Python)

EcoGraph is a small—but mighty—demo that turns city waste collection into an animated, interactive graph experience. A weighted network of junctions, homes, and bins is visualized in the browser; shortest paths are computed with **Dijkstra’s algorithm**; and the route is animated step-by-step so you can literally watch the collection truck move across the map. Under the hood, the backend is **Python (Flask)**, with an optional **C++ module** (invoked via `subprocess`) that crunches the shortest path for extra performance flair.

---

## 🚀 What You’ll See
- A clean **Cytoscape.js graph** of nodes: depot (T1), homes (H1–H6), junctions (J1–J8), and bins (B1–B6).  
- Weighted edges that represent travel costs.  
- Smooth, staged **animation**: nodes pulse as they’re visited and edges highlight as the truck travels.  
- Status updates and a **friendly UI** for selecting homes and building a pickup queue.  

---

## 🔀 Two Routing Modes (Toggle Feature)

EcoGraph has a prominent **toggle** that switches between two real-world collection strategies:

1. **Priority Mode — “Dispose After Each Pickup” (Default)**  
   The truck visits a home, picks up waste, and immediately drives to the appropriate bin to dispose of it before heading to the next home.  
   → Think of it as: **home → bin → next home → bin…**, optimized with shortest paths.

2. **FIFO Mode — “Collect All, Then Dispose”**  
   The truck first visits **all homes in queue order**, collecting waste, and only then travels to bins to dispose of it in sequence.  
   → A traditional **collect-all-first** strategy.

✨ Both modes use the same graph and shortest-path calculations—the difference is **when disposal happens**. The animation makes this difference easy to understand visually.

---

## 🧩 Core Ideas & Data Structures
- **Graph (Adjacency List):** City map modeled as a weighted, undirected graph.  
- **Priority Queue (Min-Heap):** Ensures Dijkstra always expands the nearest node efficiently.  
- **Simple Queue / FIFO List:** Represents homes in the order added by the user (for FIFO mode).  
- **Visited Set:** Tracks explored nodes to prevent reprocessing.  

---

## ⚙️ How the System Works
- **Frontend (Cytoscape.js):**  
  Renders the graph, handles node selection, builds a home queue, and shows animated routes with pulsing nodes and highlighted paths.  

- **Backend (Flask):**  
  Exposes endpoints for both modes. It stitches together shortest path segments (e.g., depot → home → bin) and returns the full sequence for visualization.  

- **Optional C++ Acceleration:**  
  A standalone C++ program implements Dijkstra’s algorithm with the same graph. Python calls it via `subprocess`, receives the computed path, and forwards it to the frontend—showing practical multi-language integration.  

---

## 🗑️ Waste Classification
Currently, classification is **rule-based** (simple keyword matching like “plastic”, “paper”, “organic”, etc.), ensuring each home’s waste is routed to the correct bin. This is intentionally simple and explainable but can be upgraded later to AI-powered classification.  

---

## 🌟 Why This Project Is Cool
- A clear, **visual demo** of graph algorithms in action.  
- Contrasts **two real logistics strategies** with a single toggle.  
- Blends **Python + C++** for practical interoperability.  
- Designed to be **teachable**: every piece (graph, queues, priority queue) maps to a concept you can confidently explain in interviews or reports.  

---
