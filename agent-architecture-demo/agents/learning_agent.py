"""
learning_agent.py
-----------------
Architecture E: Learning Agent

Operates using the 4-component architecture (Russell & Norvig):
    1. Critic: Evaluates agent actions against external performance standards.
    2. Learning Element: Updates internal knowledge, policies, and beliefs from critic feedback.
    3. Performance Element: Executes current best policy to select real actions.
    4. Problem Generator: Proposes exploratory trials to discover new possibilities.
Key Characteristics:
- Stores historical episodic experiences (planning attempts, successes, failures).
- Uses recorded feedback to adapt future decision policies.
- Demonstration:
    * Episode 1: Recommends Sunset Beach Resort (high prior expectation). Fails due to room unavailability.
    * Feedback: Critic issues failure penalty (-50) and updates hotel reliability knowledge.
    * Episode 2: Learned model adapts. Sunset Beach Resort reliability is downgraded;
      Palm Breeze Budget Guesthouse is elevated and selected directly without failure!
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
import json


@dataclass
class EpisodeExperience:
    """Records one historical planning episode."""
    episode_id: int
    hotel_selected: str
    booking_success: bool
    cost: float
    replanning_required: bool
    critic_reward: float
    notes: str


@dataclass
class HotelKnowledge:
    """Learned parameters for a specific lodging property."""
    hotel_name: str
    trials: int = 0
    failures: int = 0
    successes: int = 0
    reliability_score: float = 0.5  # Prior expectation [0.0, 1.0]
    estimated_cost: float = 3000.0


class LearningAgent:
    """
    Demonstrates a complete Learning Agent.
    Implements Critic, Learning Element, Performance Element, and Problem Generator
    to demonstrate adaptive decision making from experience.
    """

    def __init__(self):
        self.architecture_name = "Learning Agent"
        # Episode History Buffer (Experience Replay)
        self.experience_memory: List[EpisodeExperience] = []

        # Learned Knowledge Base (Hotel Reliability Models)
        self.knowledge_base: Dict[str, HotelKnowledge] = {
            "Sunset Beach Resort": HotelKnowledge(
                hotel_name="Sunset Beach Resort",
                trials=0,
                failures=0,
                successes=0,
                reliability_score=0.85,  # High naive prior belief
                estimated_cost=3000.0
            ),
            "Palm Breeze Budget Guesthouse": HotelKnowledge(
                hotel_name="Palm Breeze Budget Guesthouse",
                trials=0,
                failures=0,
                successes=0,
                reliability_score=0.60,  # Moderate prior belief
                estimated_cost=2000.0
            ),
            "Sea Mist Backpacker Hostel": HotelKnowledge(
                hotel_name="Sea Mist Backpacker Hostel",
                trials=0,
                failures=0,
                successes=0,
                reliability_score=0.50,
                estimated_cost=1500.0
            )
        }

    # =========================================================================
    # 1. Performance Element
    # =========================================================================
    def performance_element_select_hotel(self, allow_exploration: bool = False) -> str:
        """
        Selects accommodation using the current learned policy.
        Combines expected utility with learned reliability score.
        Score = Reliability * (Budget_Limit - Cost)
        """
        ranked_hotels = []
        for name, kb in self.knowledge_base.items():
            expected_utility = kb.reliability_score * (10000.0 - kb.estimated_cost)
            ranked_hotels.append((name, expected_utility, kb.reliability_score))

        # Sort descending by expected learned utility
        ranked_hotels.sort(key=lambda x: x[1], reverse=True)
        return ranked_hotels[0][0]

    # =========================================================================
    # 2. Critic
    # =========================================================================
    def critic_evaluate(self, hotel_name: str, booking_success: bool, replanning_needed: bool) -> float:
        """
        Evaluates execution outcome against performance standard:
        - Successful direct booking: +50 reward
        - Unavailability failure requiring replanning: -50 penalty
        """
        if booking_success and not replanning_needed:
            return 50.0
        elif not booking_success:
            return -50.0
        else:
            return 10.0  # Replanned successfully but had friction

    # =========================================================================
    # 3. Learning Element
    # =========================================================================
    def learning_element_update(self, episode: EpisodeExperience) -> Dict[str, Any]:
        """
        Updates internal knowledge base using reinforcement feedback from the Critic.
        Adjusts reliability score: R_new = R_old + alpha * (Outcome - R_old)
        """
        kb = self.knowledge_base[episode.hotel_selected]
        kb.trials += 1
        alpha = 0.40  # Learning rate

        if episode.booking_success:
            kb.successes += 1
            target = 1.0
        else:
            kb.failures += 1
            target = 0.0

        old_score = kb.reliability_score
        kb.reliability_score = round(old_score + alpha * (target - old_score), 3)

        self.experience_memory.append(episode)

        return {
            "hotel": episode.hotel_selected,
            "old_reliability": old_score,
            "new_reliability": kb.reliability_score,
            "trials": kb.trials,
            "failures": kb.failures,
            "critic_reward": episode.critic_reward
        }

    # =========================================================================
    # 4. Problem Generator
    # =========================================================================
    def problem_generator_suggest_probe(self) -> str:
        """
        Suggests exploratory actions (probing unverified or lesser-known alternatives)
        to prevent stagnation in suboptimal local optima.
        """
        # Find least explored option
        least_tried = min(self.knowledge_base.values(), key=lambda x: x.trials)
        return least_tried.hotel_name

    def run_demonstration(self) -> Dict[str, Any]:
        """
        Runs a comprehensive 2-Episode learning demonstration:
        - Episode 1 (Untrained): Naively picks Sunset Beach Resort -> Observes failure -> Critic penalizes -> Learner updates reliability.
        - Episode 2 (Trained): Evaluates updated knowledge -> Sunset Beach Resort is deprioritized -> Picks Palm Breeze Budget Guesthouse directly!
        """
        episode_logs = []

        # --- EPISODE 1: Naive Prior ---
        choice_ep1 = self.performance_element_select_hotel()
        # Simulated environment response: Sunset Beach Resort is unavailable
        success_ep1 = False
        reward_ep1 = self.critic_evaluate(choice_ep1, success_ep1, replanning_needed=True)
        exp1 = EpisodeExperience(
            episode_id=1,
            hotel_selected=choice_ep1,
            booking_success=success_ep1,
            cost=3000.0,
            replanning_required=True,
            critic_reward=reward_ep1,
            notes="Initial assumption failed: Sunset Beach Resort was fully booked."
        )
        update_info_ep1 = self.learning_element_update(exp1)

        episode_logs.append({
            "episode": 1,
            "state_of_knowledge": "Untrained / Naive Prior",
            "hotel_chosen": choice_ep1,
            "environment_observation": "FAILED (Unavailable)",
            "critic_reward": reward_ep1,
            "learning_update": update_info_ep1,
            "adaptation_note": f"Sunset Beach Resort reliability dropped from {update_info_ep1['old_reliability']} to {update_info_ep1['new_reliability']}."
        })

        # --- EPISODE 2: After Learning ---
        choice_ep2 = self.performance_element_select_hotel()
        # Simulated environment response: Palm Breeze Budget Guesthouse is available
        success_ep2 = True
        reward_ep2 = self.critic_evaluate(choice_ep2, success_ep2, replanning_needed=False)
        exp2 = EpisodeExperience(
            episode_id=2,
            hotel_selected=choice_ep2,
            booking_success=success_ep2,
            cost=2000.0,
            replanning_required=False,
            critic_reward=reward_ep2,
            notes="Direct booking succeeded without any replanning friction."
        )
        update_info_ep2 = self.learning_element_update(exp2)

        episode_logs.append({
            "episode": 2,
            "state_of_knowledge": "Trained with Failure Experience",
            "hotel_chosen": choice_ep2,
            "environment_observation": "SUCCESS (Available & Confirmed)",
            "critic_reward": reward_ep2,
            "learning_update": update_info_ep2,
            "adaptation_note": f"Agent avoided repeating the failed assumption and selected '{choice_ep2}' directly."
        })

        return {
            "agent_type": self.architecture_name,
            "learning_components": {
                "Critic": "Issues rewards/penalties based on room availability and replanning friction",
                "Learning_Element": "Updates property reliability weights via reinforcement rule",
                "Performance_Element": "Selects highest expected utility hotel using updated reliability beliefs",
                "Problem_Generator": "Identifies unexplored hotels to probe new availability"
            },
            "knowledge_base_state": {
                k: {
                    "reliability_score": v.reliability_score,
                    "trials": v.trials,
                    "failures": v.failures,
                    "successes": v.successes
                }
                for k, v in self.knowledge_base.items()
            },
            "episodes": episode_logs,
            "core_takeaway": (
                "A learning agent remembers past failures and actively adapts its internal policy. "
                "Instead of repeatedly failing at Sunset Beach Resort in future trips, it automatically shifts "
                "priorities toward reliable options like Palm Breeze Budget Guesthouse."
            )
        }

