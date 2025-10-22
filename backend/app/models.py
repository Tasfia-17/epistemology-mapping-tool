from pydantic import BaseModel, Field
from enum import Enum
from typing import List, Optional
from datetime import datetime


class EpistemologyType(str, Enum):
    EMPIRICAL_QUANTITATIVE = "Empirical-Quantitative"
    ORAL_INTERGENERATIONAL = "Oral-Intergenerational"
    RITUAL_CEREMONIAL = "Ritual-Ceremonial"
    EXPERIENTIAL_PERSONAL = "Experiential-Personal"
    TECHNOLOGICAL_INSTRUMENTAL = "Technological-Instrumental"
    ECOLOGICAL_RELATIONAL = "Ecological-Relational"
    HISTORICAL_DOCUMENTARY = "Historical-Documentary"
    PHILOSOPHICAL_DEDUCTIVE = "Philosophical-Deductive"
    INTUITIVE_INSPIRATIONAL = "Intuitive-Inspirational"
    THEOLOGICAL_DOCTRINAL = "Theological-Doctrinal"
    ARTISTIC_EXPRESSIVE = "Artistic-Expressive"
    LEGAL_PRECEDENTIAL = "Legal-Precedential"


class TextInput(BaseModel):
    text: str = Field(
        ..., 
        min_length=1, 
        max_length=5000
    )


class EpistemologyTag(BaseModel):
    type: EpistemologyType = Field(...)
    confidence: float = Field(..., ge=0.0, le=1.0)
    cue_words: List[str] = Field(default_factory=list)
    explanation: str = Field(...)


class TaggedNode(BaseModel):
    id: str = Field(...)
    text: str = Field(...)
    tags: List[EpistemologyTag] = Field(...)
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    source_type: str = Field(default="text")


class TagResponse(BaseModel):
    success: bool = Field(...)
    node: Optional[TaggedNode] = Field(None)
    error: Optional[str] = Field(None)
    processing_time: float = Field(...)
