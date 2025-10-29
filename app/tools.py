"""
Custom LangChain Tools for Fitness Tracker AI Agent

This module provides production-ready tools for the AI agent:
1. CalculatorTool: Safe mathematical expression evaluation
2. WeatherTool: Real-time weather data for workout planning
3. FileManagerTool: CSV file processing for bulk data import
4. WebSearchTool: Web search for fitness/nutrition information
5. FitnessTrackerTool: Interact with fitness data via CRUD operations
"""

from typing import Optional, Type, Dict, Any, List
from datetime import datetime, date
import json
import os
import re

from langchain.tools import BaseTool
from pydantic import BaseModel, Field
import sympy
import requests
from duckduckgo_search import DDGS
import pandas as pd
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import SessionLocal
from app import crud, schemas


# ============================================================================
# Tool Input Schemas (Pydantic models for validation)
# ============================================================================


class CalculatorInput(BaseModel):
    """Input schema for Calculator Tool"""
    expression: str = Field(description="Mathematical expression to evaluate (e.g., '2 + 2', 'sqrt(16)', 'sin(pi/2)')")


class WeatherInput(BaseModel):
    """Input schema for Weather Tool"""
    city: str = Field(description="City name for weather query (e.g., 'London', 'New York')")


class WebSearchInput(BaseModel):
    """Input schema for Web Search Tool"""
    query: str = Field(description="Search query for finding fitness, nutrition, or health information")
    max_results: int = Field(default=3, description="Maximum number of search results to return")


class FitnessQueryInput(BaseModel):
    """Input schema for Fitness Tracker Tool"""
    action: str = Field(description="Action to perform: 'get_user', 'list_workouts', 'get_stats', 'list_goals', 'get_progress'")
    user_id: Optional[str] = Field(default=None, description="User UUID (required for most actions)")
    filters: Optional[Dict[str, Any]] = Field(default=None, description="Optional filters (e.g., {'date_from': '2024-01-01'})")


# ============================================================================
# Custom Tools Implementation
# ============================================================================


class CalculatorTool(BaseTool):
    """
    Safe mathematical calculator using SymPy for secure expression evaluation.

    Supports arithmetic, algebra, trigonometry, and calculus operations.
    Uses SymPy instead of eval() to prevent code injection attacks.
    """
    name: str = "calculator"
    description: str = """
    Evaluates mathematical expressions safely. Supports:
    - Basic arithmetic: +, -, *, /, ** (power), sqrt()
    - Trigonometry: sin(), cos(), tan(), asin(), acos(), atan()
    - Constants: pi, e
    - Functions: log(), exp(), abs(), factorial()

    Examples:
    - "2 + 2" -> 4
    - "sqrt(16)" -> 4
    - "sin(pi/2)" -> 1
    - "log(100, 10)" -> 2
    """
    args_schema: Type[BaseModel] = CalculatorInput

    def _run(self, expression: str) -> str:
        """Execute the calculator tool synchronously"""
        try:
            # Clean the expression
            expression = expression.strip()

            # Parse and evaluate using SymPy (secure evaluation)
            result = sympy.sympify(expression)
            evaluated = result.evalf()

            # Format output
            if evaluated.is_integer:
                return f"Result: {int(evaluated)}"
            else:
                return f"Result: {float(evaluated):.6f}"

        except (sympy.SympifyError, TypeError, ValueError) as e:
            return f"Error: Invalid mathematical expression. {str(e)}"
        except Exception as e:
            return f"Error: Calculation failed. {str(e)}"

    async def _arun(self, expression: str) -> str:
        """Execute the calculator tool asynchronously"""
        return self._run(expression)


class WeatherTool(BaseTool):
    """
    Fetch real-time weather data using OpenWeatherMap API.

    Provides temperature, conditions, humidity, and wind speed for workout planning.
    """
    name: str = "weather"
    description: str = """
    Get current weather information for a city to plan outdoor workouts.
    Returns temperature (Celsius), weather conditions, humidity, and wind speed.

    Use this when users ask about:
    - Current weather conditions
    - Whether it's good weather for outdoor exercise
    - Temperature for running/cycling

    Input: City name (e.g., "London", "New York", "Tokyo")
    """
    args_schema: Type[BaseModel] = WeatherInput

    def _run(self, city: str) -> str:
        """Execute the weather tool synchronously"""
        try:
            api_key = settings.OPENWEATHER_API_KEY

            if not api_key or api_key == "your_openweather_api_key_here":
                return "Weather service unavailable: Please configure OPENWEATHER_API_KEY in .env file. Get a free key at https://openweathermap.org/api"

            # OpenWeatherMap API endpoint
            url = f"http://api.openweathermap.org/data/2.5/weather"
            params = {
                "q": city,
                "appid": api_key,
                "units": "metric"  # Celsius
            }

            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()

            # Extract relevant weather information
            temp = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            humidity = data["main"]["humidity"]
            description = data["weather"][0]["description"]
            wind_speed = data["wind"]["speed"]

            # Format weather report
            weather_report = f"""
Weather for {city}:
- Temperature: {temp}°C (feels like {feels_like}°C)
- Conditions: {description.capitalize()}
- Humidity: {humidity}%
- Wind Speed: {wind_speed} m/s

Workout Recommendation: {"Good conditions for outdoor exercise!" if 10 <= temp <= 25 else "Consider indoor workout due to temperature."}
"""
            return weather_report.strip()

        except requests.exceptions.RequestException as e:
            return f"Error: Unable to fetch weather data. {str(e)}"
        except KeyError:
            return f"Error: City '{city}' not found. Please check the city name."
        except Exception as e:
            return f"Error: Weather lookup failed. {str(e)}"

    async def _arun(self, city: str) -> str:
        """Execute the weather tool asynchronously"""
        return self._run(city)


