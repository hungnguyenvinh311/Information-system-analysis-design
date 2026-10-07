import re

class SpeechService:
    """
    Application Layer: SpeechService
    Simulates speech recognition and acoustic-to-text transcription.
    Note: Speech recognition is simulated in this prototype baseline as allowed by assignment specification.
    """
    def __init__(self):
        # Conversational filler prefixes commonly spoken by customers
        self.fillers = [
            r"^find\s+",
            r"^search\s+(for\s+)?",
            r"^look\s+for\s+",
            r"^show\s+me\s+",
            r"^can\s+you\s+find\s+",
            r"^i\s+want\s+to\s+buy\s+",
            r"^i\s+need\s+"
        ]

    def transcribe(self, audio_input: str) -> str:
        """
        Simulate Speech-to-Text conversion:
        Takes simulated audio input string, normalizes it, and extracts core search intent.
        """
        if not audio_input:
            return ""
            
        text = str(audio_input).strip().lower()
        
        # Remove common spoken conversational prefixes to extract search keywords
        for pattern in self.fillers:
            text = re.sub(pattern, "", text, flags=re.IGNORECASE)
            
        return text.strip()
