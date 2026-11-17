"""
utility_based.py
----------------
Architecture D: Utility-Based Agent

Operates using a continuous preference/utility function:
    Percept -> [Update State] -> [Utility Function Evaluation U(s)] -> Action maximizing Expected Utility
Key Characteristics:
- Goes beyond binary goal success: measures HOW DESIRABLE each world state is.
- Balances conflicting trade-offs:
    1. Financial Cost Efficiency (saving money)
    2. Accommodation Quality & Comfort (resort vs. dorm)
    3. Sightseeing & Activity Experience (richness of exploration)
- Mathematical Utility Formula:
    Utility = (w_cost * S_cost) + (w_acc * S_acc) + (w_sight * S_sight) - Penalty_Infeasible
- Selects the optimal feasible alternative plan using this transparent score.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field


@dataclass
class CandidateTravelPlan:
    """Represents a candidate travel plan evaluated by the utility agent."""
    plan_id: str
    name: str
    transport: str
    transport_cost: float
    accommodation: str
    accommodation_cost: float
    food: str
    food_cost: float
    sightseeing: str
    sightseeing_cost: float
    accommodation_quality_score: float  # 0 to 100
    sightseeing_experience_score: float  # 0 to 100
    description: str

    @property
    def total_cost(self) -> float:
        return self.transport_cost + self.accommodation_cost + self.food_cost + self.sightseeing_cost


@dataclass
class UtilityWeights:
    """Weights governing the agent's trade-off preferences (sum to 1.0)."""
    cost_efficiency: float = 0.40
    accommodation_quality: float = 0.35
    sightseeing_experience: float = 0.25


