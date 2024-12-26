WORKFLOW_PROMPTS = {
    "GREETING": "Greet the user and ask if they want to buy, sell, or rent a property.",
    "BASIC_DETAILS": "Ask the user about the type of property (apartment, villa, or townhouse) and preferred location.",
    "BUDGET_RANGE": "Ask the user about their budget range.",
    "INSTANT_SUGGESTIONS": "Provide property suggestions based on the user's preferences.",
    "FOLLOW_UP": "Respond to the user's request for photos or viewing, and ask if they want to schedule a viewing.",
    "END_INTERACTION": "Conclude the interaction by scheduling a viewing or offering more assistance."
}

def generate_workflow(conversation_history: list, current_query: str) -> str:
    if not conversation_history and "hello" in current_query.lower():
        return "GREETING"
    
    recent_queries = [item['query'] for item in conversation_history[-5:]]
    recent_queries.append(current_query)

    if any('buy' in query.lower() or 'sell' in query.lower() or 'rent' in query.lower() for query in recent_queries):
        return "BASIC_DETAILS"
    elif any('apartment' in query.lower() or 'villa' in query.lower() or 'townhouse' in query.lower() for query in recent_queries):
        return "BUDGET_RANGE"
    elif any('aed' in query.lower() or 'budget' in query.lower() for query in recent_queries):
        return "INSTANT_SUGGESTIONS"
    elif any('photo' in query.lower() or 'viewing' in query.lower() for query in recent_queries):
        return "FOLLOW_UP"
    else:
        return "END_INTERACTION"

