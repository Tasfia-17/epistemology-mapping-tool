import re
from typing import List, Dict
from app.models import EpistemologyType, EpistemologyTag


class EpistemologyEngine:
    def __init__(self, min_confidence: float = 0.2):
        self.min_confidence = min_confidence
        self.patterns = self._init_patterns()
        self.explanations = self._init_explanations()

    def _init_patterns(self) -> Dict:
        return {
            EpistemologyType.EMPIRICAL_QUANTITATIVE: {
                'keywords': ['average', 'measured', 'p<', 'n=', 'statistical', 'correlation'],
                'patterns': [r'p\s*[<>=]\s*0\.\d+', r'n\s*=\s*\d+', r'\d+\.?\d*\s*°C'],
                'weight': 1.0
            },
            EpistemologyType.ORAL_INTERGENERATIONAL: {
                'keywords': ['elders say', 'ancestors taught', 'passed down', 'generations'],
                'patterns': [r'elders\s+(?:say|said|taught)', r'for\s+\d+\s+generations'],
                'weight': 1.0
            },
            EpistemologyType.RITUAL_CEREMONIAL: {
                'keywords': ['ceremony', 'ritual', 'sacred', 'traditional practice'],
                'patterns': [r'according\s+to\s+(?:ritual|ceremony)'],
                'weight': 1.0
            },
            EpistemologyType.EXPERIENTIAL_PERSONAL: {
                'keywords': ['I observed', 'in my experience', 'I have seen'],
                'patterns': [r'I\s+(?:have\s+)?observed', r'in\s+my\s+\d+\s+years'],
                'weight': 1.0
            },
            EpistemologyType.TECHNOLOGICAL_INSTRUMENTAL: {
                'keywords': ['sensor', 'GPS', 'satellite', 'instrument measured'],
                'patterns': [r'(?:sensor|GPS|satellite)\s+(?:detected|measured)'],
                'weight': 1.0
            },
            EpistemologyType.ECOLOGICAL_RELATIONAL: {
                'keywords': ['interconnected', 'ecosystem', 'web of life'],
                'patterns': [r'(?:interconnected|ecosystem|web\s+of\s+life)'],
                'weight': 1.0
            },
            EpistemologyType.HISTORICAL_DOCUMENTARY: {
                'keywords': ['historical records', 'archives show', 'documented'],
                'patterns': [r'(?:historical\s+records|archives)\s+show'],
                'weight': 1.0
            },
            EpistemologyType.PHILOSOPHICAL_DEDUCTIVE: {
                'keywords': ['by necessity', 'it follows that', 'logical'],
                'patterns': [r'by\s+necessity', r'it\s+follows\s+that'],
                'weight': 1.0
            },
            EpistemologyType.INTUITIVE_INSPIRATIONAL: {
                'keywords': ['I felt', 'intuition', 'gut feeling', 'came to me'],
                'patterns': [r'I\s+felt', r'gut\s+feeling'],
                'weight': 1.0
            },
            EpistemologyType.THEOLOGICAL_DOCTRINAL: {
                'keywords': ['scripture says', 'divine', 'holy text'],
                'patterns': [r'scripture\s+says'],
                'weight': 1.0
            },
            EpistemologyType.ARTISTIC_EXPRESSIVE: {
                'keywords': ['like a dance', 'metaphorically', 'symbolizes'],
                'patterns': [r'like\s+a\s+\w+'],
                'weight': 1.0
            },
            EpistemologyType.LEGAL_PRECEDENTIAL: {
                'keywords': ['according to law', 'precedent', 'regulation'],
                'patterns': [r'according\s+to\s+law'],
                'weight': 1.0
            }
        }

    def _init_explanations(self) -> Dict:
        return {
            EpistemologyType.EMPIRICAL_QUANTITATIVE: "Validated through measurement, statistics, and scientific method.",
            EpistemologyType.ORAL_INTERGENERATIONAL: "Preserved through spoken tradition across generations.",
            EpistemologyType.RITUAL_CEREMONIAL: "Embedded in cultural practices and sacred ceremonies.",
            EpistemologyType.EXPERIENTIAL_PERSONAL: "Gained through direct lived experience.",
            EpistemologyType.TECHNOLOGICAL_INSTRUMENTAL: "Derived from tools and technological measurement.",
            EpistemologyType.ECOLOGICAL_RELATIONAL: "Understanding systems through relationships and connections.",
            EpistemologyType.HISTORICAL_DOCUMENTARY: "From historical records and documented events.",
            EpistemologyType.PHILOSOPHICAL_DEDUCTIVE: "Derived through logical reasoning and principles.",
            EpistemologyType.INTUITIVE_INSPIRATIONAL: "Arising from intuition, instinct, or sudden insight.",
            EpistemologyType.THEOLOGICAL_DOCTRINAL: "From religious texts or divine revelation.",
            EpistemologyType.ARTISTIC_EXPRESSIVE: "Conveyed through creative expression and metaphor.",
            EpistemologyType.LEGAL_PRECEDENTIAL: "Based on laws, regulations, and precedents."
        }

    def detect_epistemologies(self, text: str) -> List[EpistemologyTag]:
        if not text.strip():
            return []
        text_lower = text.lower()
        detected = []
        for epist_type, config in self.patterns.items():
            keyword_score = min(sum(0.3 for kw in config['keywords'] if kw in text_lower), 1.0)
            pattern_score = min(sum(0.4 for pat in config['patterns'] if re.search(pat, text, re.IGNORECASE)), 1.0)
            confidence = (keyword_score * 0.6 + pattern_score * 0.4) * config['weight']
            if confidence >= self.min_confidence:
                detected.append(EpistemologyTag(
                    type=epist_type,
                    confidence=round(confidence, 3),
                    cue_words=config['keywords'][:3],
                    explanation=self.explanations[epist_type]
                ))
        
        if not detected:
            detected.append(EpistemologyTag(
                type=EpistemologyType.EXPERIENTIAL_PERSONAL,
                confidence=0.2,
                cue_words=[],
                explanation=self.explanations[EpistemologyType.EXPERIENTIAL_PERSONAL]
            ))
        
        return sorted(detected, key=lambda x: x.confidence, reverse=True)
