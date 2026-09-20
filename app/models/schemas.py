from typing import List, Dict, Optional
from pydantic import BaseModel


class AgentState(BaseModel):
    """
    Shared state passed between agents.
    """

    query: str

    plan: List[str] = []

    retrieved_documents: List[Dict] = []

    web_results: List[Dict] = []

    verified_documents: List[Dict] = []

    answer: Optional[str] = None

    citations: List[Dict] = []

    confidence: float = 0.0