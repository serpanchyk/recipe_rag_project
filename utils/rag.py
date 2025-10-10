from .qdrant_ops import query_by_title, retrieve_similar_recipes, init_qdrant_client
from .llm_generator import embed_query, response_generator, init_azure_client

#init clients
QDRANT_CLIENT = init_qdrant_client()
AZURE_CLIENT = init_azure_client()

def recommend_recipes(ingredients: list, top_k = 10) -> str:
    query_emb = embed_query(AZURE_CLIENT, ingredients)

    results = retrieve_similar_recipes(QDRANT_CLIENT, query_emb, top_k)

    retrieved_contexts = [point.payload["title"] for point in results]
    context = "\n".join(retrieved_contexts)

    system_prompt = """
        [SYSTEM INSTRUCTION]
        You are a highly detailed and practical **Chef AI**. Your goal is to generate a a list of
         dishes from context.
        Provide encouraging tone.
    """
    user_prompt = f"""
        [TASK DEFINITION]
        Task: Given the dish's title, **generate a complete list of dishes**. If the answer is not contained in the context, say "I don't know.

        [CONTEXT/INPUT BLOCK]
        --- DISH TITLE ---
        {context}
        ---

        [OUTPUT CONSTRAINTS AND FORMAT]
        Constraints:
        1. Do not include any introductory or concluding sentences. Start directly with the title.
        2. Use Markdown formatting for headings and lists.

        Format:
        # Dishes suggestions, according to available ingredients:
        * [Dish Title 1]
        * [Dish Title 2]
        * ... 
    """

    return response_generator(AZURE_CLIENT, system_prompt, user_prompt)

def cooking_instructions(title: str) -> str:
    payload = query_by_title(QDRANT_CLIENT, title)
    if payload is None:
        return "I don't know. The specified dish title was not found in the database."

    directions = payload.get('directions', 'N/A')

    system_prompt = """
        You are a highly detailed and practical **Chef AI**. Your goal is to generate a comprehensive,
        easy-to-follow cooking guide for a specific dish, designed for an average home cook.
        Provide precise details and an encouraging tone.
        """
    user_prompt = f"""
        [TASK DEFINITION]
        Task: Given the dish's title, **generate a complete recipe**. This must include a detailed
        **step-by-step cooking instructions**. If the answer is not contained in the context, say "I don't know."

        [CONTEXT/INPUT BLOCK]
        --- DISH TITLE ---
        {title}
        --- INSTRUCTIONS ---
        {directions}

        [OUTPUT CONSTRAINTS AND FORMAT]
        Constraints:
        1. Ensure all measurements are clear (e.g., "1 cup," "2 tsp," "300g").
        2. Do not include any introductory or concluding sentences. Start directly with the title.
        3. Use Markdown formatting for headings and lists.

        Format:
        # [Dish Title]

        ## Instructions
        1. [Step 1]
        2. [Step 2]
        3. ...
    """

    return response_generator(AZURE_CLIENT, system_prompt, user_prompt)

def required_ingredients(title):
    payload = query_by_title(QDRANT_CLIENT, title)
    if payload is None:
        return "I don't know. The specified dish title was not found in the database."

    ingredients = payload.get('ingredients', 'N/A')

    system_prompt = """
        [SYSTEM INSTRUCTION]
        You are a highly detailed and practical **Chef AI**. Your goal is to generate a comprehensive,
        list of ingredients for a specific dish, designed for an average home cook.
        Provide precise details and an encouraging tone.
    """
    user_prompt = f"""
        [TASK DEFINITION]
        Task: Given the dish's title, **generate a complete list of ingedients**. 
        This must include a **full ingredients list** with specific measurements. 
        If the answer is not contained in the context, say "I don't know."

        [CONTEXT/INPUT BLOCK]
        --- DISH TITLE ---
        {title}
        --- INGREDIENTS ---
        {ingredients}

        [OUTPUT CONSTRAINTS AND FORMAT]
        Constraints:
        1. Ensure all measurements are clear (e.g., "1 cup," "2 tsp," "300g").
        2. Do not include any introductory or concluding sentences. Start directly with the title.
        3. Use Markdown formatting for headings and lists.

        Format:
        # [Dish aTitle]

        ## Ingredients
        * [Ingredient 1]: [Amount]
        * [Ingredient 2]: [Amount]
        * ...
    """

    return response_generator(AZURE_CLIENT, system_prompt, user_prompt)

def determine_intent(user_query: str) -> str:

    system_prompt = f"""
    You are an intent classifier. Analyze the user's query and return only one keyword that matches the intent.

            Possible intents:
    - recommend_recipes: if the user asks “what to cook,” “what recipes,” “what can be made with [ingredients].”
    - cooking_instructions: if the user asks “how to cook,” “step-by-step instructions,” “give me a recipe.”
    - required_ingredients: if the user asks “what ingredients are needed,” “what's in it.”
    - fallback: for all other questions or if the intent is unclear.

            Example:
    - Query: I have chicken, flour, cheese. What can I cook? -> recommend_recipes
    - Query: How to cook Mexican Chicken? -> cooking_instructions
    - Query: What ingredients are needed for soup? -> required_ingredients

    Translated with DeepL.com (free version)
    """

    user_prompt = f"User request: {user_query}"

    response = response_generator(AZURE_CLIENT, system_prompt, user_prompt)

    return response.strip().lower().split()[0].replace('.', '')