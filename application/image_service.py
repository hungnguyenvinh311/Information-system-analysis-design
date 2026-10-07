import math
from typing import List, Any

class ImageService:
    """
    Application Layer: ImageService
    Responsible for generating standardized visual feature vectors from image inputs.
    In the baseline prototype, normalized feature vectors and preset visual templates are used.
    """
    def __init__(self):
        # 5-dimensional feature prototypes:
        # Dimensions represent: [Footwear, High-Tech, Apparel/Textile, Sporty, Computing/Gadgets]
        self.preset_embeddings = {
            "shoe_image": [0.88, 0.15, 0.12, 0.82, 0.08],
            "sneaker_image": [0.85, 0.18, 0.15, 0.79, 0.10],
            "phone_image": [0.12, 0.92, 0.22, 0.08, 0.88],
            "laptop_image": [0.10, 0.86, 0.29, 0.05, 0.81],
            "headphones_image": [0.18, 0.82, 0.14, 0.16, 0.74],
            "shirt_image": [0.26, 0.06, 0.88, 0.22, 0.06],
            "jacket_image": [0.34, 0.09, 0.94, 0.29, 0.09],
            "bag_image": [0.44, 0.29, 0.39, 0.39, 0.29]
        }

    @staticmethod
    def normalize_vector(vec: List[float]) -> List[float]:
        """Normalize vector to unit length (L2 norm)."""
        norm = math.sqrt(sum(x * x for x in vec))
        if norm == 0:
            return vec
        return [x / norm for x in vec]

    def extract_features(self, image_input: Any) -> List[float]:
        """
        Extract or map image input to a normalized feature vector.
        Supports:
        - Direct vector list (e.g., [0.9, 0.1, ...])
        - Image filename / preset keyword (e.g., 'shoe_image', 'sample_shoe.jpg')
        """
        if isinstance(image_input, (list, tuple)) and len(image_input) > 0:
            return self.normalize_vector(list(map(float, image_input)))

        key = str(image_input).lower().strip()
        for preset_name, vec in self.preset_embeddings.items():
            if preset_name in key:
                return self.normalize_vector(vec)

        # Keyword-based mapping fallback
        if any(w in key for w in ["shoe", "sneaker", "footwear"]):
            return self.normalize_vector(self.preset_embeddings["shoe_image"])
        elif any(w in key for w in ["phone", "smartphone", "iphone", "galaxy"]):
            return self.normalize_vector(self.preset_embeddings["phone_image"])
        elif any(w in key for w in ["laptop", "computer", "dell", "xps"]):
            return self.normalize_vector(self.preset_embeddings["laptop_image"])
        elif any(w in key for w in ["jacket", "shirt", "jeans", "hoodie", "clothes"]):
            return self.normalize_vector(self.preset_embeddings["shirt_image"])
        elif any(w in key for w in ["bag", "briefcase", "accessory"]):
            return self.normalize_vector(self.preset_embeddings["bag_image"])

        # Default balanced feature vector
        return self.normalize_vector([0.5, 0.5, 0.5, 0.5, 0.5])
