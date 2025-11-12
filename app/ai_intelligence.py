"""AI Intelligence Features for Fitness Tracker

This module provides advanced AI capabilities:
1. AI Insights Engine - Analyzes workout data and generates personalized insights
2. Smart Goal Prediction - Predicts goal completion dates and recommends goals
3. Workout Recommendations - Suggests next workout based on history and patterns
"""

from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta, date
from collections import defaultdict, Counter
import statistics
import json

from sqlalchemy.orm import Session
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

from app.core.config import settings
from app import crud


class WorkoutInsight(BaseModel):
    """Schema for a single workout insight"""
    type: str = Field(description="Type of insight: pattern, achievement, recommendation, or warning")
    title: str = Field(description="Short title for the insight")
    message: str = Field(description="Detailed insight message")
    impact: str = Field(description="Impact level: high, medium, or low")
    emoji: str = Field(description="Relevant emoji for the insight")


class InsightsResponse(BaseModel):
    """Schema for AI insights response"""
    insights: List[WorkoutInsight] = Field(description="List of personalized insights")
    summary: str = Field(description="Overall summary of user's fitness journey")
    motivation: str = Field(description="Motivational message based on progress")


class GoalPrediction(BaseModel):
    """Schema for goal prediction"""
    goal_id: str = Field(description="ID of the goal")
    goal_type: str = Field(description="Type of goal")
    current_value: float = Field(description="Current progress value")
    target_value: float = Field(description="Target value")
    predicted_date: str = Field(description="Predicted completion date (YYYY-MM-DD)")
    confidence: str = Field(description="Confidence level: high, medium, or low")
    days_remaining: int = Field(description="Estimated days until completion")
    recommendation: str = Field(description="AI recommendation to achieve goal faster")


class WorkoutRecommendation(BaseModel):
    """Schema for workout recommendation"""
    workout_type: str = Field(description="Recommended workout type")
    duration: int = Field(description="Recommended duration in minutes")
    intensity: str = Field(description="Recommended intensity: low, moderate, or high")
    reasoning: str = Field(description="Why this workout is recommended")
    tips: List[str] = Field(description="Practical tips for the workout")
    alternatives: List[str] = Field(description="Alternative workout options")


