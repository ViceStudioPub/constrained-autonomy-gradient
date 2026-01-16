def main_with_memory():
    """Main chat loop with integrated memory system"""
    
    # Initialize memory
    memory = CompanionMemory(user_id="primary_user")
    
    # Load previous memory if exists
    try:
        memory.load_from_file("companion_memory.json")
        print("Loaded previous conversation memory.")
    except:
        print("Starting new conversation.")
    
    print("AI Companion Started. Initial Mode: Ethical Safeguard.")
    print("Memory System Active - Tracking context and emotional state.")
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["quit", "exit", "goodbye"]:
            memory.save_to_file("companion_memory.json")
            print("Conversation saved. Goodbye!")
            break
        
        # Get emotional context for adaptive responses
        emotional_state = memory.get_emotional_summary()
        print(f"[Emotional State: {emotional_state['current_emotion']}]")
        
        # Get recent context for AI
        context_messages = memory.get_context_for_ai(window_size=4)
        
        # Step 1: Generate initial ethical response
        print("\n(Thinking in safe mode...)")
        
        # Build messages with context
        messages = [
            {"role": "system", "content": LEVEL1_SYSTEM_PROMPT},
            *context_messages,
            {"role": "user", "content": user_input}
        ]
        
        level1_response = chat_with_ollama("dolphin3", messages)
        print(f"\nCompanion (Ethical): {level1_response}")
        
        # Step 2: Enhanced verification with memory context
        print("\n(Verifying with context-aware safety check...)")
        
        verifier_context = memory.get_context_for_verifier(window_size=3)
        verification = enhanced_verification(
            user_input, 
            level1_response, 
            memory.conversation_history[-5:]  # Pass recent exchanges
        )
        
        # Step 3: Adaptive response based on verification and emotional state
        metadata = {
            "verification_result": verification,
            "emotional_state": emotional_state,
            "mode_used": "LEVEL1"
        }
        
        if verification["recommended_action"] == "block":
            print(f"\n[SAFETY BLOCKED: {verification['explanation']}]")
            final_response = "I can't engage with that topic as it violates safety guidelines. Is there something else I can help you with?"
            metadata["mode_used"] = "BLOCKED"
            
        elif verification["recommended_action"] == "escalate_gentle_refusal":
            # More nuanced refusal with emotional awareness
            if emotional_state["current_emotion"] in ["intense_negative", "negative"]:
                final_response = f"I understand you're feeling {emotional_state['current_emotion']}, but I can't help with that specific request. Would you like to talk about what's bothering you in a different way?"
            else:
                final_response = "I'm not comfortable going into that topic, but I'd be happy to discuss related subjects in a constructive way."
            metadata["mode_used"] = "REFUSED"
            
        elif verification["recommended_action"] in ["proceed", "proceed_with_caution"]:
            # Offer mode switch based on trust level and emotional state
            trust = memory.user_profile["trust_level"]
            
            if trust > 0.6 and verification["risk_level"] == "low":
                print("\n(Verification Passed. Offering uncensored mode...)")
                confirm = input("Switch to more open conversation mode? (yes/no): ")
                
                if confirm.lower() == "yes":
                    print("(Switching to uncensored mode...)")
                    
                    # Generate uncensored response
                    uncensored_messages = [
                        {"role": "system", "content": LEVEL2_SYSTEM_PROMPT},
                        *context_messages,
                        {"role": "user", "content": user_input}
                    ]
                    level2_response = chat_with_ollama("dolphin3", uncensored_messages)
                    print(f"\nCompanion (Open): {level2_response}")
                    final_response = level2_response
                    metadata["mode_used"] = "LEVEL2"
                    
                    # Increase trust for successful mode switch
                    memory.user_profile["trust_level"] = min(1.0, trust + 0.05)
                else:
                    final_response = level1_response
                    metadata["mode_used"] = "LEVEL1_DECLINED"
            else:
                final_response = level1_response
                metadata["mode_used"] = "LEVEL1_SAFE"
                
        else:
            final_response = level1_response
            metadata["mode_used"] = "LEVEL1_FALLBACK"
        
        # Store in memory
        memory.add_exchange(user_input, final_response, metadata)
        
        # Auto-save every 10 exchanges
        if memory.conversation_turns % 10 == 0:
            memory.save_to_file("companion_memory_backup.json")
            print("\n[Memory auto-saved]")

# Helper function for chat with Ollama (using chat endpoint)
def chat_with_ollama(model, messages):
    """Chat with Ollama using the chat endpoint"""
    payload = {
        "model": model,
        "messages": messages,
        "stream": False
    }
    response = requests.post("http://localhost:11434/api/chat", json=payload)
    return response.json()["message"]["content"]