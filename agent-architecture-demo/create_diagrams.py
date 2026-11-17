"""
create_diagrams.py
------------------
Generates two publication-quality academic architecture diagrams (300 DPI):
1. system_architecture.png: End-to-end pipeline showing User Goal -> CoT -> ToT -> Best Selection -> ReAct Loop (Action, Observation, Replanning) -> Final Result.
2. agent_architectures_comparison.png: Side-by-side architectural flow comparison of all Five Agent Architectures (Simple Reflex, Model-Based, Goal-Based, Utility-Based, Learning).
"""

import os
import sys
import tempfile

# Ensure temp directory for Matplotlib cache
os.environ["MPLCONFIGDIR"] = os.path.join(tempfile.gettempdir(), ".mplcache")
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches


def generate_system_architecture_diagram(output_path: str):
    """
    Generates the end-to-end unified system architecture diagram:
    USER GOAL -> GOAL DECOMPOSITION (CoT) -> ALTERNATIVE PLAN GENERATION (ToT) ->
    BEST PLAN SELECTION -> ReAct REASONING LOOP (ACTION, OBSERVATION, REPLANNING) -> FINAL RESULT.
    """
    fig, ax = plt.subplots(figsize=(13, 15), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    # Academic Palette
    c_navy = "#1B365D"
    c_blue = "#0969DA"
    c_blue_light = "#EBF3FA"
    c_slate_bg = "#F6F8FA"
    c_green = "#1A7F37"
    c_green_light = "#EBF5FF"
    c_red = "#CF222E"
    c_red_light = "#FFEBE9"
    c_amber = "#BF8700"
    c_amber_light = "#FFF8E7"
    c_dark = "#24292E"
    c_border = "#D0D7DE"

    # Title Banner
    ax.text(50, 98.2, "SYSTEM ARCHITECTURE: UNIFIED CoT + ToT + ReAct DEMONSTRATOR",
            fontsize=13, fontweight="bold", ha="center", color=c_navy)
    ax.text(50, 96.5, "MIT ADT University | Units I & II: CO I & CO II | Student: Vedant Sattejkumar Kirange (PRN: ADT23SOCB1294)",
            fontsize=8.5, ha="center", color="#57606A")

    # 1. USER GOAL BOX
    g_box = patches.FancyBboxPatch((10, 89.5), 80, 5.8, boxstyle="round,pad=1.0",
                                  facecolor=c_blue_light, edgecolor=c_navy, linewidth=2.0)
    ax.add_patch(g_box)
    ax.text(50, 93.3, "USER GOAL SPECIFICATION", fontsize=10, fontweight="bold", ha="center", color=c_navy)
    ax.text(50, 91.0, '"Plan a 2-day Goa trip for 2 people within ₹10,000, including transportation, accommodation, food and sightseeing."',
            fontsize=8.5, fontstyle="italic", ha="center", color=c_dark)

    ax.annotate("", xy=(50, 85.5), xytext=(50, 89.5),
                arrowprops=dict(arrowstyle="->", lw=2, color=c_navy))

    # 2. GOAL DECOMPOSITION (CoT)
    cot_box = patches.FancyBboxPatch((8, 73.5), 84, 12.0, boxstyle="round,pad=1.0",
                                     facecolor="#F0F4F8", edgecolor=c_blue, linewidth=1.8)
    ax.add_patch(cot_box)
    ax.text(50, 83.2, "GOAL DECOMPOSITION: CHAIN-OF-THOUGHT (CoT) REASONING",
            fontsize=10.5, fontweight="bold", ha="center", color=c_navy)
    ax.text(50, 78.5,
            "• Entity & Constraint Extraction: Destination=Goa, Duration=2 Days, Travelers=2 People, Budget Cap=₹10,000\n"
            "• Ordered Subtask Dependency Graph: 1. Transport -> 2. Lodging -> 3. Food -> 4. Sightseeing -> 5. Aggregate -> 6. Audit\n"
            "• User-Facing Reasoning Summaries: Explains prerequisites without leaking raw internal prompt tokens",
            fontsize=8.0, ha="center", color=c_dark, linespacing=1.4)

    ax.annotate("", xy=(50, 69.5), xytext=(50, 73.5),
                arrowprops=dict(arrowstyle="->", lw=2, color=c_navy))

    # 3. ALTERNATIVE PLAN GENERATION (ToT)
    tot_box = patches.FancyBboxPatch((6, 52.0), 88, 17.5, boxstyle="round,pad=1.0",
                                     facecolor=c_slate_bg, edgecolor=c_border, linewidth=1.8)
    ax.add_patch(tot_box)
    ax.text(50, 67.5, "ALTERNATIVE PLAN GENERATION: TREE-OF-THOUGHT (ToT) EXPLORATION",
            fontsize=10.5, fontweight="bold", ha="center", color=c_navy)

    # Branch A
    b_a = patches.FancyBboxPatch((8, 53.5), 26, 12.0, boxstyle="round,pad=0.8",
                                facecolor="#FFFFFF", edgecolor="#6E7781", linewidth=1.4)
    ax.add_patch(b_a)
    ax.text(21, 63.5, "PLAN A: BUDGET-FOCUSED", fontsize=8.2, fontweight="bold", ha="center", color=c_navy)
    ax.text(21, 58.5, "• Non-AC Train (₹1,600)\n• Hostel Pod (₹1,500)\n• Local Meals (₹2,000)\n• Beach Walks (₹800)\nTotal: ₹5,900 [FEASIBLE]\nScore: 59.80 / 100",
            fontsize=7.2, ha="center", color=c_dark, linespacing=1.2)

    # Branch B (Winner)
    b_b = patches.FancyBboxPatch((37, 53.5), 26, 12.0, boxstyle="round,pad=0.8",
                                facecolor=c_green_light, edgecolor=c_green, linewidth=2.2)
    ax.add_patch(b_b)
    ax.text(50, 63.5, "PLAN B: BALANCED [SELECTED]", fontsize=8.2, fontweight="bold", ha="center", color=c_green)
    ax.text(50, 58.5, "• AC 3-Tier Train (₹2,000)\n• Beach Resort (₹3,000)\n• Shack Thalis (₹3,000)\n• Forts+Scooter (₹1,200)\nTotal: ₹9,200 [FEASIBLE]\nScore: 66.40 (TOP RANKED)",
            fontsize=7.2, ha="center", color=c_dark, linespacing=1.2)

    # Branch C (Pruned)
    b_c = patches.FancyBboxPatch((66, 53.5), 26, 12.0, boxstyle="round,pad=0.8",
                                facecolor=c_red_light, edgecolor=c_red, linewidth=1.4)
    ax.add_patch(b_c)
    ax.text(79, 63.5, "PLAN C: LUXURY [PRUNED]", fontsize=8.2, fontweight="bold", ha="center", color=c_red)
    ax.text(79, 58.5, "• Volvo AC Bus (₹2,800)\n• Heritage Villa (₹4,800)\n• Fine Dining (₹4,000)\n• Scuba + Cab (₹2,500)\nTotal: ₹14,100 [INFEASIBLE]\nOver budget by ₹4,100",
            fontsize=7.2, ha="center", color=c_dark, linespacing=1.2)

    ax.annotate("", xy=(50, 48.0), xytext=(50, 52.0),
                arrowprops=dict(arrowstyle="->", lw=2, color=c_navy))

    # 4. BEST PLAN SELECTION BANNER
    sel_box = patches.FancyBboxPatch((18, 43.5), 64, 4.5, boxstyle="round,pad=0.8",
                                     facecolor=c_green_light, edgecolor=c_green, linewidth=1.6)
    ax.add_patch(sel_box)
    ax.text(50, 45.7, "BEST PLAN SELECTION: Plan B (Balanced) Selected for ReAct Execution",
            fontsize=9.2, fontweight="bold", ha="center", color=c_green)

    ax.annotate("", xy=(50, 39.5), xytext=(50, 43.5),
                arrowprops=dict(arrowstyle="->", lw=2, color=c_navy))

    # 5. ReAct REASONING LOOP (THOUGHT -> ACTION -> OBSERVATION -> REPLANNING)
    react_box = patches.FancyBboxPatch((6, 14.0), 88, 25.5, boxstyle="round,pad=1.0",
                                       facecolor="#FFFFFF", edgecolor=c_navy, linewidth=2.0)
    ax.add_patch(react_box)
    ax.text(50, 37.2, "ReAct EXECUTION ENGINE: THOUGHT → ACTION → OBSERVATION LOOP",
            fontsize=10.5, fontweight="bold", ha="center", color=c_navy)

    # Sub-box: Execution sequence
    seq_box = patches.FancyBboxPatch((8, 15.5), 44, 19.5, boxstyle="round,pad=0.8",
                                    facecolor="#F8FAFC", edgecolor=c_blue, linewidth=1.4)
    ax.add_patch(seq_box)
    ax.text(30, 33.2, "Standard Tool Execution Chain", fontsize=8.5, fontweight="bold", ha="center", color=c_navy)
    ax.text(30, 24.5,
            "1. calculate_transport() -> AC Train = ₹2,000 [OK]\n"
            "2. search_accommodation('Sunset Beach Resort')\n"
            "   → FAILURE OBSERVED: Hotel fully booked!\n"
            "   → Intercepted by Dynamic Replanner\n"
            "3. estimate_food_cost() -> Beach Shacks = ₹3,000 [OK]\n"
            "4. select_sightseeing() -> Scooter + Forts = ₹1,200 [OK]\n"
            "5. calculate_total_budget() -> Sums to ₹8,200 [OK]\n"
            "6. verify_budget() -> Audits against ₹10,000 limit [PASSED]",
            fontsize=7.2, ha="center", color=c_dark, linespacing=1.25)

    # Sub-box: Controlled Failure & Replanning Loop
    replan_box = patches.FancyBboxPatch((54, 15.5), 38, 19.5, boxstyle="round,pad=0.8",
                                       facecolor=c_amber_light, edgecolor=c_amber, linewidth=1.6)
    ax.add_patch(replan_box)
    ax.text(73, 33.2, "Dynamic Replanning Sub-Loop", fontsize=8.5, fontweight="bold", ha="center", color="#7A4E00")
    ax.text(73, 24.5,
            "[CONTROLLED FAILURE TRIGGER]\n"
            "Assumption: Sunset Beach Resort (₹3,000)\n"
            "Observation: Unavailability error recorded.\n\n"
            "[AUTONOMOUS RECOVERY]\n"
            "• Explain Error: Peak tourist rush.\n"
            "• Search Alternatives: Budget guesthouse\n"
            "• verify_availability('Palm Breeze') -> Confirmed!\n"
            "• replan_accommodation() -> Booked for ₹2,000\n"
            "• In-Flight Plan Updated (Saved ₹1,000!)\n"
            "• Continue Pipeline without Restart",
            fontsize=7.2, ha="center", color=c_dark, linespacing=1.2)

    # Bidirectional arrow between action and observation inside loop
    ax.annotate("", xy=(54, 25), xytext=(52, 25),
                arrowprops=dict(arrowstyle="<->", lw=2, color=c_amber))

    ax.annotate("", xy=(50, 9.5), xytext=(50, 14.0),
                arrowprops=dict(arrowstyle="->", lw=2, color=c_navy))

    # 6. FINAL RESULT BOX
    res_box = patches.FancyBboxPatch((10, 2.5), 80, 7.0, boxstyle="round,pad=1.0",
                                     facecolor=c_green_light, edgecolor=c_green, linewidth=2.2)
    ax.add_patch(res_box)
    ax.text(50, 7.5, "FINAL RESULT: FEASIBLE & VERIFIED GOA TRAVEL PLAN",
            fontsize=10.5, fontweight="bold", ha="center", color=c_green)
    ax.text(50, 4.6,
            "Total Expenditure: ₹8,200 | Remaining Safety Buffer: ₹1,800 | Status: APPROVED (Within ₹10,000 Budget)\n"
            "Transit: ₹2,000 | Lodging (Palm Breeze Guesthouse): ₹2,000 | Dining: ₹3,000 | Activities: ₹1,200",
            fontsize=8.0, ha="center", color=c_dark)

    plt.tight_layout()
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"[+] System Architecture Diagram saved: {output_path}")