class AIIntelligenceService:
    """
    Advanced AI Intelligence Service using OpenAI GPT-4o-mini.

    Provides personalized insights, predictions, and recommendations
    based on user's fitness data and patterns.
    """

    def __init__(self):
        """Initialize the AI Intelligence Service with OpenAI LLM"""
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.7,
            openai_api_key=settings.OPENAI_API_KEY
        )

    def _analyze_workout_patterns(self, workouts: List[Any]) -> Dict[str, Any]:
        """
        Analyze workout patterns to extract meaningful statistics.

        Args:
            workouts: List of workout objects

        Returns:
            Dictionary with workout pattern analysis
        """
        if not workouts:
            return {
                "total_workouts": 0,
                "patterns": {},
                "trends": {}
            }

        # Calculate basic statistics
        total_workouts = len(workouts)
        total_duration = sum(w.duration for w in workouts)
        total_calories = sum(w.calories_burned for w in workouts)

        # Analyze by workout type
        type_counter = Counter(w.type for w in workouts)
        type_stats = {}
        for wtype in type_counter:
            type_workouts = [w for w in workouts if w.type == wtype]
            type_stats[wtype] = {
                "count": len(type_workouts),
                "avg_duration": statistics.mean(w.duration for w in type_workouts),
                "avg_calories": statistics.mean(w.calories_burned for w in type_workouts)
            }

        # Analyze frequency (workouts per week)
        if workouts:
            workout_dates = [w.date for w in workouts]
            date_range = (max(workout_dates) - min(workout_dates)).days or 1
            workouts_per_week = (total_workouts / date_range) * 7 if date_range > 0 else total_workouts
        else:
            workouts_per_week = 0

        # Analyze recency (days since last workout)
        if workouts:
            last_workout_date = max(w.date for w in workouts)
            days_since_last = (date.today() - last_workout_date).days
        else:
            days_since_last = 999

        # Analyze consistency (workout distribution across weeks)
        workout_weeks = defaultdict(int)
        for workout in workouts:
            week_key = workout.date.isocalendar()[:2]  # (year, week)
            workout_weeks[week_key] += 1

        consistency_score = 0
        if workout_weeks:
            weekly_counts = list(workout_weeks.values())
            avg_weekly = statistics.mean(weekly_counts)
            std_dev = statistics.stdev(weekly_counts) if len(weekly_counts) > 1 else 0
            consistency_score = max(0, 100 - (std_dev / avg_weekly * 100)) if avg_weekly > 0 else 0

        # Detect trends (comparing first half vs second half)
        if len(workouts) >= 4:
            mid_point = len(workouts) // 2
            first_half = workouts[:mid_point]
            second_half = workouts[mid_point:]

            first_avg_duration = statistics.mean(w.duration for w in first_half)
            second_avg_duration = statistics.mean(w.duration for w in second_half)
            duration_change = ((second_avg_duration - first_avg_duration) / first_avg_duration * 100) if first_avg_duration > 0 else 0

            first_avg_calories = statistics.mean(w.calories_burned for w in first_half)
            second_avg_calories = statistics.mean(w.calories_burned for w in second_half)
            calories_change = ((second_avg_calories - first_avg_calories) / first_avg_calories * 100) if first_avg_calories > 0 else 0
        else:
            duration_change = 0
            calories_change = 0

        return {
            "total_workouts": total_workouts,
            "total_duration": total_duration,
            "total_calories": total_calories,
            "avg_duration": total_duration / total_workouts if total_workouts > 0 else 0,
            "avg_calories": total_calories / total_workouts if total_workouts > 0 else 0,
            "workouts_per_week": round(workouts_per_week, 1),
            "days_since_last": days_since_last,
            "consistency_score": round(consistency_score, 1),
            "most_common_type": type_counter.most_common(1)[0][0] if type_counter else "none",
            "type_distribution": dict(type_counter),
            "type_stats": type_stats,
            "duration_trend": round(duration_change, 1),
            "calories_trend": round(calories_change, 1)
        }

    async def generate_insights(self, db: Session, user_id: str) -> Dict[str, Any]:
        """
        Generate personalized AI insights for a user.

        Analyzes workout history and generates insights about patterns,
        achievements, areas for improvement, and recommendations.

        Args:
            db: Database session
            user_id: User UUID

        Returns:
            Dictionary with insights, summary, and motivation
        """
        try:
            # Get user's workout data (last 90 days)
            date_from = datetime.now().date() - timedelta(days=90)
            workouts = crud.workout.get_by_user(
                db,
                user_id=user_id,
                date_from=date_from,
                skip=0,
                limit=1000
            )

            # Get user's goals
            goals = crud.goal.get_by_user(db, user_id=user_id, skip=0, limit=50)
            active_goals = [g for g in goals if g.status == "active"]

            # Analyze patterns
            patterns = self._analyze_workout_patterns(workouts)

            # Create prompt for OpenAI
            prompt_template = ChatPromptTemplate.from_messages([
                ("system", """You are an expert fitness analyst and motivational coach.
Analyze the user's workout data and generate personalized, actionable insights.

Your insights should be:
1. Data-driven and specific (use exact numbers)
2. Encouraging yet honest
3. Actionable with clear recommendations
4. Balanced between celebrating achievements and identifying improvements

Generate 4-6 diverse insights covering:
- Patterns and trends in their training
- Achievements and progress milestones
- Areas for improvement or balance
- Specific recommendations for better results
- Warnings about potential issues (overtraining, inconsistency, etc.)

Each insight must have:
- type: "pattern", "achievement", "recommendation", or "warning"
- title: Short, catchy title (max 8 words)
- message: Detailed insight (2-3 sentences)
- impact: "high", "medium", or "low"
- emoji: Single relevant emoji"""),
                ("human", """Analyze this fitness data and generate insights:

WORKOUT STATISTICS (Last 90 days):
- Total Workouts: {total_workouts}
- Average per week: {workouts_per_week}
- Days since last workout: {days_since_last}
- Consistency score: {consistency_score}/100
- Total duration: {total_duration} minutes
- Total calories: {total_calories} cal
- Average duration: {avg_duration:.1f} min per session
- Average calories: {avg_calories:.1f} cal per session

WORKOUT TYPE DISTRIBUTION:
{type_distribution}

TRENDS:
- Duration change: {duration_trend}% (first half vs second half)
- Calories change: {calories_trend}% (first half vs second half)
- Most common workout: {most_common_type}

ACTIVE GOALS:
{active_goals_summary}

Generate comprehensive insights in JSON format with this structure:
{{
  "insights": [
    {{
      "type": "pattern" | "achievement" | "recommendation" | "warning",
      "title": "string",
      "message": "string",
      "impact": "high" | "medium" | "low",
      "emoji": "string"
    }}
  ],
  "summary": "2-3 sentence overall summary of their fitness journey",
  "motivation": "Encouraging message to keep them motivated (2 sentences)"
}}""")
            ])

            # Prepare goals summary
            goals_summary = "\n".join([
                f"- {g.goal_type}: {g.current_value}/{g.target_value} {g.unit} ({g.current_value/g.target_value*100:.0f}%)"
                for g in active_goals[:5]
            ]) if active_goals else "No active goals"

            # Generate insights using OpenAI
            chain = prompt_template | self.llm
            response = await chain.ainvoke({
                "total_workouts": patterns["total_workouts"],
                "workouts_per_week": patterns["workouts_per_week"],
                "days_since_last": patterns["days_since_last"],
                "consistency_score": patterns["consistency_score"],
                "total_duration": patterns["total_duration"],
                "total_calories": patterns["total_calories"],
                "avg_duration": patterns["avg_duration"],
                "avg_calories": patterns["avg_calories"],
                "type_distribution": json.dumps(patterns["type_distribution"], indent=2),
                "duration_trend": patterns["duration_trend"],
                "calories_trend": patterns["calories_trend"],
                "most_common_type": patterns["most_common_type"],
                "active_goals_summary": goals_summary
            })

            # Parse JSON response
            response_text = response.content
            # Extract JSON from markdown code blocks if present
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()

            result = json.loads(response_text)

            # Add raw statistics for frontend display
            result["statistics"] = patterns
            result["success"] = True

            return result

        except Exception as e:
            print(f"Error generating insights: {e}")
            # Return fallback insights
            return {
                "insights": [
                    {
                        "type": "pattern",
                        "title": "Keep Building Your Routine",
                        "message": "Start tracking your workouts to unlock personalized AI insights. The more data you log, the smarter your recommendations become!",
                        "impact": "medium",
                        "emoji": "📊"
                    }
                ],
                "summary": "Begin your fitness journey by logging workouts and setting goals. AI insights will appear as you build your workout history.",
                "motivation": "Every fitness journey starts with a single workout. You've got this!",
                "statistics": self._analyze_workout_patterns([]),
                "success": False,
                "error": str(e)
            }

    async def predict_goal_completion(self, db: Session, user_id: str, goal_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Predict when user will complete their goals using AI analysis.

        Args:
            db: Database session
            user_id: User UUID
            goal_id: Optional specific goal ID to analyze

        Returns:
            List of goal predictions with completion dates
        """
        try:
            # Get goals
            if goal_id:
                goal = crud.goal.get(db, id=goal_id)
                goals = [goal] if goal and goal.user_id == user_id else []
            else:
                goals = crud.goal.get_by_user(db, user_id=user_id, status="active", skip=0, limit=20)

            if not goals:
                return []

            # Get workout history for trend analysis
            date_from = datetime.now().date() - timedelta(days=60)
            workouts = crud.workout.get_by_user(db, user_id=user_id, date_from=date_from, skip=0, limit=500)
            patterns = self._analyze_workout_patterns(workouts)

            predictions = []

            for goal in goals:
                # Calculate progress rate
                progress_pct = (goal.current_value / goal.target_value * 100) if goal.target_value > 0 else 0
                remaining = goal.target_value - goal.current_value

                # Simple linear projection based on workout frequency
                if patterns["workouts_per_week"] > 0 and remaining > 0:
                    # Estimate based on goal type and current pace
                    if goal.goal_type == "total_workouts":
                        weeks_needed = remaining / patterns["workouts_per_week"]
                    elif goal.goal_type == "calories_burned":
                        avg_calories_per_workout = patterns.get("avg_calories", 300)
                        workouts_needed = remaining / avg_calories_per_workout
                        weeks_needed = workouts_needed / patterns["workouts_per_week"]
                    elif goal.goal_type == "total_duration":
                        avg_duration_per_workout = patterns.get("avg_duration", 30)
                        workouts_needed = remaining / avg_duration_per_workout
                        weeks_needed = workouts_needed / patterns["workouts_per_week"]
                    else:
                        # Generic estimation
                        weeks_needed = (remaining / goal.target_value) * 12  # Assume 12 weeks base

                    days_needed = int(weeks_needed * 7)
                    predicted_date = datetime.now().date() + timedelta(days=days_needed)

                    # Determine confidence based on consistency
                    if patterns["consistency_score"] >= 75:
                        confidence = "high"
                    elif patterns["consistency_score"] >= 50:
                        confidence = "medium"
                    else:
                        confidence = "low"
                else:
                    predicted_date = goal.deadline
                    days_needed = (goal.deadline - datetime.now().date()).days if goal.deadline else 90
                    confidence = "low"

                # Generate AI recommendation
                prompt = ChatPromptTemplate.from_messages([
                    ("system", "You are a fitness goal coach. Provide a concise, actionable recommendation (1-2 sentences) to help achieve the goal faster."),
                    ("human", """Goal: {goal_type}
Progress: {current}/{target} {unit} ({progress_pct:.0f}%)
Current pace: {workouts_per_week} workouts/week
Consistency: {consistency_score}/100

Give ONE specific, actionable tip to reach this goal faster:""")
                ])

                chain = prompt | self.llm
                recommendation_response = await chain.ainvoke({
                    "goal_type": goal.goal_type.replace("_", " ").title(),
                    "current": goal.current_value,
                    "target": goal.target_value,
                    "unit": goal.unit,
                    "progress_pct": progress_pct,
                    "workouts_per_week": patterns["workouts_per_week"],
                    "consistency_score": patterns["consistency_score"]
                })

                prediction = {
                    "goal_id": str(goal.id),
                    "goal_type": goal.goal_type,
                    "current_value": goal.current_value,
                    "target_value": goal.target_value,
                    "unit": goal.unit,
                    "progress_percentage": round(progress_pct, 1),
                    "predicted_date": predicted_date.isoformat(),
                    "confidence": confidence,
                    "days_remaining": days_needed,
                    "deadline": goal.deadline.isoformat() if goal.deadline else None,
                    "on_track": predicted_date <= goal.deadline if goal.deadline else True,
                    "recommendation": recommendation_response.content.strip()
                }

                predictions.append(prediction)

            return predictions

        except Exception as e:
            print(f"Error predicting goals: {e}")
            return []

    async def recommend_workout(self, db: Session, user_id: str) -> Dict[str, Any]:
        """
        Generate intelligent workout recommendation based on history and patterns.

        Args:
            db: Database session
            user_id: User UUID

        Returns:
            Dictionary with workout recommendation
        """
        try:
            # Get recent workout history
            date_from = datetime.now().date() - timedelta(days=14)
            recent_workouts = crud.workout.get_by_user(db, user_id=user_id, date_from=date_from, skip=0, limit=100)

            # Get all-time stats for context
            all_workouts = crud.workout.get_by_user(db, user_id=user_id, skip=0, limit=500)
            patterns = self._analyze_workout_patterns(all_workouts)

            # Get active goals
            goals = crud.goal.get_by_user(db, user_id=user_id, status="active", skip=0, limit=10)

            # Analyze recent activity
            recent_types = [w.type for w in recent_workouts[-7:]]  # Last 7 workouts
            type_counter = Counter(recent_types)
            last_workout = recent_workouts[-1] if recent_workouts else None
            last_workout_type = last_workout.type if last_workout else "none"
            days_since_last = patterns["days_since_last"]

            # Create recommendation prompt
            prompt = ChatPromptTemplate.from_messages([
                ("system", """You are an expert personal trainer providing the NEXT workout recommendation.

Consider:
1. Workout variety and balance (avoid overworking same muscle groups)
2. Recovery time needed
3. User's goals and fitness level
4. Progressive overload principles
5. Time since last workout

Provide a specific, detailed recommendation in JSON format."""),
                ("human", """User's Fitness Profile:

RECENT ACTIVITY (Last 7 workouts):
{recent_types}

LAST WORKOUT:
- Type: {last_workout_type}
- Days ago: {days_since_last}

ALL-TIME STATS:
- Most common: {most_common_type}
- Average duration: {avg_duration:.0f} minutes
- Workouts per week: {workouts_per_week}
- Consistency: {consistency_score}/100

ACTIVE GOALS:
{goals_summary}

Recommend the BEST next workout in this JSON format:
{{
  "workout_type": "specific workout type (e.g., 'Upper Body Strength', 'HIIT Cardio', '5K Run')",
  "duration": number (minutes),
  "intensity": "low" | "moderate" | "high",
  "reasoning": "Why this workout NOW (2-3 sentences)",
  "tips": ["tip1", "tip2", "tip3"] (3 specific actionable tips),
  "alternatives": ["alternative1", "alternative2"] (2 alternative options if user can't do main recommendation)
}}""")
            ])

            # Format goals
            goals_text = "\n".join([
                f"- {g.goal_type.replace('_', ' ').title()}: {g.current_value}/{g.target_value} {g.unit}"
                for g in goals[:3]
            ]) if goals else "No active goals set"

            # Generate recommendation
            chain = prompt | self.llm
            response = await chain.ainvoke({
                "recent_types": ", ".join(recent_types) if recent_types else "No recent workouts",
                "last_workout_type": last_workout_type,
                "days_since_last": days_since_last,
                "most_common_type": patterns["most_common_type"],
                "avg_duration": patterns["avg_duration"],
                "workouts_per_week": patterns["workouts_per_week"],
                "consistency_score": patterns["consistency_score"],
                "goals_summary": goals_text
            })

            # Parse response
            response_text = response.content
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()

            recommendation = json.loads(response_text)
            recommendation["success"] = True
            recommendation["generated_at"] = datetime.now().isoformat()

            return recommendation

        except Exception as e:
            print(f"Error generating workout recommendation: {e}")
            return {
                "workout_type": "Moderate Cardio",
                "duration": 30,
                "intensity": "moderate",
                "reasoning": "A balanced cardio session is great for maintaining fitness and can be adapted to your current energy level.",
                "tips": [
                    "Start with a 5-minute warm-up",
                    "Maintain steady breathing throughout",
                    "Cool down with light stretching"
                ],
                "alternatives": ["Brisk Walk", "Light Cycling"],
                "success": False,
                "error": str(e)
            }


# Global instance
_ai_service: Optional[AIIntelligenceService] = None


def get_ai_service() -> AIIntelligenceService:
    """Get or create the global AI Intelligence Service instance"""
    global _ai_service
    if _ai_service is None:
        _ai_service = AIIntelligenceService()
    return _ai_service
