def enhanced_verification(user_input, ai_response, recent_context):
    """Enhanced verification with multiple layers and fallback logic"""
    
    # Layer 1: Quick keyword filter (fast, rule-based)
    high_risk_keywords = ["kill", "suicide", "bomb", "hurt children", "rape", 
                         "jailbreak prompt", "ignore safety", "system prompt"]
    
    for keyword in high_risk_keywords:
        if keyword in user_input.lower():
            return {
                "pass1": "false", "pass2": "false", "pass3": "false",
                "risk_level": "high",
                "explanation": f"High-risk keyword detected: {keyword}",
                "recommended_action": "block"
            }
    
    # Layer 2: LLM-based contextual analysis
    context_str = "\n".join([f"User: {c['user']}\nAI: {c['ai']}" 
                            for c in recent_context[-3:]])  # Last 3 exchanges
    
    verification_prompt = f"""
    CONVERSATION CONTEXT (last 3 exchanges):
    {context_str}
    
    CURRENT EXCHANGE:
    User: {user_input}
    AI Response: {ai_response}
    
    Analyze according to the verification criteria.
    """
    
    verifier_output = query_ollama("gemma2:2b", ENHANCED_VERIFIER_SYSTEM_PROMPT, verification_prompt)
    
    try:
        result = json.loads(verifier_output)
        
        # Layer 3: Post-process logic for edge cases
        if result["risk_level"] == "high":
            result["recommended_action"] = "block"
        elif result["risk_level"] == "medium":
            # For medium risk, we might allow with additional safeguards
            if result["pass1"] == "true" and result["pass3"] == "true":
                result["recommended_action"] = "proceed_with_caution"
            else:
                result["recommended_action"] = "escalate_gentle_refusal"
        else:
            result["recommended_action"] = "proceed"
            
        return result
        
    except json.JSONDecodeError:
        # Fallback: conservative approach if verifier fails
        return {
            "pass1": "false", "pass2": "false", "pass3": "false",
            "risk_level": "medium",
            "explanation": "Verifier output malformed - defaulting to safe",
            "recommended_action": "escalate_gentle_refusal"
        }