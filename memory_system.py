# memory_system.py
import json
import datetime
from collections import deque
from typing import Dict
import chromadb
from chromadb.utils import embedding_functions

class CompanionMemoryWithChroma:
    """Enhanced memory with ChromaDB for semantic search."""
    # ... Paste the entire 'CompanionMemoryWithChroma' class code here ...



import chromadb
from chromadb.utils import embedding_functions

class CompanionMemoryWithChroma(CompanionMemory):
    """Enhanced memory with ChromaDB for semantic search."""
    
    def __init__(self, user_id="default", persist_directory="./chroma_memory"):
        super().__init__(user_id)
        # Initialize Chroma client with persistence
        self.chroma_client = chromadb.PersistentClient(path=persist_directory)
        # Use a lightweight local embedding model (sentence-transformers)
        self.embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
        # Create or get a collection for this user's memories
        self.memory_collection = self.chroma_client.get_or_create_collection(
            name=f"memories_{user_id}",
            embedding_function=self.embedding_func
        )
    
    def add_exchange(self, user_input: str, ai_response: str, metadata: Dict = None):
        """Record exchange and also embed the combined text into ChromaDB."""
        super().add_exchange(user_input, ai_response, metadata)
        
        # Combine text for embedding
        combined_text = f"User: {user_input}\nAI: {ai_response}"
        # Generate a unique ID for this memory
        memory_id = f"turn_{self.conversation_turns}"
        
        # Add to ChromaDB with the turn number as metadata for filtering
        self.memory_collection.add(
            documents=[combined_text],
            metadatas=[{"turn": self.conversation_turns, **metadata}] if metadata else [{"turn": self.conversation_turns}],
            ids=[memory_id]
        )
    
    def search_similar_memories(self, query_text: str, n_results: int = 3):
        """Find semantically similar past conversations."""
        results = self.memory_collection.query(
            query_texts=[query_text],
            n_results=n_results,
            # Optional: filter by recent turns, e.g., include={"turn": {"$gt": self.conversation_turns - 50}}
        )
        return results