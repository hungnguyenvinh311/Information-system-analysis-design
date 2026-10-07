import math
from typing import List, Dict, Tuple, Any

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

class VectorIndex:
    """
    Data Layer: VectorIndex
    Responsible for indexing multi-dimensional feature vectors and computing cosine similarities.
    """
    def __init__(self):
        # Maps product_id -> feature vector (list of floats)
        self.index: Dict[str, List[float]] = {}

    def add_vector(self, product_id: str, vector: List[float]):
        """Register a feature vector for a product."""
        self.index[product_id] = vector

    def build_from_products(self, products: List[Dict[str, Any]]):
        """Index all products containing a 'vector' attribute."""
        for p in products:
            if "id" in p and "vector" in p:
                self.add_vector(p["id"], p["vector"])

    @staticmethod
    def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
        """
        Calculate cosine similarity between two vectors:
        sim(a, b) = (a . b) / (||a|| * ||b||)
        """
        if not vec_a or not vec_b or len(vec_a) != len(vec_b):
            return 0.0

        if HAS_NUMPY:
            a = np.array(vec_a, dtype=float)
            b = np.array(vec_b, dtype=float)
            norm_a = np.linalg.norm(a)
            norm_b = np.linalg.norm(b)
            if norm_a == 0 or norm_b == 0:
                return 0.0
            return float(np.dot(a, b) / (norm_a * norm_b))
        else:
            dot_product = sum(x * y for x, y in zip(vec_a, vec_b))
            norm_a = math.sqrt(sum(x * x for x in vec_a))
            norm_b = math.sqrt(sum(y * y for y in vec_b))
            if norm_a == 0 or norm_b == 0:
                return 0.0
            return dot_product / (norm_a * norm_b)

    def search_similar(self, query_vector: List[float], top_k: int = 5) -> List[Tuple[str, float]]:
        """
        Return list of (product_id, similarity_score) sorted by similarity descending.
        """
        scores = []
        for pid, pvec in self.index.items():
            sim = self.cosine_similarity(query_vector, pvec)
            scores.append((pid, sim))
        
        # Sort descending by similarity
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]
