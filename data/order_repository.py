import os
import json
from typing import List, Dict, Optional, Any

class OrderRepository:
    """
    Data Layer: OrderRepository
    Responsible for accessing and tracking customer orders.
    """
    def __init__(self, data_path: Optional[str] = None):
        if data_path is None:
            base_dir = os.path.dirname(__file__)
            data_path = os.path.join(base_dir, "orders.json")
        self.data_path = data_path
        self.orders: List[Dict[str, Any]] = self._load_data()

    def _load_data(self) -> List[Dict[str, Any]]:
        if os.path.exists(self.data_path):
            with open(self.data_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def get_all(self) -> List[Dict[str, Any]]:
        return list(self.orders)

    def find_order(self, order_id: str) -> Optional[Dict[str, Any]]:
        """Find an order by order_id (case-insensitive)."""
        target = order_id.strip().upper()
        for order in self.orders:
            if order["order_id"].upper() == target:
                return order
        return None

    def find_by_customer(self, customer_id: str) -> List[Dict[str, Any]]:
        """Find all orders placed by a customer."""
        target = customer_id.strip().upper()
        return [o for o in self.orders if o["customer_id"].upper() == target]
