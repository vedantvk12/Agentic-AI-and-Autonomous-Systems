"""
debate_topics.py
----------------
Structured Academic Debate Preparation and Discussion Content for MIT ADT University.
Course: Units I & II: Introduction to Agentic AI and Autonomous Systems; Reasoning, Planning & Decision-Making (CO I & CO II).

Contains 10 comprehensive debate topics with balanced arguments (PRO vs CON),
deep technical rationales, and sample student-level model answers.
"""

from typing import Dict, Any, List
from dataclasses import dataclass


@dataclass
class DebateTopic:
    """Structure for an academic debate topic."""
    question_number: int
    question: str
    concept_mapping: str
    arguments_supporting: List[str]
    arguments_opposing: List[str]
    sample_student_answer: str
    key_takeaway: str


DEBATE_TOPICS: List[DebateTopic] = [
    DebateTopic(
        question_number=1,
        question="Is a simple reflex agent sufficient for complex real-world tasks?",
        concept_mapping="Agent Architectures: Condition-Action Rules vs. Environmental Complexity (CO I)",
        arguments_supporting=[
            "Extremely low computational latency; executes in O(1) time without state tracking overhead.",
            "Completely predictable and deterministic: ideal for safety-critical micro-tasks like anti-lock braking (ABS) and emergency thermal shutdowns.",
            "Zero memory footprint makes it ultra-reliable on constrained edge microcontrollers."
        ],
        arguments_opposing=[
            "Completely fails in partially observable environments where the current percept does not convey the full world state.",
            "Highly prone to infinite execution loops when conditions oscillate.",
            "Lacks memory: cannot track spent budget, past hotel rejections, or sequential prerequisites."
        ],
        sample_student_answer=(
            "No, a simple reflex agent is insufficient for complex real-world travel planning. "
            "In our Goa travel experiment, when Sunset Beach Resort was unavailable, a simple reflex agent could only emit 'REJECT_HOTEL'. "
            "It could not remember that transit was already booked for ₹2,000, nor could it calculate remaining funds to choose an alternative. "
            "Because real-world domains are partially observable and sequential, agents must maintain historical state."
        ),
        key_takeaway="Simple reflex agents excel at instantaneous atomic reactions, but complex tasks necessitate internal state and goal representation."
    ),
    DebateTopic(
        question_number=2,
        question="Why would a model-based agent outperform a simple reflex agent in travel planning?",
        concept_mapping="State Representation and Partial Observability (CO I)",
        arguments_supporting=[
            "Maintains an internal world model tracking unobservable factors such as spent budget and confirmed bookings.",
            "Prevents redundant actions: remembers that transit is already booked and doesn't re-execute it.",
            "Remembers failure history: skips hotels known to be fully booked without making redundant API calls."
        ],
        arguments_opposing=[
            "Higher memory and state synchronization overhead; susceptible to 'model drift' if the real world changes out-of-band.",
            "More complex code architecture requiring transition models that specify how the environment changes.",
            "Still lacks explicit preference optimization (needs utility functions to choose between two valid hotels)."
        ],
        sample_student_answer=(
            "A model-based agent outperforms a simple reflex agent because it retains an internal state of the environment. "
            "In our demonstration, after observing that Sunset Beach Resort failed, the model-based agent updated its internal registry "
            "and remembered that ₹2,000 was already spent on train tickets. It used this knowledge to evaluate subsequent candidate hotels "
            "against the remaining ₹8,000 balance, avoiding redundant inquiries and preventing circular loops."
        ),
        key_takeaway="Internal state tracking transforms isolated sensory inputs into continuous, context-aware decision sequences."
    ),
    DebateTopic(
        question_number=3,
        question="Is a goal-based agent always better than a utility-based agent?",
        concept_mapping="Goal Satisfaction vs. Multi-Attribute Utility Optimization (CO I)",
        arguments_supporting=[
            "Goal-based agents are simpler to specify: 'Trip booked <= ₹10,000' is easier to define than continuous utility equations.",
            "Faster decision making when any satisfying solution is acceptable (satisficing principle).",
            "Clear binary verification: either the goal state is achieved or it is not."
        ],
        arguments_opposing=[
            "Treats all valid solutions as equal: a trip staying in a noisy dorm pod is treated identically to a private resort if both cost <= ₹10,000.",
            "Cannot balance conflicting trade-offs (e.g. spending ₹500 more for significantly higher safety or comfort).",
            "Fails to provide graceful degradation when no plan can 100% fulfill all goal constraints."
        ],
        sample_student_answer=(
            "No, a goal-based agent is not always better. While goal-based agents are effective at finding a valid sequence of actions "
            "to achieve a binary target, they cannot differentiate between a mediocre plan and an optimal one. In our project, "
            "both Plan A (Hostel Dorm, ₹5,900) and Plan B (Resort/Guesthouse, ₹8,200) satisfy the goal of visiting Goa under ₹10,000. "
            "However, the utility-based agent evaluates user comfort (88 vs 55) against cost efficiency, correctly identifying Plan B "
            "as the superior overall experience."
        ),
        key_takeaway="Goal-based planning finds feasible paths; utility-based planning finds the most desirable and balanced paths."
    ),
    DebateTopic(
        question_number=4,
        question="What are the critical limitations and risks of learning agents in autonomous decision-making?",
        concept_mapping="Adaptive Systems, Exploration vs Exploitation, and Safety (CO I & CO II)",
        arguments_supporting=[
            "Learning agents improve continuously with experience, adapting to seasonality and supplier reliability automatically.",
            "Eliminates hardcoded assumptions: learns empirically that certain hotels overbook on weekends.",
            "Discovers novel, cost-effective options through exploratory policies."
        ],
        arguments_opposing=[
            "Exploration can cause catastrophic real-world failures (e.g. testing an unverified supplier with user money).",
            "Cold-start problem: requires historical trial episodes before policies converge to high reliability.",
            "Susceptible to reward gaming or biased training distributions (e.g. never retrying a hotel after an isolated glitch)."
        ],
        sample_student_answer=(
            "The main limitation of learning agents is the risk of real-world trial-and-error exploration. "
            "If an autonomous agent is spending actual user money, exploratory actions that fail (e.g. booking an unrated property) "
            "cause financial loss and user dissatisfaction. Furthermore, learning agents require extensive feedback loops and warm-up "
            "episodes before their reliability scores become statistically trustworthy."
        ),
        key_takeaway="Autonomous learning agents require strict safety guardrails and offline simulation environments before deploying live."
    ),
    DebateTopic(
        question_number=5,
        question="How does Tree-of-Thought (ToT) improve upon linear single-path planning?",
        concept_mapping="Search and Exploration in Reasoning Frameworks (CO II)",
        arguments_supporting=[
            "Explores multiple distinct strategic branches (Budget vs. Balanced vs. Luxury) simultaneously.",
            "Enables lookahead evaluation and mathematical pruning before committing irreversible actions.",
            "Allows backtracking from unpromising branches (e.g. pruning Plan C when cost exceeds ₹10,000)."
        ],
        arguments_opposing=[
            "Exponential branch explosion if search depth and branching factors are unconstrained.",
            "Requires heuristic scoring functions to evaluate intermediate tree nodes.",
            "Higher memory footprint compared to greedy single-path linear planning."
        ],
        sample_student_answer=(
            "Tree-of-Thought (ToT) substantially improves planning by treating the decision space as a tree rather than a single linear track. "
            "In our Goa case study, ToT generated Plan A (Budget), Plan B (Balanced), and Plan C (Luxury). It computed the total cost and "
            "experience rating for each branch, immediately pruning Plan C as infeasible (₹14,100 > ₹10,000) and selecting Plan B as optimal. "
            "This prevented the agent from blindly walking down an infeasible path."
        ),
        key_takeaway="ToT brings classical heuristic search principles (like A* and minimax) into generative AI and agentic reasoning."
    ),
    DebateTopic(
        question_number=6,
        question="What are the primary limitations of pure Chain-of-Thought (CoT) reasoning without acting?",
        concept_mapping="Chain-of-Thought vs. Ground-Truth Grounding (CO II)",
        arguments_supporting=[
            "CoT decomposes complex goals into logical subtasks and exposes transparent reasoning summaries.",
            "Enforces causal ordering and prerequisite dependencies before execution begins.",
            "Computationally lightweight compared to full tree exploration."
        ],
        arguments_opposing=[
            "Pure CoT is an open-loop mental simulation; it has no mechanism to observe external ground truth.",
            "Vulnerable to hallucinations: if an internal premise is wrong (e.g. assuming Sunset Beach Resort is available), CoT continues unaware.",
            "Cannot recover dynamically when environmental conditions deviate from its generated narrative."
        ],
        sample_student_answer=(
            "Pure Chain-of-Thought is purely cognitive and ungrounded. In our experiment, CoT produced a beautifully reasoned 6-step plan "
            "assuming Sunset Beach Resort was available. However, because pure CoT does not interact with real tools, it had no way of knowing "
            "that the resort was fully booked. Without an active execution loop, pure CoT remains brittle in dynamic environments."
        ),
        key_takeaway="CoT provides the blueprint, but without real-time tool grounding, the blueprint cannot verify physical reality."
    ),
    DebateTopic(
        question_number=7,
        question="Why does ReAct interleave Thought, Action, and Observation rather than acting blindly?",
        concept_mapping="Synergy of Reasoning and Acting in ReAct (CO II)",
        arguments_supporting=[
            "Reasoning thoughts guide which tool action to select and explain the strategic context.",
            "Observations inject external ground truth (API status, room inventory, exact costs) into agent context.",
            "Creates a closed-loop feedback controller that can detect unexpected errors and replan on the fly."
        ],
        arguments_opposing=[
            "Interleaving reasoning and tool calls increases overall latency per task.",
            "Requires robust tool APIs and structured result schemas.",
            "Parsing observations consumes context window tokens in LLM architectures."
        ],
        sample_student_answer=(
            "ReAct interleaves Thought, Action, and Observation to create a closed-loop feedback system. "
            "The Thought formulates intent ('I will check hotel availability'), the Action calls the tool (`search_accommodation()`), "
            "and the Observation captures ground truth ('Hotel is unavailable'). This immediate observation allows the agent to recognize "
            "a failed premise in real-time and trigger an immediate dynamic recovery."
        ),
        key_takeaway="ReAct bridges cognitive planning with empirical reality, creating agents that think before acting and adapt after observing."
    ),
    DebateTopic(
        question_number=8,
        question="Can the ReAct framework recover from every planning failure autonomously?",
        concept_mapping="Failure Modes and Boundaries of Autonomous ReAct (CO II)",
        arguments_supporting=[
            "Dynamic replanning allows in-flight task substitution (e.g. swapping hotel for a guesthouse).",
            "Can retry with modified parameters or alternative catalog items.",
            "Catches tool-level exceptions and adapts task sequences without restarting."
        ],
        arguments_opposing=[
            "Cannot recover if all alternatives in the environment are exhausted (e.g. total region-wide hotel blackout).",
            "Vulnerable to infinite replanning loops if failure causes are misdiagnosed.",
            "Cannot recover from irrecoverable actions (e.g. non-refundable financial transactions already executed)."
        ],
        sample_student_answer=(
            "No, ReAct cannot recover from every planning failure. While ReAct successfully handled our hotel unavailability by substituting "
            "Palm Breeze Budget Guesthouse, its recovery ability depends strictly on environment slack and catalog inventory. "
            "If all hotels were booked, or if transit had already deducted ₹9,000 leaving insufficient funds for food, ReAct would fail "
            "unless granted human intervention or goal relaxation capabilities."
        ),
        key_takeaway="ReAct is an adaptive recovery engine, but it is bounded by environment constraints and irreversible action risks."
    ),
    DebateTopic(
        question_number=9,
        question="What happens when an agent receives an incorrect, incomplete, or corrupted observation?",
        concept_mapping="Observation Integrity, Hallucinations, and Epistemic Uncertainty (CO II)",
        arguments_supporting=[
            "Agents with schema validation can flag malformed tool outputs and retry.",
            "Multi-source corroboration can cross-verify facts before accepting them into state.",
            "Probabilistic state estimators maintain belief distributions rather than hard truths."
        ],
        arguments_opposing=[
            "Standard ReAct agents naively trust tool observations as infallible ground truth.",
            "An incorrect observation (e.g. reporting a ₹5,000 hotel as ₹1,000) will silently corrupt the budget audit.",
            "Garbage in, garbage out: flawed observations trigger cascading faulty decisions downstream."
        ],
        sample_student_answer=(
            "When an agent receives an incorrect observation, standard ReAct architecture suffers from epistemic corruption. "
            "For example, if an API omits hotel taxes or returns a false availability, the agent updates its internal model with false data. "
            "Subsequent thoughts and actions will be predicated on this falsehood, leading to severe budget overruns. "
            "To solve this, agents must implement schema validation, sanity assertions, and sanity check guardrails."
        ),
        key_takeaway="Observation integrity is the bedrock of autonomous agency; unvalidated observations lead to catastrophic state drift."
    ),
    DebateTopic(
        question_number=10,
        question="Which architecture would you choose for a production autonomous travel-planning system and why?",
        concept_mapping="Architectural Synthesis and Real-World System Design (CO I & CO II)",
        arguments_supporting=[
            "A hybrid architecture: ToT for strategic exploration + Utility function for scoring + ReAct for grounded execution + Learning for supplier tracking.",
            "Utility-based scoring guarantees personalization and constraint trade-offs.",
            "ReAct execution with tool verification guarantees verified bookings and dynamic error recovery."
        ],
        arguments_opposing=[
            "A single pure architecture (e.g. pure reflex or pure goal) is vastly cheaper and simpler to build.",
            "Hybrid systems have higher engineering complexity and more points of potential failure.",
            "Balancing learning updates against deterministic business rules requires delicate governance."
        ],
        sample_student_answer=(
            "For a production autonomous travel system, I would select a Hybrid Architecture combining Tree-of-Thought (ToT), "
            "a Utility-Based evaluator, and a ReAct execution engine with Learning memory. "
            "ToT explores alternative itineraries upfront; the Utility agent scores them against user preferences and budget limits; "
            "the ReAct engine executes real-world API tools with closed-loop failure recovery; and the Learning component records supplier "
            "reliability to continuously optimize future recommendations."
        ),
        key_takeaway="Modern production systems do not use a single agent paradigm in isolation; they synthesize ToT, Utility, ReAct, and Learning into a unified pipeline."
    )
]


class DebateContentManager:
    """Provides structured access to debate topics for UI, documentation, and academic reporting."""

    @classmethod
    def get_all_topics(cls) -> List[DebateTopic]:
        return DEBATE_TOPICS

    @classmethod
    def get_topic_by_number(cls, number: int) -> DebateTopic:
        for t in DEBATE_TOPICS:
            if t.question_number == number:
                return t
        return DEBATE_TOPICS[0]

