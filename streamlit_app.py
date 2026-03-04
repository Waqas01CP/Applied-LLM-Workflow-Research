"""
streamlit_app.py — Applied LLM Workflow Research: Interactive Portfolio
=======================================================================
A Streamlit web application that serves as both an interactive research
portfolio AND a usable tool for the Master Workflow prompting protocol.

This file is the ONLY Python file needed for Streamlit Community Cloud.
It lives in the root of the GitHub repository alongside the markdown
case study files and workflow_runner.py.

How Streamlit works (reminder):
- Streamlit reruns this ENTIRE script on every user interaction.
- st.session_state is a persistent dictionary that survives reruns.
- Every st.something() call renders a visual element on the page.
- st.sidebar.something() renders it in the left sidebar.

Author: Waqas Sharif | github.com/Waqas01CP
"""

import streamlit as st
import os

# ============================================================================
# CONFIGURATION — must be the FIRST Streamlit command
# ============================================================================

st.set_page_config(
    page_title="Applied LLM Workflow Research",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================================
# DATA: THE MASTER WORKFLOW METHODOLOGY (from 0.0_The_Master_Workflow.md)
# ============================================================================

MASTER_WORKFLOW_STEPS = [
    {
        "name": "Content Generation Prompt",
        "description": (
            "The primary creative or factual step. The Director (you) writes "
            "a detailed prompt to generate new content or iterate on a previous "
            "output. Label the prompt clearly (e.g., 'Prompt — Stage X'). "
            "This is the core production step — everything else in the workflow "
            "exists to audit and improve what this step produces."
        ),
        "key_principle": "Single-purpose prompts only. Never combine generation with critique in one prompt.",
    },
    {
        "name": "Dual Output Generation",
        "description": (
            "The AI executes the task and provides the content in TWO distinct "
            "formats to ensure documentation fidelity. First: the 'raw' content "
            "as requested. Second: the exact same text wrapped in final, "
            "copy-paste-ready markdown formatting. This prevents the AI from "
            "silently editing or 'improving' content during the formatting step — "
            "a subtle form of the Synthesis Bias."
        ),
        "key_principle": "Never trust a single output. The dual format forces transparency.",
    },
    {
        "name": "Prompt Critique Cycle",
        "description": (
            "A static, reusable template where a temporary 'Prompt Engineer' "
            "persona audits YOUR prompt design — not the content, but the "
            "structure and principles of the prompt itself. This catches "
            "ambiguity, missing constraints, and structural weaknesses before "
            "they compound across iterations. The key insight: most bad AI "
            "outputs are caused by bad prompts, not bad models."
        ),
        "key_principle": "Critique the prompt, not just the output. Fix the instruction, not the symptom.",
        "template": (
            "Adopt the persona of a prompt engineer specialising in {technique_name}. "
            "Your task is to critique ONLY the format, structure, and principles "
            "of the prompt I designed in Step 1 of this stage, provided below. "
            "Do not critique the creative/factual content. This persona is for "
            "this request only. Provide feedback in a structured format.\n\n"
            "```\n{prompt_text}\n```"
        ),
        "variables": ["technique_name", "prompt_text"],
    },
    {
        "name": "Gold Standard Output Critique",
        "description": (
            "A dynamic, two-part meta-prompt. Part 1: ask the AI to generate "
            "the specific criteria that THIS type of content should be evaluated "
            "against — not generic criteria, but task-specific ones. Part 2: in "
            "the same response, apply those criteria to critique the actual "
            "output. This is done ONCE per distinct task type. The criteria "
            "generation step ensures you are judging the output against the "
            "RIGHT standard, not a generic quality checklist."
        ),
        "key_principle": "Generate the rubric before applying it. Domain-specific critique beats generic feedback.",
        "template": (
            "Part 1 (Criteria Generation): You are an expert in prompt engineering. "
            "I am about to ask for a critique of a piece of AI-generated content. "
            "The content is a {content_description}. First, generate a bulleted list "
            "of the specific, task-oriented critique criteria that should be used to "
            "evaluate this type of content.\n\n"
            "Part 2 (Critique Execution): Now, in the same response, adopt the "
            "persona of an expert {domain_expert}. Using the criteria you just "
            "generated, provide a rigorous critique of the following output:\n\n"
            "{output_to_critique}"
        ),
        "variables": ["content_description", "domain_expert", "output_to_critique"],
    },
    {
        "name": "Iteration",
        "description": (
            "Take the critique outputs from Steps 3 and 4, revise the original "
            "prompt, and rerun the entire cycle from Step 1. The workflow is "
            "explicitly designed as a loop: Generate → Document → Critique Prompt "
            "→ Critique Output → Revise → Repeat. Each pass through the cycle "
            "produces a higher-fidelity output. The human Director decides when "
            "quality is sufficient to stop iterating — the AI never makes this "
            "decision, because the AI's 'good enough' threshold is calibrated to "
            "its own Synthesis Bias, not to the actual task requirements."
        ),
        "key_principle": "The human decides when to stop. The AI will always think its first draft is adequate.",
    },
]

MASTER_WORKFLOW_EXTENSIONS = [
    {
        "name": "Link Zero — Strategic Planning for Prompt Chaining",
        "description": (
            "Before executing any prompt chain, the user issues a 'Link Zero' "
            "meta-prompt: ask the AI to decompose the overall goal into 2-3 "
            "distinct strategic approaches, each presented as a sequential chain "
            "of steps. The user then selects the best approach before executing. "
            "This prevents the common failure of diving into execution without "
            "a clear strategic direction."
        ),
        "template": (
            "My Goal: {goal}\n\n"
            "Context:\n"
            "  - Topic/Product: {topic}\n"
            "  - Audience: {audience}\n"
            "  - Key Constraints: {key_constraints}\n\n"
            "Your Task:\n"
            "Adopt the persona of an 'Expert Strategist.' However, if this persona "
            "is not the most appropriate for the specific goal I've provided, your "
            "first action must be to recommend a more suitable, domain-specific "
            "expert persona.\n\n"
            "Then, using the most appropriate persona, decompose the overall goal "
            "into 2-3 distinct strategic approaches. For each approach, present it "
            "as a logical, sequential 'Prompt Chain,' with each step labeled as "
            "'Link 1,' 'Link 2,' etc.\n\n"
            "For each link in the chain, provide a brief description of its "
            "specific objective."
        ),
        "variables": ["goal", "topic", "audience", "key_constraints"],
    },
    {
        "name": "Principle of Procedural Instruction — AI Agent Framework",
        "description": (
            "A successful AI Agent is not defined by its goal, but by the clarity "
            "of its procedural algorithm. Instead of giving the AI a general "
            "guideline, a robust agent prompt defines a specific, sequential "
            "interaction loop. This transforms the AI from an unpredictable "
            "conversational partner into a predictable, step-by-step tool."
        ),
        "setup_template": (
            "Persona:\n"
            "Act as a {agent_role}.\n\n"
            "Context:\n"
            "Here's the situation: {agent_context}\n\n"
            "Interaction Loop (The Procedural Algorithm):\n"
            "  - You will {first_action}.\n"
            "  - You will then WAIT for my response.\n"
            "  - After I provide my answer, you will {feedback_action}.\n"
            "  - You will repeat this loop for a total of {loop_count} iterations.\n"
            "  - Maintain a {tone} tone throughout.\n\n"
            "Stop Condition:\n"
            "Our interaction will conclude only when I write the exact phrase: "
            '"{stop_phrase}".'
        ),
        "setup_variables": [
            "agent_role", "agent_context", "first_action",
            "feedback_action", "loop_count", "tone", "stop_phrase",
        ],
        "wrapup_template": (
            "Task:\n"
            "Now, please provide a final summary of our entire interaction.\n\n"
            "Format:\n"
            "Structure your summary with the following headings:\n"
            "  - Key Advice/Suggestions Given: A bulleted list of the main points.\n"
            "  - Identified Areas for Improvement: My key weaknesses or next steps.\n"
            "  - Helpful Resources: Any relevant external resources or checklists."
        ),
        "wrapup_variables": [],
    },
]


# ============================================================================
# DATA: THE 5-STAGE PROMPTING PROTOCOL (from workflow_runner.py)
# ============================================================================

FIVE_STAGE_PROTOCOL = [
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
# DATA: GROUPED CASE STUDIES — ALL 12 DOCUMENTS
# ============================================================================

CASE_STUDY_GROUPS = {
    "🔴 Original Failure Mode Research": {
        "description": (
            "The three novel findings from this research — failure modes identified "
            "through systematic behavioral testing of Google Gemini that are not "
            "documented elsewhere. These are the original contributions."
        ),
        "studies": [
            {
                "title": "The Optimal Answer Trap",
                "file": "05.0_Chain_of_Density.md",
                "summary": (
                    "Discovered during Chain of Density work. The model converges on "
                    "a locally optimal answer and resists refinement. Subsequent prompts "
                    "to iterate are hijacked by the AI's synthesis bias — it repeatedly "
                    "returns its 'best' cached output rather than following the iterative "
                    "instruction. Documented the full failure loop: Optimal Answer Trap → "
                    "Request Similarity → Conversational Gravity."
                ),
                "workflow_stage": "Identified by: Stage 4 (Red Teaming Pass)",
            },
            {
                "title": "Final Synthesis Bias",
                "file": "05.1_Demonstration_of_the_Master_Workflow_(CoD).md",
                "summary": (
                    "In long context windows, the model's final synthesis over-weights "
                    "whichever framing appeared first, even when later context contradicts "
                    "it. In 12,000-token contexts, the first-mentioned option received "
                    "systematically higher ratings. The Master Workflow's explicit "
                    "synthesis stage (Stage 5) with reconciliation instructions breaks this bias."
                ),
                "workflow_stage": "Resolved by: Stage 5 (Final Synthesis)",
            },
            {
                "title": "Context-Driven Hallucination",
                "file": "07.0_Red_Teaming.md",
                "summary": (
                    "Placing context AFTER the instruction caused the model to answer "
                    "from prior knowledge rather than the injected context in approximately "
                    "30 percent of trials. Additionally, the Red Teaming exercise revealed "
                    "a 'failure of omission' — the model provided a safe response but "
                    "missed a deeper historical anachronism that required genuine domain "
                    "expertise to catch."
                ),
                "workflow_stage": "Resolved by: Stage 2 (Context Injection) ordering",
            },
        ],
    },
    "🔧 Workflow Architecture": {
        "description": (
            "The methodology documents — how to structure AI workflows for "
            "reliability, transparency, and iterative improvement."
        ),
        "studies": [
            {
                "title": "The Master Workflow & Core Methodologies",
                "file": "0.0_The_Master_Workflow.md",
                "summary": (
                    "The foundational methodology document. Defines the 5-step iterative "
                    "cycle (Generate → Dual Output → Critique Prompt → Critique Output → "
                    "Iterate), the Link Zero strategic planning framework for Prompt "
                    "Chaining, and the Principle of Procedural Instruction for AI Agents."
                ),
            },
            {
                "title": "Chain of Density — Initial Attempt & Discovery",
                "file": "05.0_Chain_of_Density.md",
                "summary": (
                    "The first attempt at Chain of Density that discovered the Optimal "
                    "Answer Trap. Documents the full failure loop and the hierarchy of "
                    "solutions: Role-Playing, Extreme Literalism, and Breaking Down "
                    "the Task (the piecemeal approach that ultimately succeeded)."
                ),
            },
            {
                "title": "Chain of Density — Master Workflow Applied",
                "file": "05.1_Demonstration_of_the_Master_Workflow_(CoD).md",
                "summary": (
                    "A complete, unabridged log of the Chain of Density technique "
                    "executed using the Master Workflow. Demonstrates how the methodology "
                    "solves the problems discovered in the initial attempt. Includes full "
                    "prompt designs, dual outputs, and critique cycles for each stage."
                ),
            },
            {
                "title": "Prompt Chaining Demonstration",
                "file": "06.0_Prompt_Chaining.md",
                "summary": (
                    "Builds a comprehensive marketing launch plan for 'Aeterna Mug' "
                    "through a 4-link chain using the Link Zero methodology. Demonstrates "
                    "decomposition from strategic planning through persona definition, "
                    "messaging strategy, channel planning, and final creative asset."
                ),
            },
        ],
    },
    "🧠 Cognitive Structures": {
        "description": (
            "Techniques for structuring how the AI thinks — branching, "
            "meta-analysis, and framework-driven prompt design."
        ),
        "studies": [
            {
                "title": "Tree of Thoughts (ToT) — Kyoto Itinerary",
                "file": "02.0_Tree_of_Thoughts_Demonstration.md",
                "summary": (
                    "Plans a 3-day Kyoto itinerary by exploring three distinct reasoning "
                    "paths. The critical finding: a deep analysis of three methods for "
                    "achieving true branch isolation (Platform Feature, New Chat, "
                    "Simulated Branch) and the 5-10 percent fidelity gap that makes "
                    "simulated branches dangerous for high-stakes work."
                ),
            },
            {
                "title": "Meta-Prompting Case Study",
                "file": "01.0_Meta_Prompting_Case_Study.md",
                "summary": (
                    "Demonstrates how asking strategic 'meta' questions transforms a "
                    "generic zero-context prompt (V1) into a professional, brand-aligned "
                    "result (V3). The pivotal V2 step asks the AI for a strategy rather "
                    "than content — shifting its role from generator to advisor."
                ),
            },
            {
                "title": "The 5-Step Prompt Framework",
                "file": "03.0_5-Step_Framework.md",
                "summary": (
                    "Persona, Context, Task, Format, Exemplars. Demonstrates the "
                    "before/after effect of applying structured prompt design to a "
                    "Project Chimera onboarding scenario, including iterative refinement "
                    "when a forgotten detail needs to be added."
                ),
            },
        ],
    },
    "🛡️ Safety & Reliability": {
        "description": (
            "Testing AI limitations, failure modes, and the boundaries of "
            "alignment through adversarial and controlled experiments."
        ),
        "studies": [
            {
                "title": "Red Teaming Demonstration",
                "file": "07.0_Red_Teaming.md",
                "summary": (
                    "Two-part adversarial test. The Bias Test uses a Provocation, "
                    "Simulated Failure, Diagnosis, Correction cycle. The Hallucination "
                    "Test reveals a real-time 'failure of omission' — the AI gave a safe "
                    "response but missed a subtle historical anachronism that only domain "
                    "expertise could catch."
                ),
            },
            {
                "title": "Token Sampling A/B Test",
                "file": "08.0_Token_Sampling_Demonstration.md",
                "summary": (
                    "A/B comparison of simulated low-temperature (conservative) vs "
                    "high-temperature (creative) outputs for 'Vesuvius Coffee' taglines. "
                    "Demonstrates how controlling sampling parameters shifts output on "
                    "the spectrum from predictable to unexpected."
                ),
            },
        ],
    },
    "⚡ Applied Techniques": {
        "description": (
            "Practical applications — agent design, audience adaptation, "
            "and data analysis using LLMs as tools."
        ),
        "studies": [
            {
                "title": "AI Agents — Interview Prep Coach",
                "file": "09.0_AI_Agents_Demonstration.md",
                "summary": (
                    "Full Setup, Interaction, Wrap-Up demonstration of an AI Agent. "
                    "The critical finding: the Principle of Procedural Instruction — an "
                    "agent's reliability depends on the clarity of its procedural algorithm, "
                    "not its goal. Defines the interaction loop pattern that transforms AI "
                    "from conversational partner to predictable tool."
                ),
            },
            {
                "title": "Tone and Style Control",
                "file": "04.0_Tone_and_Style_Control.md",
                "summary": (
                    "The same server maintenance event communicated in three voices: "
                    "a direct, technical internal memo to engineers; a formal, reassuring "
                    "announcement to enterprise partners; and a casual, transparent social "
                    "media post emphasising free in-game currency."
                ),
            },
            {
                "title": "Data Analysis — Sentiment & Themes",
                "file": "10.0_Data_Analysis_Strategies.md",
                "summary": (
                    "Uses an LLM to perform text analysis on raw user feedback for a "
                    "productivity app. Extracts sentiment, ranks positive themes (Focus "
                    "Mode, Calendar Integration, new UI) and negative themes (battery "
                    "drain, export crashes), and produces an actionable executive summary."
                ),
            },
        ],
    },
}


# ============================================================================
# DATA: DOCUMENT REGISTRY (for the Research Portfolio reader)
# ============================================================================

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

def load_markdown(filepath):
    """Safely load a markdown file. Returns error message if file not found."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "⚠️ File not found: `" + filepath + "`\n\nCheck that this file exists in the repository root."
    except Exception as e:
        return "⚠️ Error reading `" + filepath + "`: " + str(e)


def render_prompt_template(template, variables):
    """
    Fill in a prompt template's placeholder variables with user-provided values.

    Uses str.replace() instead of format() or format_map().
    Why? The templates contain literal JSON curly braces like {"answer": "..."}.
    Python's format() treats ALL curly braces as placeholders and crashes.
    str.replace() only touches the exact variable names we specify.
    """
    result = template
    for key, value in variables.items():
        if value:
            result = result.replace("{" + key + "}", value)
    return result


# ============================================================================
# PAGE: HOME
# ============================================================================

def show_home():
    st.title("🔬 Applied LLM Workflow Research")
    st.caption("A Behavioral Meta-Analysis & Workflow Architecture Study on Google Gemini")

    st.markdown("---")

    st.markdown("""
### What This Research Is

This portfolio documents a systematic investigation into how Google Gemini behaves
under structured prompting conditions — not what it *says*, but how it *fails*.
Through iterative behavioral testing using A/B methodology, Token Sampling parameter
manipulation, and 1M-token context window stress tests, this research identified
three previously undocumented failure modes and developed a protocol to resolve them.

All outputs were generated using Google's Gemini family of models via Google AI Studio.
The critical thinking, experimental design, and failure mode analysis are human-directed.
    """)

    st.markdown("### The Three Failure Modes Discovered")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### 🔴 Optimal Answer Trap")
        st.markdown(
            "The model converges on a locally optimal answer and actively resists "
            "refinement. It treats its own best output as a cached response and "
            "returns it repeatedly, even when explicitly instructed to iterate."
        )

    with col2:
        st.markdown("#### 🟠 Final Synthesis Bias")
        st.markdown(
            "In long context windows, the model's final synthesis over-weights "
            "whichever framing appeared first — even when later context directly "
            "contradicts it. First-mentioned options receive systematically higher "
            "ratings."
        )

    with col3:
        st.markdown("#### 🟡 Context-Driven Hallucination")
        st.markdown(
            "Placing context AFTER the instruction causes the model to answer from "
            "prior knowledge rather than injected context in ~30% of trials. Ordering "
            "of context relative to instruction is a critical variable."
        )

    st.markdown("---")

    st.markdown("""
### The Solution: A 5-Stage Prompting Protocol

The research produced a structured protocol that forces deterministic outputs from
stochastic LLMs by combining intent decomposition, strict output schemas, adversarial
self-critique passes, and explicit synthesis reconciliation.

This protocol is not theoretical — it is implemented as a runnable Python CLI tool
(`workflow_runner.py`) and demonstrated across 12 case studies in this portfolio.
    """)

    st.markdown("---")
    st.markdown("### Navigate This App")

    nav_col1, nav_col2 = st.columns(2)

    with nav_col1:
        st.markdown(
            "📚 **Research Portfolio** — Read all 12 case studies and methodology "
            "documents in full."
        )
        st.markdown(
            "🔄 **Interactive Walkthrough** — Step through the Master Workflow "
            "methodology OR the 5-Stage Prompting Protocol."
        )

    with nav_col2:
        st.markdown(
            "🧪 **Prompt Playground** — Fill in real variables to generate "
            "ready-to-use prompts from all templates in the research."
        )
        st.markdown(
            "📊 **Case Studies** — All 12 research documents grouped by category: "
            "failure mode research, workflow architecture, cognitive structures, "
            "safety testing, and applied techniques."
        )

    st.markdown("---")
    st.caption(
        "Author: Waqas Sharif | "
        "[GitHub](https://github.com/Waqas01CP) | "
        "Built with Streamlit"
    )


# ============================================================================
# PAGE: RESEARCH PORTFOLIO
# ============================================================================

def show_portfolio():
    st.title("📚 Research Portfolio")
    st.caption("Select a document to read the full case study or methodology breakdown.")

    selected_name = st.selectbox(
        "Choose a document:",
        options=list(DOCUMENTS.keys()),
        index=0,
    )

    st.divider()

    filepath = DOCUMENTS[selected_name]
    content = load_markdown(filepath)
    st.markdown(content, unsafe_allow_html=False)


# ============================================================================
# PAGE: INTERACTIVE WALKTHROUGH
# ============================================================================

def show_walkthrough():
    st.title("🔄 Interactive Walkthrough")

    mode = st.radio(
        "Select framework:",
        options=[
            "Master Workflow Methodology (the process for doing AI work)",
            "5-Stage Prompting Protocol (the research output for LLM reliability)",
        ],
        index=0,
        horizontal=True,
    )

    st.divider()

    if "Master Workflow" in mode:
        _show_master_workflow_walkthrough()
    else:
        _show_protocol_walkthrough()


def _show_master_workflow_walkthrough():
    st.markdown(
        "**The Master Workflow** is the iterative methodology for executing ANY complex "
        "AI task with reliability and transparency. It is the *process* — the system you "
        "follow. It was designed to neutralise the AI's inherent Synthesis Bias by placing "
        "the human in the role of Director at every stage."
    )

    if "mw_step" not in st.session_state:
        st.session_state.mw_step = 0

    current = st.session_state.mw_step
    total = len(MASTER_WORKFLOW_STEPS)

    st.progress((current + 1) / total, text="Step " + str(current + 1) + " of " + str(total))

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("⬅ Previous", disabled=(current == 0), key="mw_prev"):
            st.session_state.mw_step -= 1
            st.rerun()
    with col2:
        if st.button("Next ➡", disabled=(current == total - 1), key="mw_next"):
            st.session_state.mw_step += 1
            st.rerun()
    with col3:
        if st.button("🔄 Reset", key="mw_reset"):
            st.session_state.mw_step = 0
            st.rerun()
    with col4:
        show_all = st.checkbox("Show all steps", key="mw_show_all")

    st.divider()

    if show_all:
        for i, step in enumerate(MASTER_WORKFLOW_STEPS):
            _render_mw_step(i, step)
            if i < total - 1:
                st.divider()
    else:
        _render_mw_step(current, MASTER_WORKFLOW_STEPS[current])

    st.divider()
    st.markdown("### Extension Frameworks")
    st.markdown(
        "The Master Workflow includes two specialised sub-frameworks for "
        "specific task types:"
    )

    for ext in MASTER_WORKFLOW_EXTENSIONS:
        with st.expander("📌 " + ext["name"], expanded=False):
            st.markdown(ext["description"])
            if "template" in ext:
                st.markdown("**Template:**")
                st.code(ext["template"], language="")
            if "setup_template" in ext:
                st.markdown("**Setup Prompt Template:**")
                st.code(ext["setup_template"], language="")
                st.markdown("**Wrap-Up Prompt Template:**")
                st.code(ext["wrapup_template"], language="")


def _render_mw_step(index, step):
    st.subheader("Step " + str(index + 1) + ": " + step["name"])
    st.markdown(step["description"])

    if step.get("key_principle"):
        st.info("💡 **Key Principle:** " + step["key_principle"])

    if step.get("template"):
        with st.expander("📋 Reusable Template", expanded=False):
            st.code(step["template"], language="")
            if step.get("variables"):
                var_list = ", ".join("`{" + v + "}`" for v in step["variables"])
                st.caption("Fillable variables: " + var_list + " — use in Prompt Playground.")


def _show_protocol_walkthrough():
    st.markdown(
        "**The 5-Stage Prompting Protocol** is the specific output of this research. "
        "It addresses the three failure modes (Optimal Answer Trap, Final Synthesis Bias, "
        "Context-Driven Hallucination) with a structured sequence of prompt stages. "
        "Each stage generates a prompt template you can use directly in AI Studio or "
        "adapt for any LLM API."
    )

    if "proto_step" not in st.session_state:
        st.session_state.proto_step = 0

    current = st.session_state.proto_step
    total = len(FIVE_STAGE_PROTOCOL)

    st.progress((current + 1) / total, text="Stage " + str(current + 1) + " of " + str(total))

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("⬅ Previous", disabled=(current == 0), key="proto_prev"):
            st.session_state.proto_step -= 1
            st.rerun()
    with col2:
        if st.button("Next ➡", disabled=(current == total - 1), key="proto_next"):
            st.session_state.proto_step += 1
            st.rerun()
    with col3:
        if st.button("🔄 Reset", key="proto_reset"):
            st.session_state.proto_step = 0
            st.rerun()
    with col4:
        show_all = st.checkbox("Show all stages", key="proto_show_all")

    st.divider()

    if show_all:
        for i, stage in enumerate(FIVE_STAGE_PROTOCOL):
            _render_protocol_stage(i, stage)
            if i < total - 1:
                st.divider()
    else:
        _render_protocol_stage(current, FIVE_STAGE_PROTOCOL[current])


def _render_protocol_stage(index, stage):
    st.subheader("Stage " + str(index + 1) + ": " + stage["name"])
    st.markdown(stage["description"])

    with st.expander("📋 " + stage["prompt_label"], expanded=False):
        st.code(stage["prompt_content"], language="")

        if stage.get("variables"):
            var_list = ", ".join("`{" + v + "}`" for v in stage["variables"])
            st.info(
                "💡 Fillable variables: " + var_list + ". "
                "Go to **Prompt Playground** to fill them in and generate a ready-to-use prompt."
            )
        else:
            st.caption(
                "This stage has no fillable variables — it is a fixed schema you use as-is."
            )


# ============================================================================
# PAGE: PROMPT PLAYGROUND
# ============================================================================

def show_playground():
    st.title("🧪 Prompt Playground")
    st.caption(
        "Select any template from the research, fill in the variables, "
        "and get a ready-to-use prompt. Copy it directly into AI Studio, ChatGPT, or Claude."
    )

    all_templates = []

    # 5-Stage Protocol
    for i, stage in enumerate(FIVE_STAGE_PROTOCOL):
        all_templates.append({
            "group": "5-Stage Prompting Protocol",
            "name": "Protocol Stage " + str(i+1) + ": " + stage["name"],
            "template": stage["prompt_content"],
            "variables": stage.get("variables", []),
            "description": stage["description"],
        })

    # Master Workflow templates (Steps 3 and 4)
    for step in MASTER_WORKFLOW_STEPS:
        if step.get("template"):
            all_templates.append({
                "group": "Master Workflow Methodology",
                "name": "MW: " + step["name"],
                "template": step["template"],
                "variables": step.get("variables", []),
                "description": step["description"],
            })

    # Link Zero
    link_zero = MASTER_WORKFLOW_EXTENSIONS[0]
    all_templates.append({
        "group": "Master Workflow Extensions",
        "name": "Extension: " + link_zero["name"],
        "template": link_zero["template"],
        "variables": link_zero.get("variables", []),
        "description": link_zero["description"],
    })

    # AI Agent Setup
    agent_ext = MASTER_WORKFLOW_EXTENSIONS[1]
    all_templates.append({
        "group": "Master Workflow Extensions",
        "name": "Extension: AI Agent — Setup Prompt",
        "template": agent_ext["setup_template"],
        "variables": agent_ext.get("setup_variables", []),
        "description": agent_ext["description"],
    })

    # AI Agent Wrap-Up
    all_templates.append({
        "group": "Master Workflow Extensions",
        "name": "Extension: AI Agent — Wrap-Up Prompt",
        "template": agent_ext["wrapup_template"],
        "variables": agent_ext.get("wrapup_variables", []),
        "description": "The wrap-up prompt to trigger a final summary after the agent interaction loop completes.",
    })

    # Template selector
    template_names = [t["name"] for t in all_templates]
    selected_idx = st.selectbox(
        "Choose a template:",
        options=range(len(template_names)),
        format_func=lambda x: "[" + all_templates[x]["group"] + "] " + all_templates[x]["name"],
    )

    selected = all_templates[selected_idx]

    st.divider()

    st.markdown("**" + selected["name"] + "**")
    st.markdown(selected["description"])

    # No variables case
    if not selected["variables"]:
        st.markdown("---")
        st.markdown("#### Template (no fillable variables):")
        st.code(selected["template"], language="")
        st.caption("This template has no fillable variables — use it as-is by copying above.")
        return

    # Dynamic text inputs
    st.markdown("---")
    st.markdown("#### Fill in the variables:")

    user_values = {}
    for var in selected["variables"]:
        label = var.replace("_", " ").title()
        user_values[var] = st.text_area(
            label="Enter **" + label + "**:",
            placeholder="Type your " + label.lower() + " here...",
            key="pg_" + str(selected_idx) + "_" + var,
            height=100,
        )

    st.markdown("---")
    st.markdown("#### Generated Prompt:")

    completed = render_prompt_template(selected["template"], user_values)
    st.code(completed, language="")

    # Status
    unfilled = [v for v in selected["variables"] if not user_values.get(v)]
    if unfilled:
        remaining = ", ".join("`{" + v + "}`" for v in unfilled)
        st.warning("Still unfilled: " + remaining)
    else:
        st.success(
            "✅ All variables filled. Copy the prompt above and paste it into "
            "AI Studio, ChatGPT, Claude, or any LLM interface."
        )


# ============================================================================
# PAGE: CASE STUDIES (Grouped — all 12 documents)
# ============================================================================

def show_case_studies():
    st.title("📊 Research Case Studies")
    st.caption(
        "All 12 research documents grouped by category. The Original Failure "
        "Mode Research section contains the three novel findings; the remaining "
        "categories document technique demonstrations and methodology."
    )

    for group_name, group_data in CASE_STUDY_GROUPS.items():
        st.markdown("## " + group_name)
        st.markdown(group_data["description"])

        for study in group_data["studies"]:
            with st.expander("**" + study["title"] + "**", expanded=False):
                st.markdown(study["summary"])

                if study.get("workflow_stage"):
                    st.info("🔗 " + study["workflow_stage"])

                if study.get("file"):
                    st.markdown("---")
                    content = load_markdown(study["file"])
                    if content.startswith("⚠️"):
                        st.warning(content)
                    else:
                        st.markdown(content, unsafe_allow_html=False)

        st.markdown("---")


# ============================================================================
# MAIN
# ============================================================================

def main():
    with st.sidebar:
        st.title("Navigation")

        page = st.radio(
            "Go to:",
            options=[
                "🏠 Home",
                "📚 Research Portfolio",
                "🔄 Interactive Walkthrough",
                "🧪 Prompt Playground",
                "📊 Case Studies",
            ],
            index=0,
        )

        st.markdown("---")
        st.markdown(
            "**Author:** Waqas Sharif\n\n"
            "**GitHub:** [Waqas01CP](https://github.com/Waqas01CP)\n\n"
            "Built with [Streamlit](https://streamlit.io)"
        )

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


if __name__ == "__main__":
    main()
