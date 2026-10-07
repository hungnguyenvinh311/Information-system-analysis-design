import os
import json
from typing import List, Dict, Optional, Any

class ProductRepository:
    """
    Data Layer: ProductRepository
    Responsible for accessing and querying product catalog data.
    """
    def __init__(self, data_path: Optional[str] = None):
        if data_path is None:
            base_dir = os.path.dirname(__file__)
            data_path = os.path.join(base_dir, "products.json")
        self.data_path = data_path
        self.products: List[Dict[str, Any]] = self._load_data()

    def _load_data(self) -> List[Dict[str, Any]]:
        if os.path.exists(self.data_path):
            with open(self.data_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def get_all(self) -> List[Dict[str, Any]]:
        """Return all products in catalog."""
        return list(self.products)

    def find_by_id(self, product_id: str) -> Optional[Dict[str, Any]]:
        """Find a product by its ID."""
        for p in self.products:
            if p["id"].lower() == product_id.lower():
                return p
        return None

    def find_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Filter products by category."""
        return [p for p in self.products if p.get("category", "").lower() == category.lower()]
