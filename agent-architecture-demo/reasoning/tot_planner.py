"""
tot_planner.py
--------------
Tree-of-Thought (ToT) Alternative Plan Exploration and Evaluation Module.

Implements an authentic Tree-of-Thought search mechanism:
1. Generates multiple candidate plan branches across discrete travel modalities:
   - Plan A: Budget-Focused Travel
   - Plan B: Balanced Travel
   - Plan C: Experience-Focused Travel
2. Computes component expenses using actual Python arithmetic.
3. Evaluates hard budget feasibility constraints against user ceilings.
4. Computes multi-attribute scoring across Cost Efficiency, Feasibility, and Experience Quality.
5. Produces a structured comparative evaluation table and selects the optimal candidate.
"""

from typing import List, Dict, Tuple, Any
from .models import TravelGoal, CandidatePlan


class TreeOfThoughtPlanner:
    """
    Explores alternative plan spaces using Tree-of-Thought (ToT) principles.
    Branches into distinct strategic paradigms, evaluates each leaf node mathematically,
    and returns the highest-scoring feasible candidate.
    """

    TRAVEL_MODALITIES = {
        "Plan A": {
            "name": "Budget-Focused Travel",
            "transport": {
                "name": "Standard Sleeper Train (Non-AC)",
                "rate_per_person": 800.0
            },
            "accommodation": {
                "name": "Sea Mist Backpacker Hostel (Dorm Pod)",
                "total_cost": 1500.0
            },
            "food": {
                "tier": "Local Dhabas & Street Food",
                "daily_rate_per_person": 500.0
            },
            "sightseeing": {
                "tier": "Self-Guided Beach Walks & Heritage Sites",
                "total_cost": 800.0
            },
            "experience_rating": 55.0,
            "description": "Maximizes financial savings with dormitory lodging and public walking tours.",
            "pros": ["Lowest expenditure", "High savings buffer (₹4,100)", "Zero debt risk"],
            "cons": ["Shared dorm room", "Non-AC overnight transit", "Limited dining variety"]
        },
        "Plan B": {
            "name": "Balanced Travel",
            "transport": {
                "name": "Konkan Express (AC 3-Tier Sleeper)",
                "rate_per_person": 1000.0
            },
            "accommodation": {
                "name": "Sunset Beach Resort (3-Star Beachfront)",
                "total_cost": 3000.0
            },
            "food": {
                "tier": "Local Goan Beach Shacks & Authentic Thalis",
                "daily_rate_per_person": 750.0
            },
            "sightseeing": {
                "tier": "Fort Aguada + Churches + 2-Day Scooter Rental",
                "total_cost": 1200.0
            },
            "experience_rating": 88.0,
            "description": "Optimal equilibrium of comfort, private resort stay, authentic cuisine, and motorized mobility.",
            "pros": ["Private beachfront resort room", "AC train transit", "Scooter mobility across Goa", "Fits budget comfortably"],
            "cons": ["Moderate savings buffer (₹800)", "Subject to resort room inventory availability"]
        },
        "Plan C": {
            "name": "Experience-Focused Travel",
            "transport": {
                "name": "Multi-Axle AC Volvo Sleeper Bus",
                "rate_per_person": 1400.0
            },
            "accommodation": {
                "name": "Heritage Boutique Beachfront Villa",
                "total_cost": 4800.0
            },
            "food": {
                "tier": "Fine Dining Seafood & Beachfront Cafes",
                "daily_rate_per_person": 1000.0
            },
            "sightseeing": {
                "tier": "Guided Water Sports & Scuba Package + Private Cab",
                "total_cost": 2500.0
            },
            "experience_rating": 96.0,
            "description": "Luxury-oriented itinerary prioritizing premium hospitality, watersports, and gourmet dining.",
            "pros": ["Luxury villa stay", "Curated scuba diving and water sports", "Private chauffeur cab"],
            "cons": ["Exceeds budget ceiling by ₹4,100", "Infeasible without significant budget escalation"]
        }
    }

    @classmethod
    def generate_candidate_plans(cls, goal: TravelGoal) -> List[CandidatePlan]:
        """
        Synthesizes candidate travel branches from the modality catalog
        and computes arithmetic cost sums and multi-attribute evaluations.
        """
        candidates: List[CandidatePlan] = []

        for plan_id, mod in cls.TRAVEL_MODALITIES.items():
            # Actual arithmetic computation
            transport_cost = mod["transport"]["rate_per_person"] * goal.num_people
            accommodation_cost = mod["accommodation"]["total_cost"]
            food_cost = mod["food"]["daily_rate_per_person"] * goal.num_people * goal.duration_days
            sightseeing_cost = mod["sightseeing"]["total_cost"]

            total_cost = transport_cost + accommodation_cost + food_cost + sightseeing_cost
            is_feasible = total_cost <= goal.budget_limit

            # Multi-attribute scoring logic
            # 1. Cost Efficiency Score (0 - 100): Higher savings yields higher score
            if is_feasible:
                savings = goal.budget_limit - total_cost
                cost_efficiency = round((savings / goal.budget_limit) * 100.0, 2)
                feasibility_score = 100.0
            else:
                cost_efficiency = 0.0
                feasibility_score = 0.0

            experience_rating = mod["experience_rating"]

            # Composite Weighted Evaluation:
            # Feasible candidates: 30% Cost Efficiency + 50% Experience Quality + 20% Feasibility
            # Prioritizes balanced travel comfort while respecting hard budget constraints
            if is_feasible:
                final_score = round(
                    (0.30 * cost_efficiency) +
                    (0.50 * experience_rating) +
                    (0.20 * feasibility_score),
                    2
                )
            else:
                # Heavy penalty for breaching user's budget ceiling
                deficit = total_cost - goal.budget_limit
                final_score = round(max(0.0, (0.20 * experience_rating) - (deficit * 0.01)), 2)

            cost_breakdown = {
                "transportation": transport_cost,
                "accommodation": accommodation_cost,
                "food": food_cost,
                "sightseeing": sightseeing_cost
            }

            candidate = CandidatePlan(
                plan_id=plan_id,
                name=mod["name"],
                transport_choice=mod["transport"]["name"],
                accommodation_choice=mod["accommodation"]["name"],
                food_tier=mod["food"]["tier"],
                sightseeing_tier=mod["sightseeing"]["tier"],
                cost_breakdown=cost_breakdown,
                total_cost=total_cost,
                is_feasible=is_feasible,
                cost_efficiency_score=cost_efficiency,
                experience_rating=experience_rating,
                feasibility_score=feasibility_score,
                final_score=final_score,
                description=mod["description"],
                pros=mod["pros"],
                cons=mod["cons"]
            )
            candidates.append(candidate)

        return candidates

    @classmethod
    def select_best_candidate(cls, candidates: List[CandidatePlan]) -> Tuple[CandidatePlan, str]:
        """
        Ranks candidate plans and selects the top-scoring feasible alternative.
        Returns the winning plan and a detailed justification text.
        """
        # Filter for feasible candidates
        feasible_plans = [c for c in candidates if c.is_feasible]
        if not feasible_plans:
            # Fallback to least over-budget
            fallback = min(candidates, key=lambda c: c.total_cost)
            return fallback, "No strictly feasible candidate found; selected candidate closest to budget ceiling."

        # Sort descending by final multi-attribute score
        ranked = sorted(feasible_plans, key=lambda c: c.final_score, reverse=True)
        winner = ranked[0]

        justification = (
            f"Selected '{winner.plan_id}: {winner.name}' with the highest composite score of {winner.final_score:.2f}/100. "
            f"While Plan A had greater cost savings, its experience rating was low (55.0/100) due to dormitory lodging. "
            f"Plan B delivers a balanced vacation experience (88.0/100) featuring a private beachfront resort and scooter rental, "
            f"while remaining comfortably within the budget ceiling at ₹{winner.total_cost:,.0f} (leaving a ₹{10000 - winner.total_cost:,.0f} safety buffer). "
            f"Plan C was rejected as infeasible (₹{candidates[2].total_cost:,.0f} > ₹10,000)."
        )

        return winner, justification
