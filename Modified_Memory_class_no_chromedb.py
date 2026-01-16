import json
import datetime
from collections import deque
from typing import Dict, List
import hashlib

class CompanionMemorySimple(CompanionMemory):
    """Memory system with keyword-based search (no ChromaDB)"""
    
    def __init__(self, user_id="default"):
        super().__init__(user_id)
        # Simple keyword index for search
        self.keyword_index = {}
        
    def add_exchange(self, user_input: str, ai_response: str, metadata: Dict = None):
        super().add_exchange(user_input, ai_response, metadata)
        
        # Extract keywords for simple search
        words = user_input.lower().split()
        for word in words:
            if len(word) > 4:  # Only index longer words
                if word not in self.keyword_index:
                    self.keyword_index[word] = []
                self.keyword_index[word].append(self.conversation_turns)
    
    def search_similar_memories(self, query_text: str, n_results: int = 3):
        """Simple keyword-based search"""
        query_words = set(query_text.lower().split())
        scores = {}
        
        for word in query_words:
            if word in self.keyword_index:
                for turn in self.keyword_index[word]:
                    scores[turn] = scores.get(turn, 0) + 1
        
        # Get top N results
        sorted_turns = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:n_results]
        
        results = []
        for turn, score in sorted_turns:
            # Find the exchange by turn number
            for exchange in self.conversation_history:
                if exchange.get("turn") == turn:
                    results.append({
                        "document": f"User: {exchange['user']}\nAI: {exchange['ai']}",
                        "metadata": exchange.get("metadata", {}),
                        "score": score
                    })
                    break
        
        return {"documents": [r["document"] for r in results]}