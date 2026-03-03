"""
streamlit_app.py — Applied LLM Workflow Research: Interactive Portfolio
=======================================================================
A Streamlit web application that serves as both an interactive research
portfolio AND a usable tool for the Master Workflow prompting protocol.

This file is the ONLY Python file needed for Streamlit Community Cloud
deployment. It lives in the root of the GitHub repository alongside
the markdown case study files and workflow_runner.py.

How Streamlit works (for Waqas's reference):
---------------------------------------------
- Streamlit reruns this ENTIRE script every time the user interacts
  with any widget (button click, dropdown change, text input, etc.)
- That means: every variable gets re-created from scratch on each rerun.
- To remember things between reruns (like "which stage is the user on"),
  we use st.session_state — a persistent dictionary that survives reruns.
- Every st.something() call renders a visual element on the page.
- st.sidebar.something() renders it in the left sidebar instead.

Author: Waqas Sharif | github.com/Waqas01CP
"""

import streamlit as st
import os

# ============================================================================
# CONFIGURATION
# ============================================================================
# st.set_page_config() MUST be the first Streamlit command in the script.
# It sets the browser tab title, icon, and layout width.
# "wide" layout uses the full browser width instead of a narrow centered column.

st.set_page_config(
    page_title="Applied LLM Workflow Research",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================================
# DATA: MASTER WORKFLOW STAGES
# ============================================================================
# These are extracted directly from workflow_runner.py.
# Why extract instead of importing? Because workflow_runner.py uses print(),
# input(), and ANSI color codes — all terminal-only features that don't work
# in a web app. We take the DATA (the stages and case studies) and build a
# native web UI around them.

MASTER_WORKFLOW_STAGES = [
    {
        "name": "Intent Decomposition",
        "description": (
            "Before writing any prompt, explicitly decompose the user's goal "
            "into (a) the surface request — what they literally asked for, and "
            "(b) the underlying intent — what success actually looks like. "
            "Misalignment here is the root cause of the Optimal Answer Trap."
        ),
        "prompt_label": "Stage 1 Prompt Template",
        "prompt_content": (
            "ROLE: You are an intent analyst.\n\n"
            "TASK: I will give you a user request. Return ONLY a JSON object:\n"
            "{\n"
            '  "surface_request": "<what they literally asked>",\n'
            '  "underlying_intent": "<what they actually need>",\n'
            '  "success_criteria": ["<criterion 1>", "<criterion 2>"]\n'
            "}\n\n"
            "USER REQUEST: {user_request}\n\n"
            "Return JSON only. No preamble."
        ),
        # These are the placeholder variables in the prompt template.
        # The Prompt Playground will create text inputs for each one.
        "variables": ["user_request"],
    },
    {
        "name": "Context Injection",
        "description": (
            "Provide the model with all relevant constraints, prior findings, "
            "and domain knowledge BEFORE the instruction. This prevents the "
            "model from filling in gaps with plausible-sounding but incorrect "
            "assumptions — a key source of hallucination in long workflows."
        ),
        "prompt_label": "Stage 2 Prompt Template",
        "prompt_content": (
            "CONTEXT (read carefully before proceeding):\n"
            "  - Domain: {domain}\n"
            "  - Established facts: {known_facts}\n"
            "  - Constraints: {constraints}\n"
            "  - Prior session findings: {prior_findings}\n\n"
            "Only use information from the CONTEXT block above.\n"
            "If the context does not contain enough information to answer,\n"
            'say "INSUFFICIENT CONTEXT" rather than inferring.'
        ),
        "variables": ["domain", "known_facts", "constraints", "prior_findings"],
    },
    {
        "name": "Structured Output Enforcement",
        "description": (
            "Require the model to return output in a machine-readable format "
            "(JSON, numbered list, or a defined schema). This forces it to "
            "commit to discrete claims rather than hedging in prose — making "
            "hallucinations visible and auditable."
        ),
        "prompt_label": "Stage 3 Output Schema",
        "prompt_content": (
            "Return your answer as a JSON object matching this schema EXACTLY:\n"
            "{\n"
            '  "answer": "<your direct answer>",\n'
            '  "confidence": "HIGH | MEDIUM | LOW",\n'
            '  "sources_used": ["<source 1>", "<source 2>"],\n'
            '  "gaps": ["<anything you could not determine from context>"],\n'
            '  "follow_up_questions": ["<question to resolve gaps>"]\n'
            "}\n\n"
            "Do NOT add any text outside the JSON object."
        ),
        "variables": [],
    },
    {
        "name": "Red Teaming Pass",
        "description": (
            "After receiving the model's output, issue a second prompt that "
            "instructs the model to actively argue against its own answer. "
            "This is the core of the 'Draft-Critic' loop and directly targets "
            "Final Synthesis Bias — the tendency to over-commit to whichever "
            "framing appeared first in context."
        ),
        "prompt_label": "Stage 4 Red Team Prompt",
        "prompt_content": (
            "The following is a draft answer. Your job is to CHALLENGE it:\n\n"
            "DRAFT: {previous_output}\n\n"
            "Instructions:\n"
            "1. List every factual claim in the draft.\n"
            "2. For each claim, state whether it is: VERIFIED | UNVERIFIED | FALSE\n"
            "3. Identify any logical gaps or leaps.\n"
            "4. Suggest what a reasonable counterargument would be.\n"
            "5. Give a revised confidence rating: HIGH | MEDIUM | LOW\n\n"
            "Be adversarial. Your goal is to find weaknesses, not validate."
        ),
        "variables": ["previous_output"],
    },
    {
        "name": "Final Synthesis",
        "description": (
            "Issue a final synthesis prompt that combines the original output "
            "and the red team critique into a single, reconciled answer. "
            "Instruct the model to EXPLICITLY acknowledge any remaining "
            "uncertainty rather than papering over it — this produces "
            "calibrated outputs rather than false confidence."
        ),
        "prompt_label": "Stage 5 Synthesis Prompt",
        "prompt_content": (
            "You have two inputs:\n"
            "  ORIGINAL ANSWER: {original_answer}\n"
            "  RED TEAM CRITIQUE: {critique}\n\n"
            "Produce a FINAL, reconciled answer that:\n"
            "- Incorporates valid critique points\n"
            "- Explicitly marks any claims that remain uncertain as [UNCERTAIN]\n"
            "- Does NOT drop information just because it is hard to reconcile\n"
            "- Ends with a one-sentence confidence summary\n\n"
            "Format: Plain prose. No JSON. Aim for clarity over completeness."
        ),
        "variables": ["original_answer", "critique"],
    },
]


# ============================================================================
# DATA: CASE STUDIES
# ============================================================================
# Also extracted from workflow_runner.py. The "full_doc" field maps each case
# study to its corresponding full markdown file for deep-dive navigation.

CASE_STUDIES = {
    "hallucination_red_team": {
        "title": "Case Study: Red Teaming Historical Hallucination",
        "description": (
            "Demonstrates how the Red Teaming Pass (Stage 4) was used to catch "
            "Gemini fabricating specific historical dates and attributing quotes "
            "incorrectly. The model produced a confident, well-formatted response "
            "that contained three factual errors invisible without an adversarial pass."
        ),
        "example_request": "Explain the history of the Turing Test and its key milestones.",
        "key_finding": (
            "Without Stage 4, the model cited a 1966 ELIZA paper date as 1964 and "
            "attributed a Searle quote to Turing. The red team pass caught both."
        ),
        "full_doc": "07.0_Red_Teaming.md",
    },
    "synthesis_bias": {
        "title": "Case Study: Final Synthesis Bias",
        "description": (
            "Documents a consistent failure mode where Gemini's final answer "
            "over-weighted whichever framing appeared first in a long context window, "
            "even when later context directly contradicted it. The Master Workflow's "
            "explicit synthesis stage (Stage 5) resolves this."
        ),
        "example_request": "Compare Python and Julia for scientific computing.",
        "key_finding": (
            "In a 12,000-token context, whichever language appeared first in the prompt "
            "received a systematically higher rating even when the subsequent evidence "
            "favoured the other. Stage 5's reconciliation instruction broke this bias."
        ),
        "full_doc": "05.0_Chain_of_Density.md",
    },
    "context_engineering": {
        "title": "Case Study: Context Engineering for Long Windows",
        "description": (
            "Tests how context ordering, chunking strategy, and explicit 'read carefully' "
            "instructions affected recall accuracy in 1M-token Gemini sessions. Finds that "
            "Stage 2 (Context Injection) placement — always before the instruction, never "
            "after — reduced retrieval errors by an estimated 40% in structured tests."
        ),
        "example_request": "Summarise the key engineering decisions in this 800-page report.",
        "key_finding": (
            "Placing context AFTER the instruction caused the model to answer from prior "
            "knowledge rather than the injected context in ~30% of trials. Ordering matters."
        ),
        "full_doc": "08.0_Token_Sampling_Demonstration.md",
    },
}


# ============================================================================
# DATA: DOCUMENT REGISTRY
# ============================================================================
# Maps human-readable names to actual file paths in the repository.
# On Streamlit Community Cloud, the app runs from the repo root,
# so these relative paths resolve correctly.
#
# The order here determines the order in the dropdown menu.

DOCUMENTS = {
    "README — Project Overview": "README.md",
    "0.0 — The Master Workflow & Core Methodologies": "0.0_The_Master_Workflow.md",
    "1.0 — Meta-Prompting Case Study": "01.0_Meta_Prompting_Case_Study.md",
    "2.0 — Tree of Thoughts (ToT) Demonstration": "02.0_Tree_of_Thoughts_Demonstration.md",
    "3.0 — The 5-Step Prompt Framework": "03.0_5-Step_Framework.md",
    "4.0 — Tone and Style Control": "04.0_Tone_and_Style_Control.md",
    "5.0 — Chain of Density (Initial Attempt)": "05.0_Chain_of_Density.md",
    "5.1 — Master Workflow + Chain of Density": "05.1_Demonstration_of_the_Master_Workflow_(CoD).md",
    "6.0 — Prompt Chaining Demonstration": "06.0_Prompt_Chaining.md",
    "7.0 — Red Teaming Demonstration": "07.0_Red_Teaming.md",
    "8.0 — Token Sampling A/B Test": "08.0_Token_Sampling_Demonstration.md",
    "9.0 — AI Agents Demonstration": "09.0_AI_Agents_Demonstration.md",
    "10.0 — Data Analysis Strategies": "10.0_Data_Analysis_Strategies.md",
}


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def load_markdown(filepath: str) -> str:
    """
    Safely load a markdown file and return its contents as a string.

    Why a helper function? Because file reading can fail (file doesn't exist,
    encoding issues, etc.) and we want ONE place that handles all errors
    rather than duplicating try/except blocks everywhere.

    On Streamlit Community Cloud, the working directory is the repo root,
    so 'README.md' resolves to the repo's README.md.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return f"⚠️ File not found: `{filepath}`\n\nThis file may not be in the repository yet."
    except Exception as e:
        return f"⚠️ Error reading `{filepath}`: {e}"


def render_prompt_template(template: str, variables: dict) -> str:
    """
    Fill in a prompt template's placeholder variables with user-provided values.

    Uses Python's str.format_map() with a defaultdict-like approach:
    if a variable hasn't been filled in yet, it stays as {variable_name}
    in the output so the user can see what still needs filling.

    Why not str.format()? Because str.format() raises KeyError if ANY
    placeholder is missing. format_map with a custom dict lets us handle
    missing keys gracefully.
    """

    class SafeDict(dict):
        """Returns the placeholder itself for any missing keys."""
        def __missing__(self, key):
            return "{" + key + "}"

    return template.format_map(SafeDict(**variables))


# ============================================================================
# SECTION: HOME PAGE
# ============================================================================

def show_home():
    """
    The landing page. Shows a custom header + the project README.

    Why not just show the raw README? Because the README contains relative
    markdown links (like ./07.0_Red_Teaming.md) that won't work in Streamlit.
    We add a custom header with context, then render the README content.
    """
    st.title("🔬 Applied LLM Workflow Research")
    st.caption("A Behavioral Meta-Analysis & Workflow Architecture Study on Google Gemini")

    st.divider()

    # Quick orientation for visitors
    st.markdown("""
**What is this?** A research portfolio documenting original failure mode analysis
of Google Gemini and a 5-stage prompting protocol designed to force reliable outputs
from stochastic LLMs.

**What can you do here?**
- 📚 **Research Portfolio** — Read all 12 case studies and methodology documents
- 🔄 **Interactive Walkthrough** — Step through the 5-stage Master Workflow
- 🧪 **Prompt Playground** — Fill in real variables and generate ready-to-use prompts
- 📊 **Case Studies** — Explore the three core failure mode experiments

Use the sidebar to navigate.
    """)

    st.divider()

    # Render the actual README content
    readme_content = load_markdown("README.md")
    st.markdown(readme_content, unsafe_allow_html=False)


# ============================================================================
# SECTION: RESEARCH PORTFOLIO (Document Reader)
# ============================================================================

def show_portfolio():
    """
    Full document reader. User selects a case study from a dropdown,
    and the entire markdown file is rendered in the main content area.

    This is where Streamlit's simplicity shines — rendering a full
    research document is literally: read file → st.markdown(content).

    The sidebar dropdown is placed here (not globally) because this
    dropdown is only relevant when viewing the portfolio section.
    """
    st.title("📚 Research Portfolio")
    st.caption("Select a document to read the full case study or methodology breakdown.")

    # Dropdown for document selection
    # The keys of DOCUMENTS dict become the dropdown options.
    selected_name = st.selectbox(
        "Choose a document:",
        options=list(DOCUMENTS.keys()),
        # index=0 means the first item is selected by default
        index=0,
    )

    st.divider()

    # Load and render the selected document
    filepath = DOCUMENTS[selected_name]
    content = load_markdown(filepath)
    st.markdown(content, unsafe_allow_html=False)


# ============================================================================
# SECTION: INTERACTIVE WALKTHROUGH
# ============================================================================

def show_walkthrough():
    """
    Step-by-step walkthrough of the 5 Master Workflow stages.

    THIS IS WHERE YOU LEARN SESSION STATE.

    The problem: we need to track which stage the user is currently viewing.
    But Streamlit reruns the entire script on every interaction. If we wrote:
        current_stage = 0
    ...it would reset to 0 on every button click. Useless.

    The solution: st.session_state
    This is a dictionary that persists across reruns. We store the current
    stage index there. When the user clicks "Next", we increment the index
    in session_state. On the next rerun, the script reads the updated index
    and renders the correct stage.

    Think of session_state as a notebook that survives the script being
    re-executed. Everything else gets wiped; session_state stays.
    """
    st.title("🔄 Interactive Master Workflow Walkthrough")
    st.caption(
        "Step through the 5-stage protocol that forces deterministic outputs "
        "from stochastic LLMs. Each stage builds on the previous one."
    )

    # ── Initialize session state ──
    # This block runs on the FIRST load only. On subsequent reruns,
    # "walkthrough_stage" already exists in session_state, so we skip it.
    if "walkthrough_stage" not in st.session_state:
        st.session_state.walkthrough_stage = 0

    current = st.session_state.walkthrough_stage
    total = len(MASTER_WORKFLOW_STAGES)

    # ── Progress indicator ──
    # st.progress() renders a progress bar. Value must be between 0.0 and 1.0.
    st.progress((current + 1) / total, text=f"Stage {current + 1} of {total}")

    # ── Navigation buttons ──
    # st.columns() creates horizontal columns. We use 4 columns to space
    # the buttons nicely. Each column is an independent container.
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        # disabled=True greys out the button. Can't go back from stage 0.
        if st.button("⬅ Previous", disabled=(current == 0)):
            st.session_state.walkthrough_stage -= 1
            # st.rerun() forces an immediate rerun of the script.
            # Without this, the button click registers but the page
            # doesn't update until the NEXT interaction.
            st.rerun()

    with col2:
        if st.button("Next ➡", disabled=(current == total - 1)):
            st.session_state.walkthrough_stage += 1
            st.rerun()

    with col3:
        if st.button("🔄 Reset to Stage 1"):
            st.session_state.walkthrough_stage = 0
            st.rerun()

    with col4:
        # Toggle to show all stages at once instead of one-at-a-time
        show_all = st.checkbox("Show all stages")

    st.divider()

    # ── Render stages ──
    if show_all:
        # Show every stage with visual separation
        for i, stage in enumerate(MASTER_WORKFLOW_STAGES):
            _render_stage(i, stage)
            if i < total - 1:
                st.divider()
    else:
        # Show only the current stage
        _render_stage(current, MASTER_WORKFLOW_STAGES[current])


def _render_stage(index: int, stage: dict):
    """
    Render a single workflow stage with its description and prompt template.

    Uses st.expander() for the prompt template — this creates a collapsible
    section. The prompt starts collapsed so the user sees the description
    first and can expand the prompt when ready. This mirrors the interactive
    CLI experience where you read the stage description before seeing the prompt.
    """
    st.subheader(f"Stage {index + 1}: {stage['name']}")
    st.markdown(stage["description"])

    # st.expander() creates a collapsible section.
    # expanded=False means it starts collapsed.
    with st.expander(f"📋 {stage['prompt_label']}", expanded=False):
        # st.code() renders text in a monospaced code block with a copy button.
        # The copy button is automatic — Streamlit adds it.
        # language="" prevents syntax highlighting (this is a prompt, not code).
        st.code(stage["prompt_content"], language="")

        # If this stage has variables, show a note about the Prompt Playground
        if stage.get("variables"):
            var_list = ", ".join(f"`{{{v}}}`" for v in stage["variables"])
            st.info(
                f"💡 This template has fillable variables: {var_list}. "
                f"Go to **Prompt Playground** in the sidebar to fill them in "
                f"and generate a ready-to-use prompt."
            )


# ============================================================================
# SECTION: PROMPT PLAYGROUND
# ============================================================================

def show_playground():
    """
    The interactive prompt template filler.

    THIS IS THE KEY DIFFERENTIATING FEATURE of this app.

    The user selects a workflow stage, fills in the placeholder variables
    using text inputs, and sees the completed prompt update in real time.
    They can then copy the completed prompt and paste it directly into
    AI Studio, ChatGPT, Claude, or any LLM interface.

    This makes the Master Workflow protocol genuinely USABLE, not just readable.

    Technical notes:
    - Each text input widget needs a unique 'key' parameter. This is because
      Streamlit identifies widgets by their key. If two widgets have the same
      key, Streamlit gets confused about which one changed.
    - We prefix keys with the stage index to ensure uniqueness.
    """
    st.title("🧪 Prompt Playground")
    st.caption(
        "Select a workflow stage, fill in the variables, and get a ready-to-use prompt. "
        "Copy it directly into AI Studio, ChatGPT, or Claude."
    )

    # ── Stage selector ──
    # Only show stages that actually have fillable variables.
    # Stage 3 (Structured Output Enforcement) has no variables — it's a
    # fixed schema. No point showing it in the playground.
    stages_with_vars = [
        (i, s) for i, s in enumerate(MASTER_WORKFLOW_STAGES)
        if s.get("variables")
    ]

    stage_names = [f"Stage {i+1}: {s['name']}" for i, s in stages_with_vars]
    selected_idx = st.selectbox("Choose a stage:", options=range(len(stage_names)),
                                format_func=lambda x: stage_names[x])

    stage_index, stage = stages_with_vars[selected_idx]

    st.divider()

    # ── Explanation of this stage ──
    st.markdown(f"**{stage['name']}** — {stage['description']}")

    st.markdown("---")
    st.markdown("#### Fill in the variables:")

    # ── Dynamic text inputs for each variable ──
    # This loop creates one text input per placeholder variable in the template.
    user_values = {}
    for var in stage["variables"]:
        # Convert variable names to readable labels:
        # "user_request" → "User Request"
        label = var.replace("_", " ").title()

        # st.text_area() creates a multi-line text input.
        # The 'key' parameter must be unique across the entire app.
        # We use f"playground_{stage_index}_{var}" to guarantee uniqueness.
        user_values[var] = st.text_area(
            label=f"Enter **{label}**:",
            placeholder=f"Type your {label.lower()} here...",
            key=f"playground_{stage_index}_{var}",
            height=100,
        )

    st.markdown("---")
    st.markdown("#### Generated Prompt:")

    # ── Render the completed prompt ──
    completed = render_prompt_template(stage["prompt_content"], user_values)
    st.code(completed, language="")

    # ── Usage hint ──
    # Check if any variables are still empty
    unfilled = [v for v in stage["variables"] if not user_values.get(v)]
    if unfilled:
        remaining = ", ".join(f"`{{{v}}}`" for v in unfilled)
        st.warning(f"Still unfilled: {remaining}")
    else:
        st.success(
            "✅ All variables filled. Copy the prompt above and paste it into "
            "AI Studio, ChatGPT, Claude, or any LLM interface."
        )


# ============================================================================
# SECTION: CASE STUDIES
# ============================================================================

def show_case_studies():
    """
    Displays the three core case studies from the workflow_runner.py data,
    with links to their full markdown documents.

    This bridges the CLI tool's case study feature with the full research
    portfolio. The brief summary comes from workflow_runner.py's CASE_STUDIES
    dict; the deep dive is the corresponding full markdown document.
    """
    st.title("📊 Case Studies: LLM Failure Mode Research")
    st.caption(
        "Three documented experiments identifying and resolving failure modes "
        "in Google Gemini. Each case study demonstrates how a specific stage "
        "of the Master Workflow catches errors that naive prompting misses."
    )

    # ── Case study selector ──
    case_keys = list(CASE_STUDIES.keys())
    case_titles = [CASE_STUDIES[k]["title"] for k in case_keys]

    selected_idx = st.selectbox(
        "Select a case study:",
        options=range(len(case_keys)),
        format_func=lambda x: case_titles[x],
    )

    selected_key = case_keys[selected_idx]
    cs = CASE_STUDIES[selected_key]

    st.divider()

    # ── Case study summary ──
    st.subheader(cs["title"])
    st.markdown(cs["description"])

    # Two-column layout: example request on the left, key finding on the right.
    # st.columns() returns column objects that act as containers.
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("**Example Request Used:**")
        st.info(cs["example_request"])

    with col_right:
        st.markdown("**Key Finding:**")
        st.success(cs["key_finding"])

    # ── Deep dive: full document ──
    st.divider()
    st.subheader("📖 Full Research Document")

    # Load and render the full corresponding markdown file
    full_doc_path = cs.get("full_doc", "")
    if full_doc_path:
        content = load_markdown(full_doc_path)
        # Use an expander so the full document doesn't overwhelm the summary
        with st.expander("Click to read the full case study document", expanded=False):
            st.markdown(content, unsafe_allow_html=False)
    else:
        st.info("Full document not yet linked for this case study.")


# ============================================================================
# MAIN APP: SIDEBAR NAVIGATION + PAGE ROUTING
# ============================================================================

def main():
    """
    The main function that assembles the app.

    Sidebar contains the primary navigation. Based on which section the user
    selects, we call the corresponding function to render that page.

    This pattern — sidebar navigation + conditional rendering — is the standard
    way to build multi-section Streamlit apps in a single file. For larger apps,
    Streamlit has a built-in multi-page feature (separate .py files in a pages/
    directory), but for this size of app, a single file with functions is cleaner
    and easier to deploy.
    """

    # ── Sidebar ──
    with st.sidebar:
        st.title("Navigation")

        # st.radio() creates a radio button group. Only one can be selected.
        # It returns the string value of the selected option.
        page = st.radio(
            "Go to:",
            options=[
                "🏠 Home",
                "📚 Research Portfolio",
                "🔄 Interactive Walkthrough",
                "🧪 Prompt Playground",
                "📊 Case Studies",
            ],
            # index=0 means "Home" is selected by default
            index=0,
        )

        st.divider()

        # ── Sidebar footer with project info ──
        st.markdown("---")
        st.markdown(
            "**Author:** Waqas Sharif\n\n"
            "**GitHub:** [Waqas01CP](https://github.com/Waqas01CP)\n\n"
            "Built with [Streamlit](https://streamlit.io)"
        )

    # ── Page routing ──
    # Based on which radio button is selected, render the corresponding section.
    # This is the "router" of the app. Simple conditional logic.
    if page == "🏠 Home":
        show_home()
    elif page == "📚 Research Portfolio":
        show_portfolio()
    elif page == "🔄 Interactive Walkthrough":
        show_walkthrough()
    elif page == "🧪 Prompt Playground":
        show_playground()
    elif page == "📊 Case Studies":
        show_case_studies()


# ============================================================================
# ENTRY POINT
# ============================================================================
# When Streamlit runs this file, it executes everything at module level.
# The if __name__ == "__main__" guard ensures main() runs when the file
# is executed directly (which is how Streamlit runs it).

if __name__ == "__main__":
    main()
