import json
import google.generativeai as genai

# Nutrition guidelines provided for baby diet
nutrition_guidelines = """
Guidelines for infant nutrition (6-12 months):
- Breastmilk or formula remains the primary source of nutrition.
- Introduce solid foods gradually, starting with single-ingredient purees.
- Watch for allergic reactions when introducing new foods.
- Avoid added salt, sugar, and honey in foods for babies under 1 year.
- Ensure proper portion sizes appropriate for age.
- Include a variety of fruits, vegetables, proteins, and grains.
- Texture should be appropriate for developmental stage.
- Ensure adequate iron intake through iron-rich foods.
"""

def setup_genai():
    # Assuming you have already set the API key properly in the environment or a secure method
    api_key = "AIzaSyCXg3hNjnOmJYaVJozUeAfINDZqD-UWfCk"  # Replace with your actual API key
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-2.0-flash-thinking-exp-01-21')

def get_available_foods():
    available_foods = ["fish", "eggs", "celery", "milk", "formula milk"]
    return [food.strip() for food in available_foods if food.strip()]

def get_allergens():
    allergens_input = []  # You can modify this as per user input
    if allergens_input:
        return [allergen.strip() for allergen in allergens_input.split(",") if allergen.strip()]
    return []

def generate_diet_plan(model, available_foods, allergens, guidelines):
    prompt = f"""
    You are creating an optimized baby diet plan based on the following guidelines:
    {guidelines}
    
    Available foods: {', '.join(available_foods)}
    Food allergens/restrictions: {', '.join(allergens) if allergens else 'None'}
    
    Create a daily diet plan with breakfast, lunch, dinner, and snacks.
    
    Format your response as a JSON object with this structure:
    {{
        "meals": [
            {{
                "meal_name": "Breakfast",
                "foods": [
                    {{
                        "food_name": "food name",
                        "portion_grams": portion in grams,
                        "calories": estimated calories
                    }}
                ]
            }}
        ]
    }}
    
    Only provide the JSON output with no additional text.
    """
    
    response = model.generate_content(prompt)
    
    try:
        diet_json_text = response.text
        if "```" in diet_json_text:
            diet_json_text = diet_json_text.replace("```json", "").replace("```", "").strip()
        diet_plan = json.loads(diet_json_text)
        return diet_plan
    except json.JSONDecodeError as e:
        return {"error": "Failed to generate a valid diet plan."}

def main():
    model = setup_genai()
    available_foods = get_available_foods()
    allergens = get_allergens()
    diet_plan = generate_diet_plan(model, available_foods, allergens, nutrition_guidelines)
    print("Foods Inputted:")
    print(available_foods)
    print("Allergens:")
    print(allergens)
    print("JSON Diet Plan:")
    print(json.dumps(diet_plan, indent=2))

if __name__ == "__main__":
    main()
