from utils.rag import recommend_recipes, cooking_instructions, required_ingredients

if __name__ == "__main__":
    print("--- 1. Receipts recomendations ---")
    dishes = recommend_recipes(['chicken', 'flour', 'cheese', 'vinegar', 'milk', 'butter'])
    print(dishes)
    print("\n" + "=" * 50 + "\n")

    print("--- 2. Directions 'Mexican Chicken' ---")
    instruction = cooking_instructions("Mexican Chicken")
    print(instruction)
    print("\n" + "=" * 50 + "\n")

    print("--- 3. Ingredients for 'Mexican Chicken' ---")
    ingredients = required_ingredients("Mexican Chicken")
    print(ingredients)