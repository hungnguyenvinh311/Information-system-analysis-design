import sys
import argparse
from application.speech_service import SpeechService
from application.image_service import ImageService
from application.query_service import QueryService
from application.ranking_service import RankingService
from application.search_service import SearchService
from data.product_repository import ProductRepository
from data.order_repository import OrderRepository
from data.vector_index import VectorIndex
from presentation.search_ui import SearchUI
from presentation.web_app import create_app

def bootstrap_system():
    """Wire dependencies strictly following the 3-Layer Architecture."""
    # 1. Data Layer
    product_repo = ProductRepository()
    order_repo = OrderRepository()
    vector_index = VectorIndex()

    # 2. Application Layer
    speech_service = SpeechService()
    image_service = ImageService()
    query_service = QueryService(speech_service=speech_service, image_service=image_service)
    ranking_service = RankingService()
    search_service = SearchService(
        product_repo=product_repo,
        order_repo=order_repo,
        vector_index=vector_index,
        ranking_service=ranking_service
    )

    # 3. Presentation Layer
    search_ui = SearchUI(query_service=query_service, search_service=search_service)
    flask_app = create_app(query_service=query_service, search_service=search_service)

    return search_ui, flask_app

def main():
    parser = argparse.ArgumentParser(description="Multimodal E-Commerce Search System (Assignment 06)")
    parser.add_argument("--web", action="store_true", help="Launch the Flask Web User Interface")
    parser.add_argument("--interactive", action="store_true", help="Launch interactive CLI terminal search")
    parser.add_argument("--port", type=int, default=5000, help="Port for web server (default: 5000)")
    args = parser.parse_args()

    search_ui, flask_app = bootstrap_system()

    if args.web:
        print("\n" + "=" * 70)
        print(f"  STARTING MULTIMODAL SEARCH WEB INTERFACE ON http://127.0.0.1:{args.port}")
        print("  Press Ctrl+C to stop the server")
        print("=" * 70 + "\n")
        flask_app.run(host="127.0.0.1", port=args.port, debug=False)
    elif args.interactive:
        print("\n" + "=" * 70)
        print("  INTERACTIVE TERMINAL SEARCH INTERFACE")
        print("=" * 70)
        while True:
            print("\nSelect search mode:")
            print("  1. Text Search (Keyword matching)")
            print("  2. Voice Search (Simulated speech-to-text)")
            print("  3. Image Similarity Search (Visual features)")
            print("  4. Order Lookup (Order tracking)")
            print("  5. Run Automated Demonstration Suite")
            print("  0. Exit")
            choice = input("Enter choice (0-5): ").strip()
            if choice == "0":
                print("Exiting.")
                break
            elif choice == "1":
                q = input("Enter keyword query: ").strip()
                search_ui.handle_text_search(q)
            elif choice == "2":
                q = input("Enter spoken query: ").strip()
                search_ui.handle_voice_search(q)
            elif choice == "3":
                q = input("Enter image preset (shoe_image, phone_image, bag_image): ").strip()
                search_ui.handle_image_search(q)
            elif choice == "4":
                q = input("Enter order ID (e.g. O001): ").strip()
                search_ui.handle_order_search(q)
            elif choice == "5":
                search_ui.run_demonstration_suite()
            else:
                print("Invalid choice, please select 0-5.")
    else:
        # Default execution: run the required demonstration suite
        search_ui.run_demonstration_suite()
        print("\n[TIP] To launch the Web User Interface: run 'python main.py --web'")
        print("[TIP] To launch interactive CLI terminal: run 'python main.py --interactive'\n")

if __name__ == "__main__":
    main()
