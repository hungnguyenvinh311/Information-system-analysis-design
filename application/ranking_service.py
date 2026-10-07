from typing import List, Dict, Tuple, Any

class RankingService:
    """
    Application Layer: RankingService
    Separates candidate generation (Retrieval) from candidate ordering (Ranking).
    Implements:
    - Keyword relevance scoring
    - Cosine similarity ordering
    - Multimodal linear score fusion: S(p|q) = lambda_t * S_t + lambda_i * S_i
    """
    @staticmethod
    def compute_keyword_score(product: Dict[str, Any], tokens: List[str]) -> float:
        """
        Compute weighted keyword match score for a product given query tokens.
        Weights:
        - Product Name: 2.0
        - Category: 1.5
        - Color: 1.0
        - Description: 0.5
        """
        if not tokens:
            return 0.0

        name = product.get("name", "").lower()
        category = product.get("category", "").lower()
        color = product.get("color", "").lower()
        desc = product.get("description", "").lower()

        score = 0.0
        for token in tokens:
            if token in name:
                score += 2.0
            if token in category:
                score += 1.5
            if token in color:
                score += 1.0
            if token in desc:
                score += 0.5

        return round(score, 2)

    def rank_by_keyword(self, candidates: List[Dict[str, Any]], tokens: List[str]) -> List[Tuple[Dict[str, Any], float]]:
        """Rank products by keyword score, descending."""
        scored = []
        for p in candidates:
            score = self.compute_keyword_score(p, tokens)
            if score > 0:
                scored.append((p, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        return scored

    def rank_by_similarity(self, candidates_with_sim: List[Tuple[Dict[str, Any], float]]) -> List[Tuple[Dict[str, Any], float]]:
        """Rank products by visual similarity score, descending."""
        scored = list(candidates_with_sim)
        scored.sort(key=lambda x: x[1], reverse=True)
        return [(p, round(score, 3)) for p, score in scored]

    def rank_multimodal(self, candidates_with_both: List[Tuple[Dict[str, Any], float, float]], lambda_t: float = 0.5, lambda_i: float = 0.5) -> List[Tuple[Dict[str, Any], float]]:
        """
        Combine text score and image score:
        S(p|q) = lambda_t * St + lambda_i * Si
        """
        results = []
        for p, s_text, s_img in candidates_with_both:
            # Normalize text score to [0, 1] range for fair fusion
            norm_text_score = min(1.0, s_text / 4.0)
            combined = (lambda_t * norm_text_score) + (lambda_i * s_img)
            results.append((p, round(combined, 3)))

        results.sort(key=lambda x: x[1], reverse=True)
        return results
