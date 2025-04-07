from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
import google.generativeai as genai
from config import food_collection, allergy_collection, baby_collection
from security import get_current_active_user

router = APIRouter(tags=["recommendation"])

nutrition_guidelines = """
Guidelines for infant nutrition (6-12 months):
- Breastmilk or formula remains primary nutrition
- Introduce single-ingredient purees first
- Watch for allergic reactions with new foods
- No added salt, sugar, or honey under 1 year
- Age-appropriate portion sizes
- Variety of fruits, vegetables, proteins, grains
- Texture matches developmental stage
- Ensure adequate iron intake
"""

def setup_genai():
    genai.configure(api_key="AIzaSyCXg3hNjnOmJYaVJozUeAfINDZqD-UWfCk")  # Use environment variable in production
    return genai.GenerativeModel('gemini-2.0-flash-thinking-exp-01-21')

def verify_baby_ownership(baby_id: str, user_id: str):
    if not baby_collection.find_one({"_id": ObjectId(baby_id), "parent_id": user_id}):
        raise HTTPException(status_code=404, detail="Baby not found or access denied")
    return True

@router.get("/babies/{baby_id}/diet-recommendation")
async def generate_diet_recommendation(
    baby_id: str,
    current_user: dict = Depends(get_current_active_user)
):
    verify_baby_ownership(baby_id, str(current_user["_id"]))
    
    # Get baby's foods and allergies
    foods = [f["name"] for f in food_collection.find({"baby_id": baby_id})]
    allergens = [a["name"] for a in allergy_collection.find({"baby_id": baby_id})]
    
    prompt = f"""Create a concise one-paragraph baby diet plan using these available foods: {', '.join(foods) or 'none'}.
    Avoid these allergens: {', '.join(allergens) or 'none'}. Follow these guidelines: {nutrition_guidelines}
    Structure as one flowing paragraph mentioning breakfast, lunch, dinner and snacks with portions.
    Example: "For breakfast, offer... For lunch... Include snacks like..."
    Use natural language without bullet points or section headers."""
    
    try:
        response = setup_genai().generate_content(prompt)
        return response.text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Diet plan generation failed: {str(e)}") 