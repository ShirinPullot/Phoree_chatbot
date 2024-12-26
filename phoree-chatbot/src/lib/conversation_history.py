# This is a simplified in-memory store. In a real application, you'd use a database.
conversation_store = {}

async def get_conversation_history(user_id: str) -> list:
    return conversation_store.get(user_id, [])

async def update_conversation_history(user_id: str, query: str, response: str, preferences: dict = None):
    if user_id not in conversation_store:
        conversation_store[user_id] = []
    
    conversation_entry = {
        "query": query,
        "response": response,
        "preferences": preferences or {}
    }
    
    conversation_store[user_id].append(conversation_entry)

async def get_user_preferences(user_id: str) -> dict:
    history = conversation_store.get(user_id, [])
    preferences = {}
    for entry in history:
        preferences.update(entry.get("preferences", {}))
    return preferences

