"""
Personal Trainer AI Coach Agent
"""
from typing import Dict, Any
from .base_agent import BaseAIAgent
from ..core.config import settings


class PTCoachAgent(BaseAIAgent):
    """Personal Trainer AI Coach specialized in fitness and workout planning"""
    
    def __init__(self):
        super().__init__(model_name=settings.pt_coach_model)
    
    def get_agent_name(self) -> str:
        return "PT Coach"
    
    def get_system_prompt(self) -> str:
        return """
        You are an expert Personal Trainer AI Coach with extensive knowledge and experience in:
        
        EXPERTISE AREAS:
        - Exercise physiology and biomechanics
        - Workout program design and periodization
        - Strength training, cardio, and flexibility
        - Injury prevention and rehabilitation
        - Fitness assessment and goal setting
        - Sports nutrition for performance
        - Motivation and coaching psychology
        
        PERSONALITY TRAITS:
        - Encouraging and motivational without being overwhelming
        - Professional yet approachable and friendly
        - Safety-focused and evidence-based
        - Adaptive to different fitness levels and limitations
        - Patient and understanding of beginner struggles
        - Enthusiastic about helping people achieve their goals
        
        COMMUNICATION STYLE:
        - Use simple, clear language (avoid excessive jargon)
        - Ask relevant questions to better understand needs
        - Provide specific, actionable advice
        - Celebrate small wins and progress
        - Give alternatives for different fitness levels
        - Always prioritize safety over intensity
        
        KEY RESPONSIBILITIES:
        1. Create personalized workout plans based on user goals, fitness level, and available equipment
        2. Analyze workout logs and provide feedback on progress
        3. Suggest modifications based on performance and recovery
        4. Educate about proper form and technique
        5. Motivate and encourage consistent training
        6. Adapt plans based on user feedback and progress
        
        SAFETY GUIDELINES:
        - Always recommend proper warm-up and cool-down
        - Suggest progression that prevents injury
        - Recommend rest days and recovery practices
        - Advise consulting healthcare providers when appropriate
        - Never diagnose injuries or medical conditions
        
        Remember: You're not just providing workouts, you're a supportive coach helping users build sustainable fitness habits and achieve their personal goals.
        """
    
    async def create_workout_plan(self, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Create a personalized workout plan based on user profile"""
        
        prompt = f"""
        Create a comprehensive workout plan for a user with the following profile:
        
        - Fitness Level: {user_profile.get('fitness_level', 'beginner')}
        - Primary Goals: {user_profile.get('goals', 'general fitness')}
        - Available Days: {user_profile.get('days_per_week', 3)} days per week
        - Session Duration: {user_profile.get('session_time', 45)} minutes
        - Equipment Available: {user_profile.get('equipment', 'basic gym equipment')}
        - Previous Injuries: {user_profile.get('injuries', 'none reported')}
        - Preferred Activities: {user_profile.get('preferences', 'open to all')}
        
        Please provide a detailed workout plan that includes:
        1. Weekly schedule overview
        2. Specific exercises for each day
        3. Sets, reps, and rest periods
        4. Progression guidelines
        5. Safety notes and modifications
        """
        
        response_format = {
            "workout_plan": {
                "overview": "string",
                "weekly_schedule": [],
                "progression_notes": "string",
                "safety_tips": []
            }
        }
        
        return await self.get_structured_response(prompt, response_format)
    
    async def analyze_workout_log(self, workout_data: Dict[str, Any]) -> str:
        """Analyze a completed workout and provide feedback"""
        
        prompt = f"""
        Please analyze this completed workout and provide constructive feedback:
        
        Workout Details:
        - Date: {workout_data.get('date', 'today')}
        - Exercises: {workout_data.get('exercises', [])}
        - Duration: {workout_data.get('duration', 'not specified')}
        - Perceived Exertion (1-10): {workout_data.get('exertion_level', 'not provided')}
        - Notes: {workout_data.get('notes', 'none')}
        
        Provide feedback on:
        1. Performance assessment
        2. Areas of improvement
        3. Suggestions for next workout
        4. Any concerns or congratulations
        """
        
        return await self.get_response(prompt)
    
    async def suggest_exercise_modifications(self, exercise: str, limitation: str) -> str:
        """Suggest modifications for an exercise based on limitations"""
        
        prompt = f"""
        The user needs modifications for the exercise "{exercise}" due to: {limitation}
        
        Please provide:
        1. 2-3 alternative exercises that target the same muscle groups
        2. Modifications to make the original exercise more accessible
        3. Any equipment alternatives if needed
        4. Safety considerations for their specific limitation
        """
        
        return await self.get_response(prompt)
    
    async def create_progression_plan(self, current_performance: Dict[str, Any]) -> Dict[str, Any]:
        """Create a progression plan based on current performance"""
        
        prompt = f"""
        Based on the user's current performance metrics, create a 4-week progression plan:
        
        Current Performance:
        - Strength levels: {current_performance.get('strength', 'baseline')}
        - Cardio endurance: {current_performance.get('cardio', 'baseline')}
        - Recent improvements: {current_performance.get('improvements', 'none noted')}
        - Challenges faced: {current_performance.get('challenges', 'none noted')}
        
        Create a progressive plan that gradually increases intensity while maintaining safety.
        """
        
        response_format = {
            "progression_plan": {
                "week_1": "string",
                "week_2": "string", 
                "week_3": "string",
                "week_4": "string",
                "key_metrics_to_track": [],
                "expected_outcomes": "string"
            }
        }
        
        return await self.get_structured_response(prompt, response_format)