def generate_agent_comparison_diagram(output_path: str):
    """
    Generates a high-resolution comparison diagram contrasting all Five Agent Architectures:
    1. Simple Reflex Agent
    2. Model-Based Reflex Agent
    3. Goal-Based Agent
    4. Utility-Based Agent
    5. Learning Agent
    """
    fig, ax = plt.subplots(figsize=(15, 12), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    c_navy = "#1B365D"
    c_blue = "#0969DA"
    c_slate_bg = "#F6F8FA"
    c_border = "#D0D7DE"
    c_dark = "#24292E"

    ax.text(50, 98.0, "FIVE AGENT ARCHITECTURES: STRUCTURAL COMPARISON",
            fontsize=14, fontweight="bold", ha="center", color=c_navy)
    ax.text(50, 96.0, "Internal Structures, State Representations & Decision-Making Mechanisms (Russell & Norvig Paradigm)",
            fontsize=9.0, ha="center", color="#57606A")

    # 5 Columns for the 5 agents
    agents_info = [
        {
            "x": 2, "w": 18,
            "title": "A. SIMPLE REFLEX",
            "color": "#6E7781",
            "bg": "#F6F8FA",
            "core": "Condition-Action\nRules (if-then)",
            "memory": "None (Stateless)",
            "flow": "Sensors\n  ↓\n[Current Percept]\n  ↓\n[Condition-Action]\n  ↓\nActuators",
            "handling": "If hotel unavailable,\nrejects immediately.\nZero recovery.",
            "pros": "O(1) Ultra-fast\nDeterministic",
            "cons": "Infinite loops\nZero memory\nNo planning"
        },
        {
            "x": 21.5, "w": 18,
            "title": "B. MODEL-BASED",
            "color": "#0969DA",
            "bg": "#EBF3FA",
            "core": "Internal World Model\n+ State Transition",
            "memory": "State Memory\n(Budget, Tasks, History)",
            "flow": "Sensors\n  ↓\n[Update State]\n  ↓\n[Rules with State]\n  ↓\nActuators",
            "handling": "Remembers ₹2k spent,\nknows hotel failed,\npicks alternative.",
            "pros": "Handles partial view\nTracks budget",
            "cons": "Model drift\nNo optimization"
        },
        {
            "x": 41, "w": 18,
            "title": "C. GOAL-BASED",
            "color": "#8250DF",
            "bg": "#F5F0FF",
            "core": "Explicit Goal Target\n+ Planning Search",
            "memory": "Subtask Status &\nGoal Distance",
            "flow": "Sensors\n  ↓\n[State + Goal]\n  ↓\n[Search / Planning]\n  ↓\nActuators",
            "handling": "Decomposes Goa trip;\nselects actions to reach\ngoal state <= ₹10k.",
            "pros": "Flexible re-targeting\nMulti-step planning",
            "cons": "Binary success only\nCannot rank quality"
        },
        {
            "x": 60.5, "w": 18,
            "title": "D. UTILITY-BASED",
            "color": "#1A7F37",
            "bg": "#EBF5FF",
            "core": "Multi-Attribute\nUtility Function U(s)",
            "memory": "Evaluation Matrices &\nCandidate Branches",
            "flow": "Sensors\n  ↓\n[State + Utility]\n  ↓\n[Expected Utility Max]\n  ↓\nActuators",
            "handling": "Evaluates trade-offs:\nComfort (85) vs Cost.\nPicks top utility plan.",
            "pros": "Continuous scores\nOptimal trade-offs",
            "cons": "Weight tuning\nHigh computation"
        },
        {
            "x": 80, "w": 18,
            "title": "E. LEARNING AGENT",
            "color": "#BF8700",
            "bg": "#FFF8E7",
            "core": "Critic + Learner +\nPerformance Element",
            "memory": "Experience Replay &\nReliability Weights",
            "flow": "Critic → Learner\n  ↓       ↓\nPerf. Element\n  ↓\nActuators",
            "handling": "Downgrades failing\nhotels; learns to pick\nguesthouse directly.",
            "pros": "Self-improving\nAdapts to seasonality",
            "cons": "Trial error risk\nNeeds episodes"
        }
    ]

    for ag in agents_info:
        x, w = ag["x"], ag["w"]
        # Outer card
        card = patches.FancyBboxPatch((x, 4), w, 89, boxstyle="round,pad=0.8",
                                      facecolor=ag["bg"], edgecolor=ag["color"], linewidth=1.8)
        ax.add_patch(card)

        # Header Box
        hdr = patches.FancyBboxPatch((x + 0.5, 87.5), w - 1.0, 4.5, boxstyle="round,pad=0.5",
                                    facecolor=ag["color"], edgecolor=ag["color"])
        ax.add_patch(hdr)
        ax.text(x + (w / 2.0), 89.7, ag["title"], fontsize=8.5, fontweight="bold",
                ha="center", va="center", color="#FFFFFF")

        # Section 1: Core Engine
        ax.text(x + (w / 2.0), 84.5, "DECISION ENGINE", fontsize=7.2, fontweight="bold", ha="center", color=ag["color"])
        ax.text(x + (w / 2.0), 80.5, ag["core"], fontsize=7.2, ha="center", color=c_dark)

        # Line separator
        ax.plot([x + 1.5, x + w - 1.5], [77, 77], color=ag["color"], lw=0.8, alpha=0.5)

        # Section 2: Memory / State
        ax.text(x + (w / 2.0), 74.5, "STATE / MEMORY", fontsize=7.2, fontweight="bold", ha="center", color=ag["color"])
        ax.text(x + (w / 2.0), 71.0, ag["memory"], fontsize=7.0, ha="center", color=c_dark)

        # Line separator
        ax.plot([x + 1.5, x + w - 1.5], [67.5, 67.5], color=ag["color"], lw=0.8, alpha=0.5)

        # Section 3: Architecture Flow Diagram
        ax.text(x + (w / 2.0), 65.0, "EXECUTION FLOW", fontsize=7.2, fontweight="bold", ha="center", color=ag["color"])
        flow_box = patches.FancyBboxPatch((x + 1.2, 46.5), w - 2.4, 16.5, boxstyle="round,pad=0.4",
                                          facecolor="#FFFFFF", edgecolor=c_border, linewidth=1.0)
        ax.add_patch(flow_box)
        ax.text(x + (w / 2.0), 54.5, ag["flow"], fontsize=6.8, ha="center", va="center", color=c_dark, linespacing=1.2)

        # Section 4: Goa Trip Failure Handling
        ax.text(x + (w / 2.0), 43.5, "FAILURE HANDLING", fontsize=7.2, fontweight="bold", ha="center", color=ag["color"])
        ax.text(x + (w / 2.0), 37.5, ag["handling"], fontsize=6.8, ha="center", color=c_dark, linespacing=1.2)

        # Line separator
        ax.plot([x + 1.5, x + w - 1.5], [31.5, 31.5], color=ag["color"], lw=0.8, alpha=0.5)

        # Section 5: Strengths & Weaknesses
        ax.text(x + (w / 2.0), 28.5, "ADVANTAGES", fontsize=7.2, fontweight="bold", ha="center", color="#1A7F37")
        ax.text(x + (w / 2.0), 23.5, ag["pros"], fontsize=6.8, ha="center", color=c_dark, linespacing=1.2)

        ax.plot([x + 1.5, x + w - 1.5], [18.5, 18.5], color=ag["color"], lw=0.8, alpha=0.5)

        ax.text(x + (w / 2.0), 15.5, "LIMITATIONS", fontsize=7.2, fontweight="bold", ha="center", color="#CF222E")
        ax.text(x + (w / 2.0), 9.5, ag["cons"], fontsize=6.8, ha="center", color=c_dark, linespacing=1.2)

    plt.tight_layout()
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"[+] Agent Comparison Diagram saved: {output_path}")


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    outputs_dir = os.path.join(current_dir, "outputs")
    os.makedirs(outputs_dir, exist_ok=True)

    diag1 = os.path.join(outputs_dir, "system_architecture.png")
    diag2 = os.path.join(outputs_dir, "agent_architectures_comparison.png")

    generate_system_architecture_diagram(diag1)
    generate_agent_comparison_diagram(diag2)

    # Also copy to root for easy deliverable referencing
    root_dir = os.path.dirname(current_dir)
    import shutil
    shutil.copyfile(diag1, os.path.join(root_dir, "system_architecture.png"))
    shutil.copyfile(diag2, os.path.join(root_dir, "agent_architectures_comparison.png"))
    print("[+] Architecture diagrams copied to workspace root.")