class UtilityBasedAgent:
    """
    Demonstrates a Utility-Based Agent.
    Evaluates competing alternative travel plans against multi-attribute utility criteria,
    enforcing hard budget feasibility while maximizing consumer satisfaction.
    """

    def __init__(self, budget_limit: float = 10000.0, weights: Optional[UtilityWeights] = None):
        self.architecture_name = "Utility-Based Agent"
        self.budget_limit = budget_limit
        self.weights = weights or UtilityWeights()

    def calculate_plan_utility(self, plan: CandidateTravelPlan) -> Dict[str, Any]:
        """
        Computes the multi-attribute utility score for a candidate travel plan:
        1. Cost Efficiency Score (0 to 100):
           S_cost = max(0, 100 * (1 - TotalCost / BudgetLimit)) if within budget, else 0
        2. Accommodation Quality Score (0 to 100):
           Direct metric of room comfort, cleanliness, and amenities.
        3. Sightseeing Experience Score (0 to 100):
           Direct metric of cultural richness, mobility, and activities.
        4. Infeasibility Penalty:
           Massive deduction (-1000) if TotalCost > BudgetLimit.
        """
        is_feasible = plan.total_cost <= self.budget_limit

        if is_feasible:
            # Normalized cost efficiency: 100 at 0 cost, 0 at budget ceiling
            cost_efficiency_score = max(0.0, min(100.0, ((self.budget_limit - plan.total_cost) / self.budget_limit) * 100.0))
            infeasibility_penalty = 0.0
        else:
            cost_efficiency_score = 0.0
            deficit = plan.total_cost - self.budget_limit
            infeasibility_penalty = 500.0 + (deficit * 0.1)

        raw_utility = (
            (self.weights.cost_efficiency * cost_efficiency_score) +
            (self.weights.accommodation_quality * plan.accommodation_quality_score) +
            (self.weights.sightseeing_experience * plan.sightseeing_experience_score) -
            infeasibility_penalty
        )

        final_utility = round(raw_utility, 2)

        return {
            "plan_id": plan.plan_id,
            "plan_name": plan.name,
            "total_cost": plan.total_cost,
            "is_feasible": is_feasible,
            "remaining_budget": self.budget_limit - plan.total_cost if is_feasible else -(plan.total_cost - self.budget_limit),
            "component_scores": {
                "cost_efficiency_score": round(cost_efficiency_score, 1),
                "accommodation_quality_score": round(plan.accommodation_quality_score, 1),
                "sightseeing_experience_score": round(plan.sightseeing_experience_score, 1)
            },
            "weighted_contributions": {
                "cost_contribution": round(self.weights.cost_efficiency * cost_efficiency_score, 2),
                "quality_contribution": round(self.weights.accommodation_quality * plan.accommodation_quality_score, 2),
                "experience_contribution": round(self.weights.sightseeing_experience * plan.sightseeing_experience_score, 2),
                "penalty": round(infeasibility_penalty, 2)
            },
            "final_utility_score": final_utility
        }

    def evaluate_and_select_best_plan(self, candidates: List[CandidateTravelPlan]) -> Dict[str, Any]:
        """
        Ranks all candidate plans by utility score and selects the highest-scoring feasible plan.
        """
        evaluations = [self.calculate_plan_utility(p) for p in candidates]
        # Sort descending by final utility score
        sorted_evals = sorted(evaluations, key=lambda x: x["final_utility_score"], reverse=True)
        best_plan = sorted_evals[0]

        return {
            "agent_type": self.architecture_name,
            "weights_used": {
                "w_cost_efficiency": self.weights.cost_efficiency,
                "w_accommodation_quality": self.weights.accommodation_quality,
                "w_sightseeing_experience": self.weights.sightseeing_experience
            },
            "all_evaluated_plans": sorted_evals,
            "selected_optimal_plan": best_plan,
            "selection_rationale": (
                f"Selected '{best_plan['plan_name']}' with top utility score {best_plan['final_utility_score']}. "
                f"It achieves optimal balance between accommodation comfort ({best_plan['component_scores']['accommodation_quality_score']}/100) "
                f"and total expenditure (₹{best_plan['total_cost']:,.0f}) within the ₹{self.budget_limit:,.0f} budget."
            )
        }

    def run_demonstration(self) -> Dict[str, Any]:
        """
        Demonstrates the utility agent evaluating 3 classic candidate plans:
        - Plan A: Budget-Focused (Hostel Dorm, Non-AC train)
        - Plan B: Balanced (Sunset Beach Resort / Guesthouse, AC train)
        - Plan C: Experience-Focused / Luxury (Villa, Volvo bus, Scuba)
        """
        candidates = [
            CandidateTravelPlan(
                plan_id="Plan A",
                name="Budget-Focused Travel",
                transport="Standard Non-AC Sleeper Train",
                transport_cost=1600.0,
                accommodation="Sea Mist Backpacker Hostel (Dorm Pod)",
                accommodation_cost=1500.0,
                food="Local Dhabas & Street Food",
                food_cost=2000.0,
                sightseeing="Self-Guided Beach Walks & Public Transit",
                sightseeing_cost=800.0,
                accommodation_quality_score=45.0,
                sightseeing_experience_score=50.0,
                description="Maximizes cash savings but sacrifices room privacy and transport comfort."
            ),
            CandidateTravelPlan(
                plan_id="Plan B",
                name="Balanced Travel",
                transport="Konkan Express (AC 3-Tier Sleeper)",
                transport_cost=2000.0,
                accommodation="Sunset Beach Resort (3-Star Beachfront)",
                accommodation_cost=3000.0,
                food="Local Beach Shacks & Authentic Thalis",
                food_cost=3000.0,
                sightseeing="North Goa Forts & 2-Day Scooter Rental",
                sightseeing_cost=1200.0,
                accommodation_quality_score=85.0,
                sightseeing_experience_score=85.0,
                description="Best equilibrium of comfort, mobility, authentic dining, and budget compliance."
            ),
            CandidateTravelPlan(
                plan_id="Plan C",
                name="Experience-Focused Travel (Luxury)",
                transport="Multi-Axle AC Volvo Sleeper Bus",
                transport_cost=2800.0,
                accommodation="Heritage Boutique Beachfront Villa",
                accommodation_cost=4800.0,
                food="Fine Dining Seafood Restaurants",
                food_cost=4000.0,
                sightseeing="Guided Water Sports & Scuba Package + Private Cab",
                sightseeing_cost=2500.0,
                accommodation_quality_score=98.0,
                sightseeing_experience_score=95.0,
                description="Ultra-luxury itinerary; severely breaches the ₹10,000 budget ceiling."
            )
        ]

        return self.evaluate_and_select_best_plan(candidates)

