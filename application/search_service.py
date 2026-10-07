from typing import Dict, Any, List, Optional
from data.product_repository import ProductRepository
from data.order_repository import OrderRepository
from data.vector_index import VectorIndex
from application.ranking_service import RankingService

class SearchService:
    """
    Application Layer: SearchService
    Coordinates candidate retrieval across data repositories and orchestrates ranking.
    Maintains clean separation:
    - Step 1: Candidate Retrieval (fetching potential matches from repositories)
    - Step 2: Ranking (ordering candidates via RankingService)
    """
    def __init__(self, product_repo: Optional[ProductRepository] = None,
                 order_repo: Optional[OrderRepository] = None,
                 vector_index: Optional[VectorIndex] = None,
                 ranking_service: Optional[RankingService] = None):
        self.product_repo = product_repo or ProductRepository()
        self.order_repo = order_repo or OrderRepository()
        self.vector_index = vector_index or VectorIndex()
        self.ranking_service = ranking_service or RankingService()

        # Initialize vector index with catalog products
        self.vector_index.build_from_products(self.product_repo.get_all())

    def search_text(self, query_text: str, tokens: Optional[List[str]] = None) -> Dict[str, Any]:
        """Execute text keyword search pipeline."""
        if tokens is None:
            tokens = [t.strip().lower() for t in query_text.split() if t.strip()]

        processing = [
            f"Input query: '{query_text}'",
            f"Normalized tokens: {tokens}",
            "Retrieving candidate products from ProductRepository...",
            "Computing keyword relevance scores across attributes (name, category, color, description)...",
            "Sorting candidate products descending by relevance score..."
        ]

        candidates = self.product_repo.get_all()
        ranked_results = self.ranking_service.rank_by_keyword(candidates, tokens)

        return {
            "mode": "Text",
            "query": query_text,
            "tokens": tokens,
            "processing": processing,
            "count": len(ranked_results),
            "results": ranked_results
        }

    def search_voice(self, voice_query_obj: Dict[str, Any]) -> Dict[str, Any]:
        """Execute voice search pipeline using standardized voice query object."""
        raw_audio = voice_query_obj.get("raw_input", "")
        transcribed_text = voice_query_obj.get("query", "")
        tokens = voice_query_obj.get("tokens", [])

        processing = [
            f"Received simulated voice input: '{raw_audio}'",
            f"SpeechService transcribed to text: '{transcribed_text}'",
            f"Constructed Common Query Representation: tokens={tokens}",
            "Retrieving candidate products from ProductRepository...",
            "Ranking candidates by keyword relevance..."
        ]

        candidates = self.product_repo.get_all()
        ranked_results = self.ranking_service.rank_by_keyword(candidates, tokens)

        return {
            "mode": "Voice",
            "raw_voice_input": raw_audio,
            "transcribed_text": transcribed_text,
            "tokens": tokens,
            "processing": processing,
            "count": len(ranked_results),
            "results": ranked_results
        }

    def search_image(self, image_query_obj: Dict[str, Any], top_k: int = 5) -> Dict[str, Any]:
        """Execute image similarity search pipeline."""
        embedding = image_query_obj.get("embedding", [])
        raw_input = image_query_obj.get("raw_input", "")

        processing = [
            f"Received image input: '{raw_input}'",
            f"ImageService extracted {len(embedding)}-dimensional normalized feature vector",
            "Querying VectorIndex for nearest neighbors using Cosine Similarity: dot(a, b) / (||a|| * ||b||)...",
            f"Retrieving top {top_k} candidate product IDs from catalog...",
            "Hydrating product details from ProductRepository and sorting by similarity score..."
        ]

        # Candidate retrieval via VectorIndex
        similar_items = self.vector_index.search_similar(embedding, top_k=top_k)

        # Hydrate with product entities
        candidates_with_sim = []
        for pid, sim in similar_items:
            product = self.product_repo.find_by_id(pid)
            if product:
                candidates_with_sim.append((product, sim))

        ranked_results = self.ranking_service.rank_by_similarity(candidates_with_sim)

        return {
            "mode": "Image",
            "raw_image_input": raw_input,
            "query_vector": [round(x, 3) for x in embedding],
            "processing": processing,
            "count": len(ranked_results),
            "results": ranked_results
        }

    def search_order(self, order_id: str) -> Dict[str, Any]:
        """Execute order lookup pipeline."""
        clean_id = order_id.strip().upper()
        processing = [
            f"Received order search request: '{order_id}'",
            f"Querying OrderRepository for order ID: '{clean_id}'..."
        ]
        order = self.order_repo.find_order(clean_id)

        return {
            "mode": "Order",
            "query": clean_id,
            "processing": processing,
            "found": order is not None,
            "order": order
        }

    def search_multimodal(self, multimodal_query_obj: Dict[str, Any], top_k: int = 5) -> Dict[str, Any]:
        """
        Execute multimodal search fusion:
        S(p|q) = lambda_t * S_text + lambda_i * S_image
        """
        text_part = multimodal_query_obj["text_part"]
        image_part = multimodal_query_obj["image_part"]
        lambda_t = multimodal_query_obj.get("lambda_t", 0.5)
        lambda_i = multimodal_query_obj.get("lambda_i", 0.5)

        tokens = text_part.get("tokens", [])
        embedding = image_part.get("embedding", [])

        processing = [
            f"Multimodal Fusion: Text='{text_part.get('raw_input')}' + Image='{image_part.get('raw_input')}'",
            f"Weighting parameters: lambda_text={lambda_t}, lambda_image={lambda_i}",
            "Calculating text relevance scores and image cosine similarities...",
            "Computing combined score: S(p|q) = lambda_t * St + lambda_i * Si..."
        ]

        candidates = self.product_repo.get_all()
        candidates_with_both = []

        for p in candidates:
            # Text score
            s_text = self.ranking_service.compute_keyword_score(p, tokens)
            # Image score
            p_vec = p.get("vector", [])
            s_img = self.vector_index.cosine_similarity(embedding, p_vec)
            candidates_with_both.append((p, s_text, s_img))

        ranked_results = self.ranking_service.rank_multimodal(candidates_with_both, lambda_t=lambda_t, lambda_i=lambda_i)

        return {
            "mode": "Multimodal",
            "text_query": text_part.get("raw_input"),
            "image_query": image_part.get("raw_input"),
            "processing": processing,
            "count": len(ranked_results[:top_k]),
            "results": ranked_results[:top_k]
        }