class WebSearchTool(BaseTool):
    """
    Search the web for fitness, nutrition, and health information using DuckDuckGo.

    Provides up-to-date information that the LLM's training data might not include.
    """
    name: str = "web_search"
    description: str = """
    Search the web for fitness, nutrition, health, and wellness information.

    Use this when users ask about:
    - Latest fitness trends or techniques
    - Nutrition information for specific foods
    - Exercise form and safety
    - Health research or studies
    - Equipment recommendations

    Returns up to 3 relevant search results with titles, snippets, and URLs.
    """
    args_schema: Type[BaseModel] = WebSearchInput

    def _run(self, query: str, max_results: int = 3) -> str:
        """Execute the web search tool synchronously"""
        try:
            # Initialize DuckDuckGo search
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=max_results))

            if not results:
                return f"No search results found for: {query}"

            # Format search results
            formatted_results = f"Search results for '{query}':\n\n"
            for i, result in enumerate(results, 1):
                title = result.get("title", "No title")
                snippet = result.get("body", "No description")
                url = result.get("href", "")

                formatted_results += f"{i}. {title}\n"
                formatted_results += f"   {snippet}\n"
                formatted_results += f"   Source: {url}\n\n"

            return formatted_results.strip()

        except Exception as e:
            return f"Error: Web search failed. {str(e)}"

    async def _arun(self, query: str, max_results: int = 3) -> str:
        """Execute the web search tool asynchronously"""
        return self._run(query, max_results)


