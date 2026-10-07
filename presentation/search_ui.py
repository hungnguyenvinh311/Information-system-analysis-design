import sys
from typing import Dict, Any, List
from application.query_service import QueryService
from application.search_service import SearchService

class SearchUI:
    """
    Presentation Layer: SearchUI (Terminal / CLI View)
    Responsible for:
    - Capturing user input (text, voice, image selection)
    - Forwarding requests strictly to Application Layer (QueryService, SearchService)
    - Presenting ranked results, processing logs, and scores
    """
    def __init__(self, query_service: QueryService, search_service: SearchService):
        self.query_service = query_service
        self.search_service = search_service

    def display_results(self, response: Dict[str, Any]):
        """Render formatted search output in terminal."""
        mode = response.get("mode", "Search")
        print("\n" + "=" * 70)
        print(f"  MODE: {mode.upper()} SEARCH RESULTS")
        print("=" * 70)

        # Show Processing Pipeline
        print("\n[Processing Pipeline Steps]")
        for step in response.get("processing", []):
            print(f"  -> {step}")

        # Display Order Results
        if mode == "Order":
            order = response.get("order")
            print("\n[Order Lookup Result]")
            if order:
                print(f"  Order ID    : {order['order_id']}")
                print(f"  Customer ID : {order['customer_id']}")
                print(f"  Status      : {order['status']}")
                print(f"  Total Amount: ${order['total']}")
                print(f"  Items       : {', '.join(order.get('items', []))}")
            else:
                print(f"  Order '{response.get('query')}' not found in database.")
            print("-" * 70)
            return

        # Display Product Results
        results = response.get("results", [])
        count = response.get("count", 0)
        print(f"\n[Returned Products (Total: {count})]")
        if not results:
            print("  No matching products found.")
        else:
            header = f"  {'Rank':<5} {'ID':<6} {'Name':<35} {'Category':<12} {'Price':<8} {'Score':<8}"
            print(header)
            print("  " + "-" * 68)
            for idx, (prod, score) in enumerate(results, 1):
                name = prod.get("name", "")
                if len(name) > 33:
                    name = name[:30] + "..."
                row = f"  {idx:<5} {prod.get('id'):<6} {name:<35} {prod.get('category'):<12} ${prod.get('price'):<7.1f} {score:<8}"
                print(row)
        print("=" * 70)

    def handle_text_search(self, text: str):
        query_obj = self.query_service.text_query(text)
        response = self.search_service.search_text(query_obj["query"], query_obj["tokens"])
        self.display_results(response)
        return response

    def handle_voice_search(self, audio_input: str):
        query_obj = self.query_service.voice_query(audio_input)
        response = self.search_service.search_voice(query_obj)
        self.display_results(response)
        return response

    def handle_image_search(self, image_input: Any):
        query_obj = self.query_service.image_query(image_input)
        response = self.search_service.search_image(query_obj)
        self.display_results(response)
        return response

    def handle_order_search(self, order_id: str):
        query_obj = self.query_service.order_query(order_id)
        response = self.search_service.search_order(query_obj["query"])
        self.display_results(response)
        return response

    def run_demonstration_suite(self):
        """Execute the required 3-mode demonstration suite automatically."""
        print("\n" + "#" * 70)
        print("  AUTOMATED MULTIMODAL SEARCH DEMONSTRATION SUITE")
        print("#" * 70)

        # 1. Text Query Demo
        print("\n>>> DEMO 1: TEXT QUERY")
        self.handle_text_search("black running shoes")

        # 2. Voice Query Demo
        print("\n>>> DEMO 2: VOICE QUERY (Simulated Speech Input)")
        self.handle_voice_search("find blue running shoes")

        # 3. Image Query Demo
        print("\n>>> DEMO 3: IMAGE QUERY (Visual Feature Similarity)")
        self.handle_image_search("shoe_image")

        # 4. Order Query Demo
        print("\n>>> DEMO 4: ORDER TRACKING QUERY")
        self.handle_order_search("O001")

        print("\n" + "#" * 70)
        print("  DEMONSTRATION COMPLETED SUCCESSFULLY")
        print("#" * 70)
