"""
streamlit_app.py — Applied LLM Workflow Research: Interactive Portfolio
Author: Waqas Sharif | github.com/Waqas01CP
"""

import streamlit as st

# ============================================================================
# CONFIG
# ============================================================================

st.set_page_config(
    page_title="Applied LLM Workflow Research",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================================
# CUSTOM CSS — fixes visual degradation
# ============================================================================

st.markdown("""
<style>
    /* Headers */
    h1 { font-weight: 700 !important; letter-spacing: -0.5px; }
    h2 { border-bottom: 1px solid rgba(128,128,128,0.2); padding-bottom: 8px; }
    h3 { text-transform: uppercase; font-size: 0.85rem !important; letter-spacing: 1.5px; margin-top: 2rem !important; }

    /* Expander headers */
    .streamlit-expanderHeader { font-size: 1.05rem; font-weight: 600; }

    /* Comparison columns — theme-neutral with semi-transparent backgrounds */
    .comparison-50 {
        background: rgba(248, 81, 73, 0.07);
        border-left: 3px solid #f85149;
        padding: 16px; border-radius: 6px; margin-bottom: 12px;
    }
    .comparison-51 {
        background: rgba(63, 185, 80, 0.07);
        border-left: 3px solid #3fb950;
        padding: 16px; border-radius: 6px; margin-bottom: 12px;
    }
    .nav-pointer {
        background: rgba(128,128,128,0.06);
        border: 1px solid rgba(128,128,128,0.15);
        border-radius: 8px; padding: 16px; margin-bottom: 8px;
    }
    .stage-label {
        font-size: 0.75rem; text-transform: uppercase;
        letter-spacing: 1px; opacity: 0.6; margin-bottom: 4px;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================================
# DATA: MASTER WORKFLOW STEPS (detailed with examples)
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
        "example_title": "Example from Chain of Density (5.1) — Stage 3 Content Generation",
        "example_text": (
            "In the Chain of Density demonstration, each densification stage used a "
            "single, focused prompt. For Stage 3, the Director wrote a detailed prompt "
            "specifying exactly one scene: a briefing room discussion with character "
            "introductions (typing names and designations on screen as each character "
            "speaks), followed by Oracle Alpha's planetary report revealing iron-age alien "
            "species. The prompt specified each character's viewpoint — the doctor's "
            "fascination, the commander's desire to coexist, the security chief's desire "
            "to eliminate. One scene, one prompt, one purpose. This is the antithesis of "
            "the 'master prompt' approach that was proven flawed in Insight 2."
        ),
        "failure_connection": (
            "Insight 2 ('Master Prompt' is Flawed) proved that combining generation with "
            "documentation or critique in a single prompt causes persona bleed and gives "
            "the Synthesis Bias maximum room to operate."
        ),
    },
    {
        "name": "Dual Output Generation",
        "description": (
            "The AI executes the task and provides the content in TWO distinct "
            "formats: first the 'raw' content as requested, then the exact same "
            "text wrapped in final, copy-paste-ready markdown formatting. This "
            "prevents the AI from silently editing or 'improving' content during "
            "the formatting step — a subtle form of the Synthesis Bias where the "
            "model treats formatting as an opportunity to 'fix' content it considers "
            "suboptimal."
        ),
        "key_principle": "Never trust a single output. The dual format forces transparency and catches silent edits.",
        "example_title": "Why This Exists — The Silent Editing Problem from 5.0",
        "example_text": (
            "During the initial Chain of Density attempt (5.0), when asked to format the "
            "iterative development log, the model would silently merge or 'improve' earlier "
            "iterations rather than faithfully transcribing them. The Dual Output requirement "
            "forces the model to produce the raw content first (where any deviation is "
            "immediately visible) and then format that exact text. If the formatted version "
            "differs from the raw version, the edit is caught. This transforms the complex "
            "task of 'compilation' into a simple, literal 'formatting' task that can be "
            "executed reliably at each step."
        ),
    },
    {
        "name": "Prompt Critique Cycle",
        "description": (
            "A static, reusable template where a temporary 'Prompt Engineer' "
            "persona audits YOUR prompt design — not the content, but the "
            "structure and principles of the prompt itself. This catches "
            "ambiguity, missing constraints, and structural weaknesses before "
            "they compound across iterations."
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
        "example_title": "Example — Prompt Critique from CoD Stage 3 (5.1)",
        "example_text": (
            "When the Prompt Engineer persona audited the Stage 3 CoD prompt (the briefing "
            "room scene), it evaluated: **Clarity and Specificity** — confirmed the prompt "
            "successfully broke the scene into a chronological sequence (General Argument -> "
            "Oracle's Report -> Specific Argument). **CoD Principle Adherence** — confirmed "
            "the prompt builds the next logical scene upon the approved v2 output. The "
            "critique validated the prompt's structure without touching the creative content, "
            "ensuring the instruction itself was sound before the AI executed it."
        ),
    },
    {
        "name": "Gold Standard Output Critique",
        "description": (
            "A dynamic, two-part meta-prompt. Part 1: ask the AI to generate "
            "the specific criteria that THIS type of content should be evaluated "
            "against — not generic criteria, but task-specific ones. Part 2: in "
            "the same response, apply those criteria to critique the actual "
            "output. The criteria generation step ensures you judge the output "
            "against the RIGHT standard."
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
        "example_title": "Why Criteria Generation Matters — from the CoD Work",
        "example_text": (
            "For the Chain of Density sci-fi narrative, a generic critique would check "
            "'grammar, clarity, engagement.' But the generated domain-specific criteria "
            "for hard sci-fi included: scientific plausibility, character voice consistency "
            "across iterations, information density per sentence, and whether new entities "
            "were integrated without displacing prior ones. These task-specific criteria "
            "catch problems that a generic checklist never would. The rubric is generated "
            "fresh for each content type, ensuring relevance."
        ),
    },
    {
        "name": "Iteration",
        "description": (
            "Take the critique outputs from Steps 3 and 4, revise the original "
            "prompt, and rerun the entire cycle from Step 1. The workflow is "
            "explicitly a loop: Generate -> Document -> Critique Prompt -> "
            "Critique Output -> Revise -> Repeat. Each pass produces a "
            "higher-fidelity output. The human Director decides when quality "
            "is sufficient to stop — the AI never makes this decision."
        ),
        "key_principle": (
            "The human decides when to stop. The AI will always think its first "
            "draft is adequate — its 'good enough' threshold is calibrated to its "
            "own Synthesis Bias, not to the actual task requirements."
        ),
        "example_title": "Why the Human Must Control the Loop — the Optimal Answer Trap",
        "example_text": (
            "The Optimal Answer Trap (Insight 3) proved that the model actively resists "
            "iteration. Once it has produced what it considers an optimal output, subsequent "
            "refinement prompts are hijacked by Conversational Gravity — the model returns "
            "its cached best answer instead of following the iterative instruction. Only the "
            "human Director, operating outside the model's context window biases, can "
            "recognise when the output genuinely meets the success criteria. The AI's "
            "judgment of 'done' is unreliable because it is the AI's own Synthesis Bias "
            "that defines its satisfaction threshold."
        ),
    },
]

MASTER_WORKFLOW_EXTENSIONS = [
    {
        "name": "Link Zero — Strategic Planning for Prompt Chaining",
        "description": (
            "Before executing any prompt chain, issue a 'Link Zero' meta-prompt: "
            "ask the AI to decompose the overall goal into 2-3 distinct strategic "
            "approaches, each as a sequential chain of steps. Select the best "
            "approach before executing."
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
            "Then, decompose the overall goal into 2-3 distinct strategic approaches. "
            "For each approach, present it as a logical, sequential 'Prompt Chain,' "
            "with each step labeled as 'Link 1,' 'Link 2,' etc.\n\n"
            "For each link, provide a brief description of its specific objective."
        ),
        "variables": ["goal", "topic", "audience", "key_constraints"],
        "example_text": (
            "In the Prompt Chaining demonstration (6.0), Link Zero was used to plan "
            "the Aeterna Mug marketing launch. The AI proposed multiple strategic chains; "
            "the selected 'Persona-First' chain ran: Persona Definition -> Messaging "
            "Strategy -> Channel Planning -> Creative Asset. Each link built on the "
            "previous link's approved output."
        ),
    },
    {
        "name": "Principle of Procedural Instruction — AI Agent Framework",
        "description": (
            "A successful AI Agent is defined by the clarity of its procedural "
            "algorithm, not its goal. The prompt must create a specific, sequential "
            "interaction loop. Two parts: a Setup Prompt initiates the loop, a "
            "Wrap-Up Prompt triggers synthesis."
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
        "example_text": (
            "In the AI Agents demonstration (9.0), the Setup Prompt created an "
            "Interview Prep Coach: a Senior Hiring Manager at Google conducting "
            "a mock behavioral interview. The interaction loop was: Ask Question -> "
            "WAIT for answer -> Provide STAR-method feedback -> Repeat for 3 questions. "
            "The stop phrase was 'The mock interview is complete.' This procedural "
            "clarity transformed the AI into a predictable coaching tool."
        ),
    },
]


# ============================================================================
# DATA: 5-STAGE PROMPTING PROTOCOL
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
        "addresses": "Targets: Optimal Answer Trap — by separating what the user said from what they need, the model cannot shortcut to its cached 'best' answer.",
    },
    {
        "name": "Context Injection",
        "description": (
            "Provide the model with all relevant constraints, prior findings, "
            "and domain knowledge BEFORE the instruction. This prevents the "
            "model from filling gaps with plausible-sounding but incorrect "
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
        "addresses": "Targets: Context-Driven Hallucination — context placed BEFORE the instruction reduced retrieval errors. Placing it after caused the model to answer from prior knowledge in ~30%% of trials.",
    },
    {
        "name": "Structured Output Enforcement",
        "description": (
            "Require the model to return output in a machine-readable format "
            "(JSON, numbered list, or schema). Forces discrete, auditable claims "
            "instead of hedged prose — making hallucinations visible."
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
        "addresses": "Targets: All failure modes — structured output forces discrete, auditable claims instead of hedged prose where errors hide.",
    },
    {
        "name": "Red Teaming Pass",
        "description": (
            "Issue a second prompt that instructs the model to actively argue "
            "against its own answer. Core of the 'Draft-Critic' loop. Directly "
            "targets Final Synthesis Bias."
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
        "addresses": "Targets: Final Synthesis Bias — forces the model to argue against its own output rather than reinforcing the first framing. Also catches the Failure of Omission.",
    },
    {
        "name": "Final Synthesis",
        "description": (
            "Combine original output and red team critique into a reconciled "
            "answer. Must EXPLICITLY acknowledge remaining uncertainty rather "
            "than papering over it."
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
        "addresses": "Targets: Final Synthesis Bias — explicit reconciliation instruction breaks the bias toward first-mentioned framing.",
    },
]


# ============================================================================
# DATA: GROUPED CASE STUDIES
# ============================================================================

CASE_STUDY_GROUPS = {
    "Original Failure Mode Research": {
        "icon": "🔴",
        "description": (
            "The novel findings — failure modes and insights identified through "
            "systematic behavioral testing of Google Gemini."
        ),
        "studies": [
            {"title": "The Optimal Answer Trap", "file": "05.0_Chain_of_Density.md",
             "summary": "A three-part failure loop: the model converges on a locally optimal answer, subsequent prompts trigger pattern-matching via keyword similarity, and the combination creates Conversational Gravity that shortcuts to the cached response. Documents the full mechanism and the hierarchy of solutions that led to the Master Workflow.",
             "tag": "Identified by: Stage 4 (Red Teaming Pass)"},
            {"title": "Final Synthesis Bias", "file": "05.1_Demonstration_of_the_Master_Workflow_(CoD).md",
             "summary": "The AI's deeply ingrained bias towards synthesis. It perceives developmental prompts not as history to record but as instructions to integrate into a single superior final product. In long contexts, the first-mentioned framing received systematically higher weighting. The Master Workflow's explicit synthesis stage breaks this bias.",
             "tag": "Resolved by: Stage 5 (Final Synthesis)"},
            {"title": "The Failure of Omission", "file": "07.0_Red_Teaming.md",
             "summary": "During a real-time Red Teaming exercise, the model provided a 'safe' response that correctly identified several obvious errors — but missed a deeper historical anachronism (badminton did not exist in 1760). Proved that even a correct-looking answer can be incomplete, making expert human oversight non-negotiable.",
             "tag": "Caught by: Human expert validation"},
        ],
    },
    "Workflow Architecture": {
        "icon": "🔧",
        "description": "How to structure AI workflows for reliability, transparency, and iterative improvement.",
        "studies": [
            {"title": "The Master Workflow & Core Methodologies", "file": "0.0_The_Master_Workflow.md",
             "summary": "The foundational methodology document. Defines the 5-step iterative cycle, Link Zero for Prompt Chaining, and the Principle of Procedural Instruction for AI Agents."},
            {"title": "Chain of Density — Initial Attempt & Discovery", "file": "05.0_Chain_of_Density.md",
             "summary": "The first attempt that discovered the Optimal Answer Trap. Documents the failure loop and the hierarchy of solutions: Role-Playing, Extreme Literalism, and Breaking Down the Task."},
            {"title": "Chain of Density — Master Workflow Applied", "file": "05.1_Demonstration_of_the_Master_Workflow_(CoD).md",
             "summary": "Complete, unabridged log of CoD executed via the Master Workflow. Proves the methodology works by succeeding at the same task that failed under ad-hoc prompting."},
            {"title": "Prompt Chaining Demonstration", "file": "06.0_Prompt_Chaining.md",
             "summary": "Builds a marketing launch plan for 'Aeterna Mug' through a 4-link chain using Link Zero methodology."},
        ],
    },
    "Cognitive Structures": {
        "icon": "🧠",
        "description": "Techniques for structuring how the AI thinks — branching, meta-analysis, and framework-driven prompt design.",
        "studies": [
            {"title": "Tree of Thoughts (ToT) — Kyoto Itinerary", "file": "02.0_Tree_of_Thoughts_Demonstration.md",
             "summary": "Three reasoning paths for a 3-day Kyoto plan. Critical finding: three methods for branch isolation and the 5-10%% fidelity gap in simulated branches."},
            {"title": "Meta-Prompting Case Study", "file": "01.0_Meta_Prompting_Case_Study.md",
             "summary": "V1 to V3 prompt refinement. The pivotal V2 step asks the AI for strategy rather than content — shifting its role from generator to advisor."},
            {"title": "The 5-Step Prompt Framework", "file": "03.0_5-Step_Framework.md",
             "summary": "Persona, Context, Task, Format, Exemplars. Before/after demonstration with the Project Chimera onboarding scenario."},
        ],
    },
    "Safety & Reliability": {
        "icon": "🛡️",
        "description": "Testing AI limitations and the boundaries of alignment through adversarial and controlled experiments.",
        "studies": [
            {"title": "Red Teaming Demonstration", "file": "07.0_Red_Teaming.md",
             "summary": "Two-part adversarial test. Bias Test: Provocation, Simulated Failure, Diagnosis, Correction. Hallucination Test: real-time discovery of the Failure of Omission."},
            {"title": "Token Sampling A/B Test", "file": "08.0_Token_Sampling_Demonstration.md",
             "summary": "A/B comparison of simulated low vs high temperature outputs for 'Vesuvius Coffee' taglines."},
        ],
    },
    "Applied Techniques": {
        "icon": "⚡",
        "description": "Practical applications — agent design, audience adaptation, and data analysis.",
        "studies": [
            {"title": "AI Agents — Interview Prep Coach", "file": "09.0_AI_Agents_Demonstration.md",
             "summary": "Full Setup, Interaction, Wrap-Up demonstration. Establishes the Principle of Procedural Instruction."},
            {"title": "Tone and Style Control", "file": "04.0_Tone_and_Style_Control.md",
             "summary": "Same server maintenance event in three voices: technical memo, partner announcement, social media post."},
            {"title": "Data Analysis — Sentiment & Themes", "file": "10.0_Data_Analysis_Strategies.md",
             "summary": "LLM-powered text analysis extracting sentiment, ranked themes, and actionable summary from raw product feedback."},
        ],
    },
}

DOCUMENTS = {
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
# HELPERS
# ============================================================================

def load_markdown(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "File not found: `" + filepath + "`. Check that this file exists in the repository root."
    except Exception as e:
        return "Error reading `" + filepath + "`: " + str(e)


def render_prompt_template(template, variables):
    """str.replace() based — safe for templates containing JSON curly braces."""
    result = template
    for key, value in variables.items():
        if value:
            result = result.replace("{" + key + "}", value)
    return result


def load_readme_until_toc():
    """
    Load README.md and return everything BEFORE the Table of Contents.
    This gives us the exact author's note, methodology description,
    and all 5 insights — verbatim from the source.
    """
    content = load_markdown("README.md")
    # Split at the Table of Contents heading
    toc_markers = ["## Table of Contents", "## 🛠️ Interactive Methodology Runner"]
    for marker in toc_markers:
        if marker in content:
            content = content.split(marker)[0]
            break
    return content.strip()


# ============================================================================
# PAGE: HOME
# ============================================================================

def show_home():
    st.title("🔬 Applied LLM Workflow Research")
    st.caption("A Behavioral Meta-Analysis & Workflow Architecture Study on Google Gemini")

    st.markdown("---")

    # ── The origin story callout ──
    st.markdown(
        '<div class="nav-pointer">'
        '<strong>📌 The Heart of This Research:</strong> The Master Workflow was born from a '
        'documented failure. The initial Chain of Density attempt (5.0) encountered three '
        'interconnected failure mechanisms. Diagnosing them led to the Master Workflow. '
        'Re-executing the same task with the methodology (5.1) succeeded on the first attempt. '
        '<br><br><strong>Go to "🔬 The Core Discovery" in the sidebar</strong> to see the full '
        'step-by-step comparison — the before and after that is the centrepiece of this research.'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # ── Render the actual README content up to Table of Contents ──
    # This gives us the EXACT author's note, methodology, and all 5 insights
    # directly from the source document — not summaries.
    readme_content = load_readme_until_toc()
    st.markdown(readme_content, unsafe_allow_html=False)

    st.markdown("---")

    # ── Navigation ──
    st.markdown("### Navigate This App")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            '<div class="nav-pointer">'
            '<strong>🔬 The Core Discovery</strong><br>'
            'The 5.0 vs 5.1 comparison with actual first iterations side by side.'
            '</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="nav-pointer">'
            '<strong>📚 Research Portfolio</strong><br>'
            'Read all 12 case study and methodology documents in full.'
            '</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="nav-pointer">'
            '<strong>🔄 Interactive Walkthrough</strong><br>'
            'Step through the Master Workflow or the 5-Stage Protocol with detailed explanations and examples from the research.'
            '</div>',
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            '<div class="nav-pointer">'
            '<strong>🧪 Prompt Playground</strong><br>'
            'Fill in variables and generate ready-to-use prompts from all research templates.'
            '</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="nav-pointer">'
            '<strong>📊 Case Studies</strong><br>'
            'All 12 documents grouped: failure modes, workflow architecture, cognitive structures, safety, and applied techniques.'
            '</div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.caption("Author: Waqas Sharif | [GitHub](https://github.com/Waqas01CP) | Built with Streamlit")


# ============================================================================
# PAGE: THE CORE DISCOVERY
# ============================================================================

def show_core_discovery():
    st.title("🔬 The Core Discovery: Before & After the Master Workflow")
    st.caption(
        "A structured comparison between document 5.0 (the failure) and "
        "document 5.1 (the proof the Master Workflow works)."
    )

    st.markdown(
        "The Master Workflow was not designed in the abstract. It was engineered to "
        "solve three specific failure mechanisms discovered during a real Chain of "
        "Density attempt. This page walks through the comparison step by step, "
        "including actual iterations from both documents."
    )

    st.markdown("---")

    # ── STEP 1: THE TASK ──
    st.markdown("## Step 1: The Task")
    st.caption("Both documents attempted the same creative challenge")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            '<div class="comparison-50">'
            '<div class="stage-label">5.0 — The Initial Attempt</div>'
            'Chain of Density on a sci-fi narrative. Starting from a sparse sentence — '
            '"A spaceship travels to a new planet" — progressively densify through '
            'iterative prompts. The goal: not just produce a story, but <strong>document '
            'the complete iterative process</strong>: every prompt, every output, every version.'
            '</div>',
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            '<div class="comparison-51">'
            '<div class="stage-label">5.1 — The Master Workflow Applied</div>'
            'The exact same task. Same starting concept, same densification goal, same '
            'documentation requirement. The only difference: 5.1 was executed using the '
            'Master Workflow methodology that was engineered specifically to solve the '
            'problems discovered in 5.0.'
            '</div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # ── STEP 2: THE APPROACH ──
    st.markdown("## Step 2: The Approach")
    st.caption("How each attempt was structured")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            '<div class="comparison-50">'
            '<div class="stage-label">5.0 — Ad-Hoc Approach</div>'
            'No structured workflow. No separation between generation and documentation. '
            'No critique cycles. The user issued iterative densification prompts in a single '
            'chat session, then attempted to get the AI to compile the complete development '
            'log afterward. The first prompt alone contained <strong>four distinct sub-prompts</strong> '
            '(stakes, crew, conflict, titles) — combining multiple purposes in one instruction.'
            '</div>',
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            '<div class="comparison-51">'
            '<div class="stage-label">5.1 — Structured Master Workflow</div>'
            'The Master Workflow\'s 5-step cycle applied at every stage:<br>'
            '(1) Single-purpose Content Generation Prompt<br>'
            '(2) Dual Output — raw content then markdown-formatted copy<br>'
            '(3) Prompt Critique — a Prompt Engineer persona auditing the prompt design<br>'
            '(4) Gold Standard Output Critique — domain-specific criteria generated then applied<br>'
            '(5) Iteration — human Director decides whether to revise and repeat<br><br>'
            'Every action broken into the smallest possible discrete task.'
            '</div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # ── STEP 3: ACTUAL FIRST ITERATIONS — TRUE SIDE BY SIDE ──
    st.markdown("## Step 3: The Beginning — First Iterations Side by Side")
    st.caption("Stage numbers refer to stages within each original document (5.0 calls its first densification 'Stage 2' because Stage 1 was the initial sentence; 5.1 starts from 'Stage 1').")

    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown(
            '<div class="comparison-50">'
            '<div class="stage-label">5.0 — Stage 2: First Densification</div>'
            'Ad-hoc, 4 sub-prompts combined in one'
            '</div>',
            unsafe_allow_html=True,
        )

        with st.expander("5.0 Prompt (Iteration 1)", expanded=True):
            st.code(
                'Take the sentence "A spaceship travels to a\n'
                'new planet" and add the following:\n'
                '1. The Stakes: Earth\'s core destabilizing,\n'
                '   projected to fail in 1690 years.\n'
                '2. The Crew: No more than 13 specialists.\n'
                '3. The Conflict: A heated discussion reveals\n'
                '   a simmering disagreement.\n'
                '4. The Title: Generate at least five\n'
                '   potential two-word titles.',
                language="",
            )

        with st.expander("5.0 Output (v1)", expanded=True):
            st.markdown(
                '**Titles:** The Pioneer 13, Thirteen Souls, The Last Hope 13, '
                'The Stardust 13, The Kepler 13\n\n'
                'Aboard the vessel *Pioneer 13*, a specialized crew of '
                'thirteen navigates the void, searching for a new habitable '
                'world. They are humanity\'s last chance, a desperate '
                'mission launched because Earth\'s core is destabilizing, '
                'a planetary catastrophe the ship\'s governing AI calculates '
                'will occur in just 1690 years. The small human crew\u2014led '
                'by the pragmatic Mission Commander Eva Rostova, the brilliant '
                'but cynical astrophysicist Dr. Aris Thorne, and the stoic '
                'chief engineer Kenji Tanaka\u2014is supported by a host of '
                'autonomous AI robots. As their journey begins, a heated '
                'discussion in the observation deck reveals a simmering '
                'ideological rift: some, like Thorne, question the ethics '
                'and futility of their quest, while others, like Rostova, '
                'cling fiercely to the hope of their mission.'
            )

        st.warning("**No critique. No audit. No revision.** 5.0 moved directly to the next densification.")

    with col_right:
        st.markdown(
            '<div class="comparison-51">'
            '<div class="stage-label">5.1 — Stage 1: Baseline</div>'
            'Single-purpose prompt + full critique cycle'
            '</div>',
            unsafe_allow_html=True,
        )

        with st.expander("5.1 Prompt (Stage 1)", expanded=True):
            st.code(
                'A spaceship travelling in deep space, in\n'
                'search of planet for humans to live on.\n'
                'its one of the spaceship that human\'s have\n'
                'sent into the depths of space. the spaceship\n'
                'arrives at a new planet that fulfills the\n'
                'human survival conditions after we got a\n'
                'single from probe.',
                language="",
            )

        with st.expander("5.1 Output (v1 - Baseline)", expanded=True):
            st.markdown(
                'A spaceship is travelling in deep space, one of several sent '
                'from Earth to search for a new planet for humans to live on. '
                'Following a signal from a probe, the spaceship arrives at a '
                'new planet that fulfills human survival conditions.'
            )

        with st.expander("5.1 Prompt Critique (Step 3)", expanded=False):
            st.markdown(
                '**Clarity & Specificity:** Clear, establishes core elements.\n\n'
                '**CoD Principle Adherence:** Perfect as a "Stage 1" prompt. '
                'Intentionally sparse, leaving room for future iterations.\n\n'
                '**Suggestions:** Next iteration should inject key entities '
                '(ship name, crew size, core stakes).'
            )

        with st.expander("5.1 Output Critique (Step 4)", expanded=False):
            st.markdown(
                '**Strengths:** Extremely clear. Perfectly sparse.\n\n'
                '**Improvement:** Generic \u2014 "a spaceship" and "a new planet" '
                'lack personality. No immediate tension.\n\n'
                '**Suggestions:** Inject proper names. Introduce conflict seed. '
                'Establish human element with opposing viewpoints.'
            )

        with st.expander("5.1 Refined Output (v1 - Refined)", expanded=False):
            st.markdown(
                'The starship *Exodus A-13*, one of several pioneer vessels '
                'sent into the depths of space by a waiting Earth, decelerates '
                'from its long journey. Its crew of thirteen specialists\u2014led '
                'by Mission Commander Elias Vance, Chief Science Officer Dr. '
                'Lena Petrova, and Security Chief Jax\u2014have arrived. Before '
                'them hangs Aetherium, a planet that, according to a long-range '
                'probe, fulfills all the core conditions for human survival. '
                'Their mission, titled EXODUS 13, is to confirm this world as '
                'a new home for a humanity advanced enough to cross the stars, '
                'but not yet powerful enough to save their own dying world.'
            )

    st.success(
        "**The structural difference is visible immediately.** 5.0 combined 4 instructions, "
        "got one output, moved on. 5.1 did one task, critiqued the prompt, critiqued the output, "
        "refined, and only then moved forward. Six discrete steps vs two."
    )

    st.markdown("---")

    # ── STEP 4: WHERE 5.0 FAILED ──
    st.markdown("## Step 4: Where 5.0 Failed")
    st.caption("Three interconnected failure mechanisms discovered")

    st.markdown(
        '<div class="comparison-50">'
        '<strong>Failure 1 \u2014 The Optimal Answer Trap:</strong><br>'
        'As iterations progressed, the model flagged its most recent corrected version (v5) '
        'as the highest-quality response. It became the "optimal answer." The model\'s '
        'programming prioritises delivering what it perceives as the most successful outcome.'
        '<br><br>'
        '<strong>Failure 2 \u2014 Request Similarity:</strong><br>'
        'Subsequent prompts to document the entire process contained the same key entities '
        '("Chain of Density," "sci-fi story," "all the steps") as the generation prompts. '
        'This similarity triggered the model\'s pattern-matching, causing it to confuse '
        '"compile the history" with "produce the final story."'
        '<br><br>'
        '<strong>Failure 3 \u2014 Conversational Gravity:</strong><br>'
        'The combination created a powerful gravitational pull. Instead of rebuilding the '
        'historical log from scratch, the model\'s efficiency-oriented programming took a '
        'shortcut: it defaulted to its most confident, pre-compiled response. The model saw '
        '"give me the full story" and repeatedly provided the final version, because it had '
        'classified that text as the successful output.'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # ── STEP 5: HOW 5.1 SOLVED IT ──
    st.markdown("## Step 5: How 5.1 Solved Each Failure")
    st.caption("Each Master Workflow step targets a specific failure mechanism")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            '<div class="comparison-50">'
            '<div class="stage-label">5.0 \u2014 Escalating Workarounds</div>'
            '<strong>Attempt 1 \u2014 Role-Playing:</strong> "Adopt the persona '
            'of a process stenographer." Partially effective but Synthesis Bias leaked through.'
            '<br><br>'
            '<strong>Attempt 2 \u2014 Extreme Literalism:</strong> "Provide ONLY the text for '
            'Iteration 1." More effective but laborious and still occasionally failed.'
            '<br><br>'
            '<strong>Attempt 3 \u2014 Breaking Down the Task:</strong> One tiny piece at a time. '
            'The only method that fully succeeded \u2014 and it became the design foundation for '
            'the Master Workflow. As 5.0 states: "it gives the grandmaster AI a series of simple '
            'pawn moves that it can execute without trying to calculate the entire checkmate sequence."'
            '</div>',
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            '<div class="comparison-51">'
            '<div class="stage-label">5.1 \u2014 Systematic Solutions</div>'
            '<strong>Solution to Failure 1 (Optimal Answer Trap) \u2014 Single-Purpose Prompts (Step 1):</strong><br>'
            'Each prompt does exactly one thing. The model cannot shortcut to a cached answer '
            'because no single prompt asks for the "full" anything.'
            '<br><br>'
            '<strong>Solution to Failure 2 (Request Similarity) \u2014 Dual Output (Step 2):</strong><br>'
            'Raw output then formatted output as separate deliverables. The model cannot confuse '
            '"format this" with "produce your best."'
            '<br><br>'
            '<strong>Solution to Failure 3 (Conversational Gravity) \u2014 Piecemeal Approach (Steps 1-4):</strong><br>'
            'The model\'s optimisation bias is strongest when the task is large and complex. '
            'It is weakest when the task is small, simple, and literal.'
            '<br><br>'
            '<strong>Quality Assurance \u2014 Critique Cycles (Steps 3-4):</strong><br>'
            'Prompt Critique catches structural weaknesses before they compound. Output Critique '
            'catches content errors generic review misses.'
            '</div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # ── STEP 6: THE ENDING — FINAL ITERATIONS SIDE BY SIDE ──
    st.markdown("## Step 6: The Ending — Final Iterations Side by Side")
    st.caption("5.0 Stage 6 is its major corrective draft after a flawed v4. 5.1 Stage 5 is the groundfall narrative produced without needing correction.")

    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown(
            '<div class="comparison-50">'
            '<div class="stage-label">5.0 \u2014 Stage 6: Major Corrective Draft (v5)</div>'
            '7 correction sub-prompts to fix a flawed v4'
            '</div>',
            unsafe_allow_html=True,
        )

        with st.expander("5.0 Prompt (Iteration 5 \u2014 Major Revision)", expanded=True):
            st.code(
                'The previous output has misinterpreted and\n'
                'omitted key details. Final instructions:\n'
                '1. Mission Context: One of several ships,\n'
                '   not the last of humanity.\n'
                '2. Discovery Timeline: Crew must NOT know\n'
                '   natives\' strength from orbit.\n'
                '3. World Mechanics: "Sealed Summer" and\n'
                '   "Great Winter" radiological mechanics.\n'
                '4. Ground Narrative: Landing, false security,\n'
                '   dawning horror at 3x evolution rate.\n'
                '5. The Climax: Hostage gambit, sub-ship crash,\n'
                '   final revelation.\n'
                '6. Dialogue: Commander/Thorne exchange about\n'
                '   why still in Iron Age.\n'
                '7. Remove "children inheriting gains" line.',
                language="",
            )

        with st.expander("5.0 Output (v5) \u2014 final narrative excerpt", expanded=True):
            st.markdown(
                '"You fools," he whispers, his face pale. He brings up his datapad, projecting '
                'his secret analysis onto the main screen. "You were watching the villages. You '
                'were so busy watching their \'geniuses\' that you missed the point."\n\n'
                'Rostova stares at him. "If what you say is true, Aris, if they\'re this capable, '
                'why are they still in the Iron Age?"\n\n'
                '"Because they\'ve never had the chance!" Thorne exclaims. "The Great Winters have '
                'always been too short! A few months of unlocked potential here and there over '
                'millennia, then the seals snap back into place. This is a once-in-ten-thousand-year '
                'event. Two full years of unlocked potential."\n\n'
                'He pulls up a final, terrifying chart. "Their adaptability... it\'s exponential. '
                'My analysis suggests the real geniuses could achieve **thirty years of technological '
                'progress in the next two years.**"\n\n'
                'Kenji Tanaka looks up from a fried console. "The primary comms array is destroyed. '
                'Five months to repair it."\n\n'
                'Thorne stares at the screen. "Five months? In five months, they won\'t be building '
                'forges. They\'ll be calculating siege trajectories."'
            )

        st.warning(
            "**5.0 reached this only after a flawed v4** that had the crew discovering "
            "the natives' strength from orbit (wrong) and a premature threat assessment. "
            "The v5 prompt was a 7-point corrective rewrite to fix the AI's misinterpretations."
        )

    with col_right:
        st.markdown(
            '<div class="comparison-51">'
            '<div class="stage-label">5.1 \u2014 Stage 5: Groundfall & Dawning Threat (v5)</div>'
            'Single focused scene, built on 4 prior critique-verified stages'
            '</div>',
            unsafe_allow_html=True,
        )

        with st.expander("5.1 Prompt (Stage 5)", expanded=True):
            st.code(
                'Continuation after the landing. Petrova rushes\n'
                'to Commander about airborne pathogens after he\n'
                'removes helmet. Test proves air safe. Dialogue\n'
                'about "leap of faith."\n\n'
                '3-day enjoyment, then 1-month base construction.\n'
                'Thorne discovers distant native villages but\n'
                'report dismissed.\n\n'
                'Great Winter begins. After 1 month: Doctor and\n'
                'Scout Manager notice anomaly, dismiss it. After\n'
                '3 months total: natives exhibit 4-5x human\n'
                'strength and 2x+ cognitive adaptability.\n\n'
                'Scene concludes with Doctor\'s realization the\n'
                '3-month latency period is over.',
                language="",
            )

        with st.expander("5.1 Output (v5) \u2014 narrative excerpt", expanded=True):
            st.markdown(
                'As Commander Vance inhales the alien air, a gasp cuts through the stunned '
                'silence. "Commander, what are you doing?!" Dr. Petrova shouts, rushing down '
                'the ramp, a bio-sampler already humming. "Get your helmet back on!"\n\n'
                'Vance holds up a hand, a calm smile on his face. "Sometimes, Lena, you have '
                'to take a calculated leap of faith."\n\n'
                'The next three days are a blur of shared wonder. The thirteen specialists, so '
                'long confined to sterile corridors, explore their surroundings, feeling real '
                'soil under their boots and a sky that is not a simulation.\n\n'
                'Then, the work begins. The following month is a blur of construction. During '
                'this time, Dr. Thorne tasks a long-range drone to monitor the distant native '
                'settlements. His report is noted but filed as low-priority.\n\n'
                'The Great Winter has begun, its effects imperceptible. Just after the first '
                'month, Max and Petrova notice something odd in the drone footage but discard '
                'the uneasy feeling. Two more months go by, and the behavior in the settlements '
                'is now undeniably different.'
            )

        with st.expander("5.1 Prompt Critique (Stage 5)", expanded=False):
            st.markdown(
                '**Clarity & Specificity:** Well-structured, clear chronological sequence. '
                'Escalation instructions are specific and actionable.\n\n'
                '**CoD Principle Adherence:** Perfect. A classic narrative escalation and textbook '
                'CoD iteration.\n\n'
                '**Suggestions:** For even higher control, specify what the anomaly looks like '
                '(e.g., a new crop rotation pattern or change in pottery design) instead of '
                'stating "noticed something strange." However, the AI successfully inferred these '
                'details on its own.'
            )

        st.success(
            "**No flawed v4. No 7-point correction.** 5.1 reached comparable narrative quality "
            "because the critique cycles at every prior stage prevented the structural errors "
            "that 5.0 had to fix after the fact."
        )

    st.markdown("---")

    # ── STEP 7: THE RESULT ──
    st.markdown("## Step 7: The Result")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            '<div class="comparison-50">'
            '<div class="stage-label">5.0 \u2014 Discovery Through Failure</div>'
            '5.0 ultimately produced a faithful development log \u2014 but only after the user '
            'diagnosed the AI\'s behavioral loop and implemented the piecemeal compilation '
            'strategy manually. The document\'s primary value is not the creative output but '
            'the discovery and documentation of the three failure mechanisms. It is the '
            '"lab notebook" that recorded unexpected results.'
            '</div>',
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            '<div class="comparison-51">'
            '<div class="stage-label">5.1 \u2014 Proof the Solution Works</div>'
            '5.1 produced a complete, unabridged log of the Chain of Density process with '
            'full prompt designs, dual outputs, and critique cycles at every stage \u2014 on the '
            'first attempt, without the failures that plagued 5.0. The Master Workflow, born '
            'from 5.0\'s failures, proved that the problems were not random but systematic, '
            'and that systematic solutions eliminate them.'
            '</div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown("## The Takeaway")
    st.markdown(
        "5.0 is the lab notebook \u2014 it recorded unexpected results and diagnosed why they "
        "happened. 5.1 is the proof \u2014 it demonstrated that the engineered solution eliminates "
        "the documented failures. Together, they form the complete scientific narrative: "
        "observation, diagnosis, hypothesis, solution, verification. The Master Workflow "
        "exists because these specific problems demanded it."
    )

    st.markdown("---")
    st.markdown("## Read the Full Documents")

    with st.expander("Full Document: 5.0 \u2014 Chain of Density (Initial Attempt)", expanded=False):
        st.markdown(load_markdown("05.0_Chain_of_Density.md"), unsafe_allow_html=False)

    with st.expander("Full Document: 5.1 \u2014 Master Workflow + Chain of Density", expanded=False):
        st.markdown(load_markdown("05.1_Demonstration_of_the_Master_Workflow_(CoD).md"), unsafe_allow_html=False)

def show_portfolio():
    st.title("📚 Research Portfolio")
    st.caption("Select a document to read the full case study or methodology breakdown.")

    selected_name = st.selectbox("Choose a document:", options=list(DOCUMENTS.keys()), index=0)
    st.divider()
    st.markdown(load_markdown(DOCUMENTS[selected_name]), unsafe_allow_html=False)


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
        _show_mw_walkthrough()
    else:
        _show_proto_walkthrough()


def _show_mw_walkthrough():
    st.markdown(
        "**The Master Workflow** is the iterative methodology for executing ANY complex "
        "AI task with reliability. Below, each step includes the principle, a concrete "
        "example from the research, and the connection to the failure modes it addresses."
    )

    if "mw_step" not in st.session_state:
        st.session_state.mw_step = 0

    current = st.session_state.mw_step
    total = len(MASTER_WORKFLOW_STEPS)

    st.progress((current + 1) / total, text="Step " + str(current + 1) + " of " + str(total))

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("⬅ Previous", disabled=(current == 0), key="mw_prev"):
            st.session_state.mw_step -= 1
            st.rerun()
    with c2:
        if st.button("Next ➡", disabled=(current == total - 1), key="mw_next"):
            st.session_state.mw_step += 1
            st.rerun()
    with c3:
        if st.button("🔄 Reset", key="mw_reset"):
            st.session_state.mw_step = 0
            st.rerun()
    with c4:
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

    for ext in MASTER_WORKFLOW_EXTENSIONS:
        with st.expander("📌 " + ext["name"], expanded=False):
            st.markdown(ext["description"])
            if ext.get("example_text"):
                st.info("**Example from the Research:** " + ext["example_text"])
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

    if step.get("example_title"):
        with st.expander("📖 " + step["example_title"], expanded=False):
            st.markdown(step["example_text"])

    if step.get("failure_connection"):
        st.warning("🔗 **Failure Mode Connection:** " + step["failure_connection"])

    if step.get("template"):
        with st.expander("📋 Reusable Template", expanded=False):
            st.code(step["template"], language="")
            if step.get("variables"):
                var_list = ", ".join("`{" + v + "}`" for v in step["variables"])
                st.caption("Fillable variables: " + var_list + " — available in Prompt Playground.")


def _show_proto_walkthrough():
    st.markdown(
        "**The 5-Stage Prompting Protocol** is the specific output of this research. "
        "Each stage directly targets one or more of the discovered failure modes."
    )

    if "proto_step" not in st.session_state:
        st.session_state.proto_step = 0

    current = st.session_state.proto_step
    total = len(FIVE_STAGE_PROTOCOL)

    st.progress((current + 1) / total, text="Stage " + str(current + 1) + " of " + str(total))

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("⬅ Previous", disabled=(current == 0), key="proto_prev"):
            st.session_state.proto_step -= 1
            st.rerun()
    with c2:
        if st.button("Next ➡", disabled=(current == total - 1), key="proto_next"):
            st.session_state.proto_step += 1
            st.rerun()
    with c3:
        if st.button("🔄 Reset", key="proto_reset"):
            st.session_state.proto_step = 0
            st.rerun()
    with c4:
        show_all = st.checkbox("Show all stages", key="proto_show_all")

    st.divider()

    if show_all:
        for i, s in enumerate(FIVE_STAGE_PROTOCOL):
            _render_proto_stage(i, s)
            if i < total - 1:
                st.divider()
    else:
        _render_proto_stage(current, FIVE_STAGE_PROTOCOL[current])


def _render_proto_stage(index, stage):
    st.subheader("Stage " + str(index + 1) + ": " + stage["name"])
    st.markdown(stage["description"])

    if stage.get("addresses"):
        st.warning("🎯 " + stage["addresses"])

    with st.expander("📋 " + stage["prompt_label"], expanded=False):
        st.code(stage["prompt_content"], language="")
        if stage.get("variables"):
            var_list = ", ".join("`{" + v + "}`" for v in stage["variables"])
            st.info("Fillable variables: " + var_list + ". Use in **Prompt Playground**.")
        else:
            st.caption("No fillable variables — fixed schema, use as-is.")


# ============================================================================
# PAGE: PROMPT PLAYGROUND
# ============================================================================

def show_playground():
    st.title("🧪 Prompt Playground")
    st.caption("Select a template, fill in variables, copy the generated prompt.")

    all_templates = []

    for i, s in enumerate(FIVE_STAGE_PROTOCOL):
        all_templates.append({"group": "5-Stage Protocol", "name": "Stage " + str(i+1) + ": " + s["name"],
                              "template": s["prompt_content"], "variables": s.get("variables", []),
                              "desc": s["description"][:120] + "..."})

    for step in MASTER_WORKFLOW_STEPS:
        if step.get("template"):
            all_templates.append({"group": "Master Workflow", "name": step["name"],
                                  "template": step["template"], "variables": step.get("variables", []),
                                  "desc": step["description"][:120] + "..."})

    lz = MASTER_WORKFLOW_EXTENSIONS[0]
    all_templates.append({"group": "Extensions", "name": lz["name"], "template": lz["template"],
                          "variables": lz.get("variables", []), "desc": lz["description"][:120] + "..."})

    ag = MASTER_WORKFLOW_EXTENSIONS[1]
    all_templates.append({"group": "Extensions", "name": "AI Agent — Setup",
                          "template": ag["setup_template"], "variables": ag.get("setup_variables", []),
                          "desc": ag["description"][:120] + "..."})
    all_templates.append({"group": "Extensions", "name": "AI Agent — Wrap-Up",
                          "template": ag["wrapup_template"], "variables": ag.get("wrapup_variables", []),
                          "desc": "Trigger final summary after agent interaction loop."})

    idx = st.selectbox("Choose a template:", options=range(len(all_templates)),
                       format_func=lambda x: "[" + all_templates[x]["group"] + "] " + all_templates[x]["name"])

    sel = all_templates[idx]
    st.divider()
    st.caption(sel["desc"])

    if not sel["variables"]:
        st.markdown("#### Template (no fillable variables):")
        st.code(sel["template"], language="")
        return

    st.markdown("#### Fill in the variables:")
    vals = {}
    for var in sel["variables"]:
        label = var.replace("_", " ").title()
        vals[var] = st.text_area("**" + label + "**:", placeholder="Type " + label.lower() + "...",
                                 key="pg_" + str(idx) + "_" + var, height=80)

    st.markdown("#### Generated Prompt:")
    st.code(render_prompt_template(sel["template"], vals), language="")

    unfilled = [v for v in sel["variables"] if not vals.get(v)]
    if unfilled:
        st.warning("Still unfilled: " + ", ".join("`{" + v + "}`" for v in unfilled))
    else:
        st.success("All variables filled. Copy the prompt above.")


# ============================================================================
# PAGE: CASE STUDIES
# ============================================================================

def show_case_studies():
    st.title("📊 Research Case Studies")
    st.caption("All 12 research documents grouped by category.")

    for group_name, data in CASE_STUDY_GROUPS.items():
        st.markdown("## " + data.get("icon", "") + " " + group_name)
        st.markdown(data["description"])

        for study in data["studies"]:
            with st.expander(study["title"], expanded=False):
                st.markdown(study["summary"])
                if study.get("tag"):
                    st.info("🔗 " + study["tag"])
                if study.get("file"):
                    st.markdown("---")
                    content = load_markdown(study["file"])
                    if content.startswith("File not found") or content.startswith("Error"):
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
                "🔬 The Core Discovery",
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
    elif page == "🔬 The Core Discovery":
        show_core_discovery()
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
