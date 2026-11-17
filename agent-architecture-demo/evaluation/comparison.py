"""
comparison.py
-------------
Comparative Evaluation Module for the Five Agent Architectures:
1. Simple Reflex Agent
2. Model-Based Reflex Agent
3. Goal-Based Agent
4. Utility-Based Agent
5. Learning Agent

Provides structured comparison data, evaluation metrics, and tabular formats
for academic reporting and Streamlit display.
"""

from typing import Dict, Any, List


AGENT_COMPARISON_DATA: List[Dict[str, str]] = [
    {
        "agent_type": "Simple Reflex Agent",
        "internal_architecture": "Sensors -> Condition-Action Rules (if-then) -> Actuators. Completely stateless (no memory of past states or percepts).",
        "decision_making_method": "Immediate stimulus-response rule lookup. Matches current instantaneous percept against hardcoded condition-action table.",
        "advantages": "Ultra-fast execution (O(1) to O(k) lookup), minimal compute and memory overhead, deterministic and predictable behavior.",
        "limitations": "Completely vulnerable to infinite loops in partially observable environments; zero adaptation, cannot remember past failures or plan multi-step goals.",
        "suitable_applications": "Thermostats, fire alarm triggers, basic automated braking (ABS), simple network packet filter firewalls."
    },
    {
        "agent_type": "Model-Based Reflex Agent",
        "internal_architecture": "Sensors -> State Estimator -> Internal World Model (tracks unobserved world states & physics) -> Condition-Action Rules with State -> Actuators.",
        "decision_making_method": "Evaluates condition-action rules using both the current percept AND the internal state history (tracks spent budget, booked tasks, hotel availability).",
        "advantages": "Handles partial observability, avoids repetitive cyclic errors, maintains context across sequential multi-step tasks.",
        "limitations": "Model drift if world dynamics diverge; requires accurate environment transition models; lacks explicit goal optimization or quality metrics.",
        "suitable_applications": "Automated vacuum cleaners with room mapping (Roomba), automotive cruise control with obstacle tracking, multi-step booking monitors."
    },
    {
        "agent_type": "Goal-Based Agent",
        "internal_architecture": "Sensors -> State Tracker -> Explicit Goal Specification -> Planning / Search Engine (DFS, A*, Task Decomposition) -> Actuators.",
        "decision_making_method": "Forward search, means-ends analysis, or hierarchical task decomposition. Selects action sequences that transition current state into goal state.",
        "advantages": "High behavioral flexibility; easy to reconfigure by changing the goal without rewriting rule tables; supports multi-step planning toward complex targets.",
        "limitations": "Binary objective mindset (goal achieved vs. not achieved); cannot differentiate between a high-comfort trip vs. an uncomfortable bare-minimum trip; higher compute overhead.",
        "suitable_applications": "GPS route navigation systems, robotic warehouse pick-and-pack planners, automated flight path planning."
    },
    {
        "agent_type": "Utility-Based Agent",
        "internal_architecture": "Sensors -> State Tracker -> Multi-Attribute Utility Function U(s) -> Decision-Theoretic Optimization Engine -> Actuators.",
        "decision_making_method": "Maximizes Expected Utility. Evaluates competing candidate plans by scoring trade-offs across cost efficiency, accommodation comfort, and activity quality.",
        "advantages": "Balances conflicting real-world constraints; provides continuous, nuanced desirability scores; selects optimal compromise when goals are contradictory.",
        "limitations": "Designing and calibrating multi-attribute utility weights is complex; computationally expensive over large combinatorial action spaces.",
        "suitable_applications": "Autonomous algorithmic stock trading, personalized travel recommendation platforms, dynamic hospital triage systems."
    },
    {
        "agent_type": "Learning Agent",
        "internal_architecture": "Split into 4 components: Critic (evaluates results against standard), Learning Element (updates knowledge/weights), Performance Element (operational actor), Problem Generator (probes new actions).",
        "decision_making_method": "Reinforcement learning / Bayesian belief updating. Adapts internal policies based on empirical success/failure feedback over sequential episodes.",
        "advantages": "Continuously improves over time; self-corrects after environmental disruptions; proactively avoids historical points of failure without manual code patches.",
        "limitations": "Requires training episodes and feedback signals; exploration carries risk of costly mistakes; policy convergence can be slow or unstable without safeguards.",
        "suitable_applications": "Autonomous vehicle navigation, adaptive recommendation systems (Netflix/Amazon), dynamic game AI, smart travel agents with supplier tracking."
    }
]


class AgentArchitectureComparator:
    """
    Provides programmatic access to comparative evaluation metrics
    and generates markdown and structured comparison tables.
    """

    @classmethod
    def get_comparison_table(cls) -> List[Dict[str, str]]:
        return AGENT_COMPARISON_DATA

    @classmethod
    def get_markdown_table(cls) -> str:
        headers = [
            "Agent Type",
            "Internal Architecture",
            "Decision-Making Method",
            "Advantages",
            "Limitations",
            "Suitable Real-World Applications"
        ]
        lines = []
        lines.append("| " + " | ".join(headers) + " |")
        lines.append("| " + " | ".join(["---"] * len(headers)) + " |")

        for row in AGENT_COMPARISON_DATA:
            lines.append(
                f"| **{row['agent_type']}** | "
                f"{row['internal_architecture']} | "
                f"{row['decision_making_method']} | "
                f"{row['advantages']} | "
                f"{row['limitations']} | "
                f"{row['suitable_applications']} |"
            )

        return "\n".join(lines)

