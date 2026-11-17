"""
cot_planner.py
--------------
Chain-of-Thought (CoT) Structured Reasoning and Goal Decomposition Module.

Responsible for:
1. Parsing natural language user travel goals and extracting core entities & constraints.
2. Formulating structured, user-facing reasoning summaries (explaining WHY each task is needed).
3. Establishing task dependencies and determining optimal execution order.
4. Keeping private raw chain-of-thought non-leaking, surfacing crisp, professional rationales.
"""

import re
from typing import Dict, List, Any
from .models import TravelGoal, ReasoningSummary


class ChainOfThoughtPlanner:
    """
    Implements structured Chain-of-Thought (CoT) reasoning for goal decomposition.
    Analyzes complex travel objectives into ordered subtasks with clear justifications.
    """

    @staticmethod
    def parse_goal(goal_text: str) -> TravelGoal:
        """
        Parses the user's natural language goal into a structured TravelGoal dataclass.
        Extracts destination, duration, party size, and budget ceiling.
        """
        # Destination extraction
        dest_match = re.search(r'\bto\s+([A-Za-z]+)', goal_text, re.IGNORECASE) or re.search(r'([A-Za-z]+)\s+trip', goal_text, re.IGNORECASE)
        destination = dest_match.group(1).capitalize() if dest_match else "Goa"

        # Duration extraction (e.g. "2-day", "2 days")
        dur_match = re.search(r'(\d+)[-\s]*(?:day|days)', goal_text, re.IGNORECASE)
        duration_days = int(dur_match.group(1)) if dur_match else 2

        # Party size extraction (e.g. "2 people", "for 2 travelers")
        people_match = re.search(r'(\d+)\s*(?:people|persons|travelers|guests)', goal_text, re.IGNORECASE)
        num_people = int(people_match.group(1)) if people_match else 2

        # Budget extraction (e.g. "₹10,000", "Rs. 10000", "within 10000")
        budget_match = (
            re.search(r'budget\s*(?:of|is|:)?\s*(?:₹|rs\.?|inr)?\s*([\d,]+)', goal_text, re.IGNORECASE) or
            re.search(r'(?:₹|rs\.?|inr)\s*([\d,]+)', goal_text, re.IGNORECASE) or
            re.search(r'within\s*(?:₹|rs\.?|inr)?\s*([\d,]+)', goal_text, re.IGNORECASE)
        )
        if budget_match:
            clean_num = budget_match.group(1).replace(',', '')
            budget_limit = float(clean_num) if clean_num.isdigit() else 10000.0
        else:
            budget_limit = 10000.0

        return TravelGoal(
            raw_goal=goal_text.strip(),
            destination=destination,
            duration_days=duration_days,
            num_people=num_people,
            budget_limit=budget_limit,
            categories=["transportation", "accommodation", "food", "sightseeing"]
        )

    @classmethod
    def decompose_goal(cls, goal: TravelGoal) -> ReasoningSummary:
        """
        Applies Chain-of-Thought (CoT) reasoning to decompose the goal into structured,
        ordered subtasks with explicit justifications and dependency mappings.
        """
        constraints = [
            f"Strict Total Budget Ceiling: ₹{goal.budget_limit:,.0f} (Non-negotiable hard ceiling)",
            f"Geographic Target: {goal.destination} (Requires inter-city transit and local mobility)",
            f"Trip Duration: {goal.duration_days} Days / 1 Night (Compact schedule requiring efficient logistics)",
            f"Party Size: {goal.num_people} Persons (All per-person rates must scale by {goal.num_people})",
            "Mandatory Scope: Transportation, Accommodation, Food, and Sightseeing must all be covered"
        ]

        subtasks = [
            {
                "step": "1",
                "task_name": "Calculate Transportation Expenses",
                "tool_action": "calculate_transport",
                "dependency": "None (Foundational Entrypoint)",
                "justification": (
                    f"Transit to and from {goal.destination} constitutes the foundational logistics prerequisite. "
                    f"Round-trip tickets for {goal.num_people} people must be locked in first to establish baseline expenditure "
                    f"and confirm arrival timing before hotel bookings."
                )
            },
            {
                "step": "2",
                "task_name": "Find and Secure Accommodation",
                "tool_action": "search_accommodation",
                "dependency": "Requires confirmed transport arrival dates",
                "justification": (
                    f"Lodging is the primary fixed overhead during the {goal.duration_days}-day stay. "
                    f"Inventory availability in {goal.destination} must be actively verified to secure overnight rest "
                    f"and provide an anchor point for daily sightseeing."
                )
            },
            {
                "step": "3",
                "task_name": "Estimate Food and Dining Expenses",
                "tool_action": "estimate_food_cost",
                "dependency": "Requires duration and party size confirmation",
                "justification": (
                    f"Nutritional sustainment across {goal.duration_days} days for {goal.num_people} people requires allocating "
                    f"a predictable daily per-person meal allowance (breakfast, lunch, dinner)."
                )
            },
            {
                "step": "4",
                "task_name": "Select Sightseeing and Local Commute",
                "tool_action": "select_sightseeing",
                "dependency": "Requires remaining budget after lodging and transport",
                "justification": (
                    f"Local exploration and sightseeing in {goal.destination} completes the leisure experience. "
                    f"Must balance activity fees and internal transit (e.g. scooter rental) with remaining funds."
                )
            },
            {
                "step": "5",
                "task_name": "Calculate Total Trip Budget",
                "tool_action": "calculate_total_budget",
                "dependency": "Requires all component subtasks (1-4) to report costs",
                "justification": (
                    "Synthesizes discrete component costs (transport, lodging, food, sightseeing) into an accurate, "
                    "verifiable total trip sum."
                )
            },
            {
                "step": "6",
                "task_name": "Audit Budget Feasibility & Approve Plan",
                "tool_action": "verify_budget",
                "dependency": "Requires total sum from step 5",
                "justification": (
                    f"Formally audits aggregated total cost against the user's hard limit of ₹{goal.budget_limit:,.0f} "
                    f"to establish mathematical feasibility and approve final release."
                )
            }
        ]

        summary_text = (
            f"Goal decomposed into 6 ordered subtasks for {goal.num_people} travelers to {goal.destination} "
            f"over {goal.duration_days} days with a strict budget cap of ₹{goal.budget_limit:,.0f}. "
            "Sequential dependency pipeline guarantees all prerequisite bookings and financial feasibility constraints are audited."
        )

        return ReasoningSummary(
            goal_summary=summary_text,
            constraints=constraints,
            subtasks=subtasks,
            total_budget_limit=goal.budget_limit
        )