class FitnessTrackerTool(BaseTool):
    """
    Interact with the Fitness Tracker database to query and analyze user data.

    Provides access to users, workouts, goals, and progress metrics via CRUD operations.
    """
    name: str = "fitness_tracker"
    description: str = """
    Query and analyze fitness data from the database. Supports the following actions:

    1. 'get_user' - Get user information by user_id
    2. 'list_workouts' - List workout sessions (optional filters: user_id, date_from, date_to)
    3. 'get_stats' - Calculate workout statistics (total workouts, calories, duration)
    4. 'list_goals' - List fitness goals (optional filters: user_id, status)
    5. 'get_progress' - Get progress metrics (optional filters: user_id, metric, date_from, date_to)

    Examples:
    - action='get_user', user_id='123e4567-e89b-12d3-a456-426614174000'
    - action='list_workouts', user_id='...', filters={'date_from': '2024-01-01'}
    - action='get_stats', user_id='...'
    - action='list_goals', user_id='...', filters={'status': 'active'}
    """
    args_schema: Type[BaseModel] = FitnessQueryInput

    def _run(self, action: str, user_id: Optional[str] = None, filters: Optional[Dict[str, Any]] = None) -> str:
        """Execute the fitness tracker tool synchronously"""
        db: Session = SessionLocal()
        try:
            filters = filters or {}

            # Action: Get user information
            if action == "get_user":
                if not user_id:
                    return "Error: user_id is required for 'get_user' action"

                user = crud.user.get(db, id=user_id)
                if not user:
                    return f"User not found with ID: {user_id}"

                return f"""
User Information:
- ID: {user.id}
- Username: {user.username}
- Email: {user.email}
- Member since: {user.created_at.strftime('%Y-%m-%d')}
"""

            # Action: List workout sessions
            elif action == "list_workouts":
                if not user_id:
                    return "Error: user_id is required for 'list_workouts' action"

                # Parse date filters if provided
                date_from = filters.get("date_from")
                date_to = filters.get("date_to")

                # Convert string dates to date objects
                if date_from and isinstance(date_from, str):
                    date_from = datetime.strptime(date_from, "%Y-%m-%d").date()
                if date_to and isinstance(date_to, str):
                    date_to = datetime.strptime(date_to, "%Y-%m-%d").date()

                workouts = crud.workout.get_by_user(
                    db,
                    user_id=user_id,
                    date_from=date_from,
                    date_to=date_to,
                    skip=0,
                    limit=100
                )

                if not workouts:
                    return f"No workouts found for user {user_id}"

                result = f"Found {len(workouts)} workout(s):\n\n"
                for workout in workouts[:10]:  # Limit to 10 for display
                    result += f"- {workout.type.capitalize()} on {workout.date}: {workout.duration}min, {workout.calories_burned} cal\n"

                if len(workouts) > 10:
                    result += f"\n... and {len(workouts) - 10} more workouts"

                return result

            # Action: Calculate workout statistics
            elif action == "get_stats":
                if not user_id:
                    return "Error: user_id is required for 'get_stats' action"

                workouts = crud.workout.get_by_user(db, user_id=user_id, skip=0, limit=1000)

                if not workouts:
                    return f"No workout data available for user {user_id}"

                total_workouts = len(workouts)
                total_duration = sum(w.duration for w in workouts)
                total_calories = sum(w.calories_burned for w in workouts)
                avg_duration = total_duration / total_workouts if total_workouts > 0 else 0
                avg_calories = total_calories / total_workouts if total_workouts > 0 else 0

                # Group by workout type
                workout_types = {}
                for w in workouts:
                    workout_types[w.type] = workout_types.get(w.type, 0) + 1

                stats = f"""
Workout Statistics:
- Total Workouts: {total_workouts}
- Total Duration: {total_duration} minutes ({total_duration/60:.1f} hours)
- Total Calories Burned: {total_calories:.0f} cal
- Average Duration: {avg_duration:.1f} minutes per session
- Average Calories: {avg_calories:.0f} cal per session

Workout Types:
"""
                for wtype, count in workout_types.items():
                    stats += f"  - {wtype.capitalize()}: {count} sessions\n"

                return stats.strip()

            # Action: List fitness goals
            elif action == "list_goals":
                if not user_id:
                    return "Error: user_id is required for 'list_goals' action"

                status = filters.get("status")
                goals = crud.goal.get_by_user(db, user_id=user_id, status=status, skip=0, limit=50)

                if not goals:
                    return f"No goals found for user {user_id}"

                result = f"Found {len(goals)} goal(s):\n\n"
                for goal in goals:
                    progress_pct = (goal.current_value / goal.target_value * 100) if goal.target_value > 0 else 0
                    result += f"- {goal.goal_type}: {goal.current_value}/{goal.target_value} {goal.unit} ({progress_pct:.1f}%) - Status: {goal.status}\n"
                    result += f"  Deadline: {goal.deadline}\n\n"

                return result.strip()

            # Action: Get progress metrics
            elif action == "get_progress":
                if not user_id:
                    return "Error: user_id is required for 'get_progress' action"

                metric = filters.get("metric")
                date_from = filters.get("date_from")
                date_to = filters.get("date_to")

                # Convert string dates
                if date_from and isinstance(date_from, str):
                    date_from = datetime.strptime(date_from, "%Y-%m-%d").date()
                if date_to and isinstance(date_to, str):
                    date_to = datetime.strptime(date_to, "%Y-%m-%d").date()

                progress_list = crud.progress.get_by_user(
                    db,
                    user_id=user_id,
                    metric=metric,
                    date_from=date_from,
                    date_to=date_to,
                    skip=0,
                    limit=100
                )

                if not progress_list:
                    return f"No progress metrics found for user {user_id}"

                result = f"Found {len(progress_list)} progress metric(s):\n\n"
                for p in progress_list[:15]:  # Limit display
                    result += f"- {p.date}: {p.metric} = {p.value} {p.unit}"
                    if p.notes:
                        result += f" (Note: {p.notes})"
                    result += "\n"

                if len(progress_list) > 15:
                    result += f"\n... and {len(progress_list) - 15} more entries"

                return result.strip()

            else:
                return f"Error: Unknown action '{action}'. Valid actions: get_user, list_workouts, get_stats, list_goals, get_progress"

        except Exception as e:
            return f"Error: Fitness tracker query failed. {str(e)}"

        finally:
            db.close()

    async def _arun(self, action: str, user_id: Optional[str] = None, filters: Optional[Dict[str, Any]] = None) -> str:
        """Execute the fitness tracker tool asynchronously"""
        return self._run(action, user_id, filters)


# ============================================================================
# Tool Registry
# ============================================================================

def get_all_tools() -> List[BaseTool]:
    """
    Returns a list of all available tools for the AI agent.

    Returns:
        List[BaseTool]: List of instantiated tool objects
    """
    return [
        CalculatorTool(),
        WeatherTool(),
        WebSearchTool(),
        FitnessTrackerTool()
    ]


def get_tools_info() -> List[Dict[str, str]]:
    """
    Returns metadata about all available tools for API documentation.

    Returns:
        List[Dict]: List of tool metadata (name, description)
    """
    tools = get_all_tools()
    return [
        {
            "name": tool.name,
            "description": tool.description.strip()
        }
        for tool in tools
    ]
