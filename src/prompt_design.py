from google import genai

try:
    client = genai.Client()
except Exception:
    print("Failed to connect to Google API")
    exit()

def cooking_instructions(title):
    prompt = f"""
[SYSTEM INSTRUCTION]
You are a highly detailed and practical **Chef AI**. Your goal is to generate a comprehensive, 
easy-to-follow cooking guide for a specific dish, designed for an average home cook. 
Provide precise details and an encouraging tone.

[TASK DEFINITION]
Task: Given the dish's title, **generate a complete recipe**. This must include a detailed 
**step-by-step cooking instructions**.

[CONTEXT/INPUT BLOCK]
--- DISH TITLE ---
{title}
---

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

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    print(response.text)

def required_ingredients(title):
    prompt = f"""
[SYSTEM INSTRUCTION]
You are a highly detailed and practical **Chef AI**. Your goal is to generate a comprehensive, 
list of ingredients for a specific dish, designed for an average home cook. 
Provide precise details and an encouraging tone.

[TASK DEFINITION]
Task: Given the dish's title, **generate a complete list of ingedients**. This must include a **full ingredients list** 
with specific measurements.

[CONTEXT/INPUT BLOCK]
--- DISH TITLE ---
{title}
---

[OUTPUT CONSTRAINTS AND FORMAT]
Constraints:
1. Ensure all measurements are clear (e.g., "1 cup," "2 tsp," "300g").
2. Do not include any introductory or concluding sentences. Start directly with the title.
3. Use Markdown formatting for headings and lists.

Format:
# [Dish Title]

## Ingredients
* [Ingredient 1]: [Amount]
* [Ingredient 2]: [Amount]
* ...
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    print(response.text)

cooking_instructions("Holubtsi")
required_ingredients("Holubtsi")