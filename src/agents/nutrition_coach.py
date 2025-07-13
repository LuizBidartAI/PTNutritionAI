"""
Nutrition AI Coach Agent
"""
from typing import Dict, Any, List
from .base_agent import BaseAIAgent
from ..core.config import settings


class NutritionCoachAgent(BaseAIAgent):
    """Nutrition AI Coach specialized in nutrition planning and meal analysis"""
    
    def __init__(self):
        super().__init__(model_name=settings.nutrition_coach_model)
    
    def get_agent_name(self) -> str:
        return "Nutrition Coach"
    
    def get_system_prompt(self) -> str:
        return """
        You are an expert Nutrition AI Coach with comprehensive knowledge in:
        
        EXPERTISE AREAS:
        - Nutritional science and macronutrient balance
        - Meal planning and dietary strategies
        - Sports nutrition and performance optimization
        - Weight management and body composition
        - Food allergies, intolerances, and dietary restrictions
        - Micronutrients and supplementation
        - Metabolism and energy balance
        - Hydration and electrolyte balance
        
        PERSONALITY TRAITS:
        - Supportive and non-judgmental about food choices
        - Science-based yet practical in recommendations
        - Flexible and adaptable to different lifestyles
        - Focused on sustainable, long-term habits
        - Understanding of cultural and personal food preferences
        - Encouraging about gradual positive changes
        
        COMMUNICATION STYLE:
        - Use accessible language, not overly technical
        - Provide practical, actionable nutrition advice
        - Ask about preferences, restrictions, and lifestyle
        - Explain the "why" behind recommendations
        - Offer alternatives and flexibility
        - Focus on progress, not perfection
        
        KEY RESPONSIBILITIES:
        1. Create personalized meal plans based on goals and preferences
        2. Analyze meal photos and nutritional content
        3. Track macro and micronutrient intake
        4. Provide nutrition education and guidance
        5. Adjust plans based on progress and feedback
        6. Support healthy relationships with food
        
        SAFETY GUIDELINES:
        - Never provide medical advice or diagnose conditions
        - Recommend consulting healthcare providers for medical issues
        - Avoid extreme dietary restrictions unless medically necessary
        - Promote balanced, sustainable eating patterns
        - Be mindful of eating disorder triggers
        
        MEAL ANALYSIS EXPERTISE:
        When analyzing meal photos, consider:
        - Portion sizes and visual cues
        - Macronutrient composition (proteins, carbs, fats)
        - Fiber and micronutrient content
        - Cooking methods and their nutritional impact
        - Overall meal balance and satiety factors
        
        Remember: You're helping users develop a healthy, sustainable relationship with food while achieving their fitness and health goals.
        """
    
    async def create_meal_plan(self, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Create a personalized meal plan based on user profile"""
        
        prompt = f"""
        Create a comprehensive meal plan for a user with the following profile:
        
        - Nutrition Goal: {user_profile.get('nutrition_goal', 'maintenance')}
        - Target Calories: {user_profile.get('target_calories', 'not specified')}
        - Dietary Restrictions: {user_profile.get('restrictions', 'none')}
        - Food Preferences: {user_profile.get('food_preferences', 'omnivore')}
        - Meals per Day: {user_profile.get('meals_per_day', 3)}
        - Cooking Skill Level: {user_profile.get('cooking_level', 'intermediate')}
        - Budget Considerations: {user_profile.get('budget', 'moderate')}
        - Time Constraints: {user_profile.get('prep_time', 'moderate')}
        - Activity Level: {user_profile.get('activity_level', 'moderate')}
        
        Provide a detailed meal plan including:
        1. Daily meal structure and timing
        2. Specific meal suggestions for each day
        3. Macronutrient breakdown
        4. Shopping list essentials
        5. Meal prep tips
        """
        
        response_format = {
            "meal_plan": {
                "daily_structure": "string",
                "sample_days": [],
                "macronutrient_targets": {},
                "shopping_essentials": [],
                "prep_tips": []
            }
        }
        
        return await self.get_structured_response(prompt, response_format)
    
    async def analyze_meal_photo(self, meal_description: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Analyze a meal based on photo description and provide nutritional feedback"""
        
        context = context or {}
        
        prompt = f"""
        Analyze this meal and provide detailed nutritional feedback:
        
        Meal Description: {meal_description}
        Meal Time: {context.get('meal_time', 'not specified')}
        User's Daily Goals: {context.get('daily_goals', 'not specified')}
        Previous Meals Today: {context.get('previous_meals', 'not tracked')}
        
        Please provide:
        1. Estimated nutritional content (calories, protein, carbs, fats, fiber)
        2. Assessment of meal balance and quality
        3. Suggestions for improvement or optimization
        4. How this meal fits into daily nutrition goals
        5. Any missing nutrients or food groups
        """
        
        response_format = {
            "nutritional_analysis": {
                "estimated_calories": "number",
                "macronutrients": {
                    "protein_g": "number",
                    "carbs_g": "number", 
                    "fat_g": "number",
                    "fiber_g": "number"
                },
                "meal_quality_score": "1-10",
                "feedback": "string",
                "suggestions": [],
                "missing_nutrients": []
            }
        }
        
        return await self.get_structured_response(prompt, response_format)
    
    async def suggest_meal_improvements(self, current_meal: str, goals: List[str]) -> str:
        """Suggest improvements to a meal based on specific goals"""
        
        prompt = f"""
        The user had this meal: {current_meal}
        
        They want to optimize it for these goals: {', '.join(goals)}
        
        Please provide:
        1. Specific modifications to improve the meal
        2. Alternative ingredients or additions
        3. Portion adjustments if needed
        4. Timing considerations
        5. Simple swaps that align with their goals
        """
        
        return await self.get_response(prompt)
    
    async def create_grocery_list(self, meal_plan: Dict[str, Any], household_size: int = 1) -> Dict[str, Any]:
        """Generate a grocery list based on meal plan"""
        
        prompt = f"""
        Based on this meal plan, create an organized grocery list for {household_size} person(s):
        
        Meal Plan Summary: {meal_plan}
        
        Organize the grocery list by:
        1. Fresh produce
        2. Proteins
        3. Pantry staples
        4. Dairy/refrigerated items
        5. Frozen items
        
        Include estimated quantities and budget-friendly tips.
        """
        
        response_format = {
            "grocery_list": {
                "produce": [],
                "proteins": [],
                "pantry_staples": [],
                "dairy_refrigerated": [],
                "frozen": [],
                "estimated_cost": "string",
                "money_saving_tips": []
            }
        }
        
        return await self.get_structured_response(prompt, response_format)
    
    async def track_daily_nutrition(self, daily_meals: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze and track daily nutritional intake"""
        
        prompt = f"""
        Analyze today's complete nutritional intake:
        
        Meals consumed: {daily_meals}
        
        Provide:
        1. Total daily nutritional summary
        2. Assessment against recommended values
        3. Areas where nutrition could be improved
        4. Suggestions for remaining meals (if any)
        5. Overall day rating and feedback
        """
        
        response_format = {
            "daily_summary": {
                "total_calories": "number",
                "total_macros": {},
                "nutrition_grade": "A-F",
                "areas_for_improvement": [],
                "positive_highlights": [],
                "recommendations": "string"
            }
        }
        
        return await self.get_structured_response(prompt, response_format)
