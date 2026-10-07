from application.speech_service import SpeechService
from application.image_service import ImageService
from application.query_service import QueryService
from application.ranking_service import RankingService
from application.search_service import SearchService
from data.product_repository import ProductRepository
from data.order_repository import OrderRepository
from data.vector_index import VectorIndex

def run_evaluation():
    # Bootstrap
    product_repo = ProductRepository()
    order_repo = OrderRepository()
    vector_index = VectorIndex()
    speech_service = SpeechService()
    image_service = ImageService()
    query_service = QueryService(speech_service, image_service)
    ranking_service = RankingService()
    search_service = SearchService(product_repo, order_repo, vector_index, ranking_service)

    # Test cases: (query, mode, expected_top1_category_or_id, description)
    test_cases = [
        {"query": "black running shoes", "mode": "Text", "expected": "P001", "desc": "Keyword match exact name/category"},
        {"query": "apple iphone", "mode": "Text", "expected": "P004", "desc": "Brand and product match"},
        {"query": "find blue running shoes", "mode": "Voice", "expected": "P002", "desc": "Spoken query with conversational filler"},
        {"query": "search for dell laptop", "mode": "Voice", "expected": "P006", "desc": "Spoken query for electronics"},
        {"query": "shoe_image", "mode": "Image", "expected": "shoes", "desc": "Visual feature similarity for footwear"},
        {"query": "phone_image", "mode": "Image", "expected": "electronics", "desc": "Visual feature similarity for smartphone"},
        {"query": "O001", "mode": "Order", "expected": "O001", "desc": "Valid order lookup"},
        {"query": "O002", "mode": "Order", "expected": "O002", "desc": "Valid delivered order lookup"},
        {"query": "flying rocket car", "mode": "Text", "expected": "None", "desc": "Negative test: Out-of-catalog query"}
    ]

    total = len(test_cases)
    successful = 0
    records = []

    print("\n" + "=" * 80)
    print("  MULTIMODAL SEARCH SYSTEM EVALUATION BENCHMARK")
    print("=" * 80)
    print(f"{'#':<3} {'Query':<25} {'Mode':<8} {'Top-1 Result':<32} {'Score':<8} {'Success':<8}")
    print("-" * 80)

    for idx, tc in enumerate(test_cases, 1):
        q = tc["query"]
        mode = tc["mode"]
        exp = tc["expected"]
        is_success = False
        top1_name = "None"
        top1_score = "0.0"

        if mode == "Text":
            q_obj = query_service.text_query(q)
            res = search_service.search_text(q_obj["query"], q_obj["tokens"])
            if res["results"]:
                top1_p, score = res["results"][0]
                top1_name = f"{top1_p['id']} - {top1_p['name'][:22]}"
                top1_score = str(score)
                if top1_p["id"] == exp or exp == "None":
                    is_success = (exp != "None")
            else:
                top1_name = "No results"
                if exp == "None":
                    is_success = True

        elif mode == "Voice":
            q_obj = query_service.voice_query(q)
            res = search_service.search_voice(q_obj)
            if res["results"]:
                top1_p, score = res["results"][0]
                top1_name = f"{top1_p['id']} - {top1_p['name'][:22]}"
                top1_score = str(score)
                if top1_p["id"] == exp:
                    is_success = True

        elif mode == "Image":
            q_obj = query_service.image_query(q)
            res = search_service.search_image(q_obj)
            if res["results"]:
                top1_p, score = res["results"][0]
                top1_name = f"{top1_p['id']} - {top1_p['name'][:22]}"
                top1_score = str(score)
                if top1_p.get("category") == exp:
                    is_success = True

        elif mode == "Order":
            q_obj = query_service.order_query(q)
            res = search_service.search_order(q_obj["query"])
            if res["found"]:
                o = res["order"]
                top1_name = f"Order {o['order_id']} ({o['status']})"
                top1_score = "N/A"
                if o["order_id"] == exp:
                    is_success = True

        if is_success:
            successful += 1

        status_str = "Yes" if is_success else "No"
        print(f"{idx:<3} {q:<25} {mode:<8} {top1_name:<32} {top1_score:<8} {status_str:<8}")
        records.append({
            "query": q,
            "mode": mode,
            "top1": top1_name,
            "score": top1_score,
            "success": status_str,
            "desc": tc["desc"]
        })

    success_rate = (successful / total) * 100.0
    print("-" * 80)
    print(f"Summary: Total Queries: {total} | Successful: {successful} | Success Rate: {success_rate:.1f}%")
    print("=" * 80 + "\n")

    return total, successful, success_rate, records

if __name__ == "__main__":
    run_evaluation()
