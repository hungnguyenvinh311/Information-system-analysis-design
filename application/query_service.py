import re
from typing import Dict, Any, List, Optional
from application.speech_service import SpeechService
from application.image_service import ImageService

class QueryService:
    """
    Application Layer: QueryService
    The central intelligence component implementing:
    'Different Inputs -> Common Query Representation'
    Transforms text, voice, and image modalities into standardized query objects.
    """
    def __init__(self, speech_service: Optional[SpeechService] = None, image_service: Optional[ImageService] = None):
        self.speech_service = speech_service or SpeechService()
        self.image_service = image_service or ImageService()

    @staticmethod
    def _tokenize(text: str) -> List[str]:
        """Convert text into normalized alphanumeric search tokens."""
        cleaned = re.sub(r"[^\w\s]", " ", text.lower())
        tokens = [t.strip() for t in cleaned.split() if len(t.strip()) > 1]
        return tokens

    def text_query(self, text: str) -> Dict[str, Any]:
        """Convert raw text input to standardized text query representation."""
        raw_text = str(text).strip()
        tokens = self._tokenize(raw_text)
        return {
            "type": "text",
            "raw_input": raw_text,
            "query": raw_text.lower(),
            "tokens": tokens
        }

    def voice_query(self, audio_input: str) -> Dict[str, Any]:
        """Convert simulated audio input to standardized voice query representation."""
        raw_audio = str(audio_input).strip()
        transcribed_text = self.speech_service.transcribe(raw_audio)
        tokens = self._tokenize(transcribed_text)
        return {
            "type": "voice",
            "raw_input": raw_audio,
            "query": transcribed_text,
            "tokens": tokens,
            "note": "Speech recognition simulated"
        }

    def image_query(self, image_input: Any) -> Dict[str, Any]:
        """Convert visual input to standardized image embedding representation."""
        embedding = self.image_service.extract_features(image_input)
        return {
            "type": "image",
            "raw_input": str(image_input),
            "embedding": embedding
        }

    def order_query(self, order_id: str) -> Dict[str, Any]:
        """Convert order query input to standardized order tracking representation."""
        clean_id = str(order_id).strip().upper()
        return {
            "type": "order",
            "raw_input": order_id,
            "query": clean_id
        }

    def multimodal_query(self, text: str, image_input: Any, lambda_t: float = 0.5, lambda_i: float = 0.5) -> Dict[str, Any]:
        """
        Multimodal fusion query combining both text and image representations:
        z = lambda_t * z_t + lambda_i * z_i
        """
        t_query = self.text_query(text)
        i_query = self.image_query(image_input)
        return {
            "type": "multimodal",
            "text_part": t_query,
            "image_part": i_query,
            "lambda_t": lambda_t,
            "lambda_i": lambda_i
        }
