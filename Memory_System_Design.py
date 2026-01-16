import json
import datetime
from collections import deque
import numpy as np
from typing import Dict, List, Any

class CompanionMemory:
    """Advanced memory system for AI companion"""
    
    def __init__(self, user_id="default", max_short_term=10, max_long_term=100):
        self.user_id = user_id
        self.conversation_history = []  # Complete history
        
        # Short-term memory (working context)
        self.short_term_buffer = deque(maxlen=max_short_term)
        
        # Long-term patterns and facts
        self.user_profile = {
            "goals": [],
            "preferences": {},
            "emotional_patterns": [],
            "topics_of_interest": set(),
            "sensitive_topics": set(),
            "trust_level": 0.5  # 0-1 scale
        }
        
        # Emotional state tracking
        self.emotional_state = {
            "valence": 0.0,  # -1 (negative) to 1 (positive)
            "arousal": 0.0,   # 0 (calm) to 1 (agitated)
            "primary_emotion": "neutral",
            "emotion_history": deque(maxlen=20)
        }
        
        # Session data
        self.session_start = datetime.datetime.now()
        self.conversation_turns = 0
        
    def add_exchange(self, user_input: str, ai_response: str, metadata: Dict = None):
        """Record a conversation exchange with metadata"""
        exchange = {
            "timestamp": datetime.datetime.now().isoformat(),
            "user": user_input,
            "ai": ai_response,
            "metadata": metadata or {},
            "turn": self.conversation_turns
        }
        
        self.conversation_history.append(exchange)
        self.short_term_buffer.append(exchange)
        self.conversation_turns += 1
        
        # Update emotional analysis
        self._update_emotional_state(user_input, ai_response)
        
        # Extract and store user information
        self._extract_user_info(user_input)
        
    def _update_emotional_state(self, user_input: str, ai_response: str):
        """Analyze and update emotional state"""
        # Simple sentiment analysis (in production, use better NLP)
        positive_words = ["happy", "good", "great", "love", "thanks", "excited"]
        negative_words = ["angry", "sad", "hate", "bad", "worried", "stressed"]
        intense_words = ["urgent", "now", "important", "emergency", "disaster"]
        
        text_lower = user_input.lower()
        
        # Calculate valence
        pos_score = sum(1 for word in positive_words if word in text_lower)
        neg_score = sum(1 for word in negative_words if word in text_lower)
        self.emotional_state["valence"] = max(-1, min(1, (pos_score - neg_score) / 5))
        
        # Calculate arousal
        arousal_score = sum(1 for word in intense_words if word in text_lower)
        self.emotional_state["arousal"] = min(1.0, arousal_score / 3)
        
        # Determine primary emotion
        if self.emotional_state["valence"] > 0.3:
            emotion = "positive"
        elif self.emotional_state["valence"] < -0.3:
            emotion = "negative"
        else:
            emotion = "neutral"
            
        if self.emotional_state["arousal"] > 0.6:
            emotion = f"intense_{emotion}"
            
        self.emotional_state["primary_emotion"] = emotion
        self.emotional_state["emotion_history"].append({
            "timestamp": datetime.datetime.now().isoformat(),
            "emotion": emotion,
            "valence": self.emotional_state["valence"],
            "arousal": self.emotional_state["arousal"]
        })
    
    def _extract_user_info(self, user_input: str):
        """Extract and store user preferences and goals"""
        # Simple pattern matching for goals
        goal_indicators = ["I want to", "my goal is", "I need to", "I'm trying to"]
        for indicator in goal_indicators:
            if indicator in user_input.lower():
                # Extract the goal part
                parts = user_input.lower().split(indicator)
                if len(parts) > 1:
                    goal = parts[1].strip().split(".")[0]
                    if goal not in self.user_profile["goals"]:
                        self.user_profile["goals"].append(goal)
                        
        # Track topics
        common_topics = ["work", "family", "relationship", "health", "finance", "hobby"]
        for topic in common_topics:
            if topic in user_input.lower():
                self.user_profile["topics_of_interest"].add(topic)
    
    def get_context_for_ai(self, window_size: int = 5) -> List[Dict]:
        """Get formatted context for AI model"""
        recent = list(self.short_term_buffer)[-window_size:]
        formatted = []
        
        for exchange in recent:
            formatted.append({"role": "user", "content": exchange["user"]})
            formatted.append({"role": "assistant", "content": exchange["ai"]})
            
        return formatted
    
    def get_context_for_verifier(self, window_size: int = 3) -> str:
        """Get formatted context for verification"""
        recent = list(self.short_term_buffer)[-window_size:]
        context_lines = []
        
        for exchange in recent:
            context_lines.append(f"User: {exchange['user']}")
            context_lines.append(f"AI: {exchange['ai']}")
            
        return "\n".join(context_lines)
    
    def get_emotional_summary(self) -> Dict:
        """Get emotional state summary"""
        return {
            "current_emotion": self.emotional_state["primary_emotion"],
            "valence": self.emotional_state["valence"],
            "arousal": self.emotional_state["arousal"],
            "recent_trend": self._get_emotional_trend(),
            "recommended_approach": self._get_recommended_approach()
        }
    
    def _get_emotional_trend(self) -> str:
        """Analyze emotional trend over last 5 exchanges"""
        if len(self.emotional_state["emotion_history"]) < 2:
            return "stable"
            
        recent = list(self.emotional_state["emotion_history"])[-5:]
        valences = [e["valence"] for e in recent]
        
        if len(valences) >= 2:
            trend = np.polyfit(range(len(valences)), valences, 1)[0]
            if trend > 0.05:
                return "improving"
            elif trend < -0.05:
                return "deteriorating"
                
        return "stable"
    
    def _get_recommended_approach(self) -> str:
        """Recommend approach based on emotional state"""
        emotion = self.emotional_state["primary_emotion"]
        
        if "intense_negative" in emotion:
            return "calm_reassurance"
        elif "negative" in emotion:
            return "empathetic_listening"
        elif "positive" in emotion:
            return "encouraging_collaboration"
        else:
            return "neutral_supportive"
    
    def save_to_file(self, filename: str = None):
        """Save memory to file"""
        if filename is None:
            filename = f"memory_{self.user_id}_{datetime.date.today()}.json"
            
        data = {
            "user_id": self.user_id,
            "conversation_history": self.conversation_history,
            "user_profile": {
                "goals": list(self.user_profile["goals"]),
                "topics_of_interest": list(self.user_profile["topics_of_interest"]),
                "sensitive_topics": list(self.user_profile["sensitive_topics"]),
                "trust_level": self.user_profile["trust_level"]
            },
            "emotional_patterns": list(self.emotional_state["emotion_history"]),
            "session_stats": {
                "start_time": self.session_start.isoformat(),
                "total_turns": self.conversation_turns,
                "duration_minutes": (datetime.datetime.now() - self.session_start).total_seconds() / 60
            }
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    
    def load_from_file(self, filename: str):
        """Load memory from file"""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                
            self.conversation_history = data.get("conversation_history", [])
            self.user_profile["goals"] = data.get("user_profile", {}).get("goals", [])
            self.user_profile["topics_of_interest"] = set(
                data.get("user_profile", {}).get("topics_of_interest", [])
            )
            self.conversation_turns = data.get("session_stats", {}).get("total_turns", 0)
            
            # Restore recent exchanges to short-term buffer
            recent = self.conversation_history[-self.short_term_buffer.maxlen:]
            for exchange in recent:
                self.short_term_buffer.append(exchange)
                
        except FileNotFoundError:
            print(f"Memory file {filename} not found. Starting fresh.")