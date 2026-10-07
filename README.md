# Multimodal Product Search System for E-Commerce
## Assignment 06 — Software Architecture & AI-Oriented Prototype

This project implements an AI-oriented multimodal product search system for an e-commerce platform. It demonstrates the complete development cycle from **Requirements Specification** to **UML System Modeling** (Three-Layer Architecture) and an executable **Python Prototype**.

The system unifies product discovery across multiple input modalities:
1. **Keyword Text Search:** Attribute-weighted token matching.
2. **Voice Search (Simulated):** Speech-to-text transcription simulation.
3. **Image Similarity Search:** Normalized visual feature embeddings and Cosine Similarity.
4. **Order Tracking Search:** Real-time order lookup by ID.
5. **Multimodal Fusion:** Weighted score combination ($S(p|q) = \lambda_t S_t + \lambda_i S_i$).

---

## 1. System Requirements

* **Python Version:** Python 3.9 or higher (tested on Python 3.12).
* **Required Libraries:**
  * `numpy` (for fast vector math & cosine similarity)
  * `flask` (optional, for launching the Web UI)

Install dependencies:
```bash
pip install numpy flask
```

---

## 2. Directory Structure

The project strictly follows the **Three-Layer Architecture** (Presentation $\rightarrow$ Application $\rightarrow$ Data):

```
assignment06/
├── main.py                     # Primary entrypoint (CLI demo, interactive, web)
├── evaluate.py                 # Evaluation benchmark script (9 test cases)
├── presentation/               # Presentation Layer
│   ├── __init__.py
│   ├── search_ui.py            # Terminal CLI presentation & formatted tables
│   └── web_app.py              # Flask Web Application controller & REST API
├── application/                # Application / Intelligence Layer
│   ├── __init__.py
│   ├── query_service.py        # Central Unified Query Representation
│   ├── speech_service.py       # Speech-to-Text simulation
│   ├── image_service.py        # Visual feature vector extraction & normalization
│   ├── search_service.py       # Candidate Retrieval
│   └── ranking_service.py      # Candidate Ranking (scores & similarity)
├── data/                       # Data Layer
│   ├── __init__.py
│   ├── product_repository.py   # Product catalog data access
│   ├── order_repository.py     # Order data access
│   ├── vector_index.py         # Vector indexing & Cosine Similarity calculation
│   ├── products.json           # Catalog dataset (12 diverse products)
│   ├── orders.json             # Orders dataset (4 customer orders)
│   └── images/                 # Sample product images for visual search
└── templates/
    └── index.html              # Modern, responsive Web User Interface
```

---

## 3. How to Run the Program

### Mode 1: Automated Demonstration Suite (Default)
Runs all 4 search modes automatically and prints formatted tables with scores:
```bash
python main.py
```

### Mode 2: Interactive Terminal Search
Allows free-form querying via terminal menu:
```bash
python main.py --interactive
```

### Mode 3: Modern Web User Interface
Launches a responsive browser interface on `http://127.0.0.1:5000`:
```bash
python main.py --web
```

### Mode 4: Automated Evaluation Benchmark
Runs 9 test cases and outputs accuracy metrics and success rate:
```bash
python evaluate.py
```

---

## 4. Architectural Principles

1. **Strict 3-Layer Architecture:**
   $$\text{Presentation Layer} \longrightarrow \text{Application Layer} \longrightarrow \text{Data Layer}$$
   Direct access from Presentation to Data is strictly prohibited.
2. **Different Inputs $\longrightarrow$ Common Representation:**
   All modalities are transformed by `QueryService` into a standardized `dict` before hitting retrieval.
3. **Retrieval $\neq$ Ranking:**
   `SearchService` retrieves candidates ($C(q)$) from repositories, while `RankingService` orders them ($Rank(C(q))$).

---

## 5. Prototype Limitations

* Speech-to-text is simulated using pattern-based conversational extraction.
* Visual feature vectors are normalized representations mapped to catalog embeddings rather than computed via an active GPU deep neural network.
* Catalog data is loaded from JSON file stores rather than an enterprise relational/NoSQL cluster.
