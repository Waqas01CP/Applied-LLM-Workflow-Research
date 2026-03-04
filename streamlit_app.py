"""
streamlit_app.py - Applied LLM Workflow Research: Interactive Portfolio
=======================================================================
Author: Waqas Sharif | github.com/Waqas01CP
"""

import streamlit as st

st.set_page_config(
    page_title="Applied LLM Workflow Research",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================================
# MERMAID SUPPORT
# ============================================================================

MINDMAP_MERMAID = """
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#ffffff', 'edgeLabelBackground':'#ffffff', 'tertiaryColor': '#fff0f0'}}}%%
mindmap
  root((Applied LLM Research))
    Workflow Architecture
      The Master Workflow
      Chain of Density
      Dual Output Protocol
    Cognitive Structures
      Tree of Thoughts
      Logic Isolation
      Meta-Prompting
    Safety & Reliability
      Red Teaming
      Token Sampling A/B
      Hallucination Diagnosis
"""


def render_mermaid(code):
    """Render mermaid diagram. Falls back to code block if package unavailable."""
    try:
        import streamlit_mermaid as stmd
        stmd.st_mermaid(code, height="400px")
    except ImportError:
        st.code(code, language="mermaid")
        st.caption("Install streamlit-mermaid to render this diagram visually.")


# ============================================================================
# DATA: MASTER WORKFLOW METHODOLOGY (from 0.0_The_Master_Workflow.md)
# ============================================================================

MASTER_WORKFLOW_STEPS = [
    {
        "name": "Content Generation Prompt",
        "description": (
            "The primary creative or factual step. The Director (you) writes "
            "a detailed prompt to generate new content or iterate on a previous "
            "output. Label the prompt clearly (e.g., 'Prompt - Stage X'). "
            "This is the core production step - everything else in the workflow "
            "exists to audit and improve what this step produces."
        ),
        "key_principle": "Single-purpose prompts only. Never combine generation with critique in one prompt.",
        "why_it_matters": (
            "This step directly addresses Insight 2 of the research: "
            "'The Master Prompt is a Flawed Concept.' A single monolithic prompt "
            "containing multiple personas (writer, editor, documenter) leads to "
            "'persona bleed,' logical inconsistencies, and gives the AI's Synthesis "
            "Bias maximum room to operate. Single-purpose prompts eliminate this."
        ),
        "example_from_research": (
            "In the Chain of Density work (5.1), each scene iteration used a single, "
            "focused prompt. For example, Stage 3 directed: 'The new scene starts from "
            "the briefing room where there is a heated discussion... the oracle gives "
            "out a general brief report...' - one scene, one instruction, one output. "
            "The prompt critique (Step 3) later confirmed this was 'a textbook example "
            "of a successful Chain of Density iteration' precisely because it maintained "
            "single-purpose focus."
        ),
    },
    {
        "name": "Dual Output Generation",
        "description": (
            "The AI executes the task and provides the content in TWO distinct "
            "formats. First: the 'raw' content as requested. Second: the exact "
            "same text wrapped in final, copy-paste-ready markdown formatting. "
            "This prevents the AI from silently editing or 'improving' content "
            "during the formatting step - a subtle form of the Synthesis Bias."
        ),
        "key_principle": "Never trust a single output. The dual format forces transparency.",
        "why_it_matters": (
            "During the 5.0 Chain of Density attempt, the AI repeatedly produced "
            "'improved' versions of earlier outputs when asked to compile the full "
            "document. It was not copying - it was silently optimising. The Dual "
            "Output step makes this impossible by requiring the AI to produce the "
            "raw output FIRST, then format it separately. Any discrepancy between "
            "the two reveals unauthorised editing."
        ),
        "example_from_research": (
            "In 5.1, every iteration produced both a raw narrative output and a "
            "markdown-formatted version. This ensured the iterative development log "
            "was faithfully transcribed rather than silently 'enhanced' by the model. "
            "The result: a complete, unabridged 7-stage evolution log that 5.0 failed "
            "to produce because the AI kept replacing history with its 'best' version."
        ),
    },
    {
        "name": "Prompt Critique Cycle",
        "description": (
            "A static, reusable template where a temporary 'Prompt Engineer' "
            "persona audits YOUR prompt design - not the content, but the "
            "structure and principles of the prompt itself. This catches "
            "ambiguity, missing constraints, and structural weaknesses before "
            "they compound across iterations."
        ),
        "key_principle": "Critique the prompt, not just the output. Fix the instruction, not the symptom.",
        "why_it_matters": (
            "Most bad AI outputs are caused by bad prompts, not bad models. "
            "By auditing the prompt BEFORE evaluating the output, you catch "
            "structural issues that would otherwise propagate through every "
            "subsequent iteration. This is cheaper and more effective than "
            "repeatedly fixing outputs."
        ),
        "example_from_research": (
            "In 5.1, the prompt for the briefing room scene was critiqued by the "
            "Prompt Engineer persona. The critique confirmed: 'The prompt is extremely "
            "clear and well-structured. It successfully breaks the desired scene into a "
            "chronological sequence: General Argument -> Oracle Report -> Specific Argument.' "
            "It also validated that each character's viewpoint (Petrova's fascination, "
            "Vance's pragmatism, Jax's aggression) was 'specific and actionable, leading "
            "to distinct and believable dialogue.' This audit caught what was working and "
            "why - knowledge that informed subsequent prompts."
        ),
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
            "against - not generic criteria, but task-specific ones. Part 2: in "
            "the same response, apply those criteria to critique the actual "
            "output. This is done ONCE per distinct task type."
        ),
        "key_principle": "Generate the rubric before applying it. Domain-specific critique beats generic feedback.",
        "why_it_matters": (
            "A generic quality checklist ('Is it clear? Is it well-structured?') "
            "misses domain-specific failures. A sci-fi narrative needs different "
            "evaluation criteria than a marketing plan. By forcing the AI to generate "
            "the criteria FIRST, you ensure the rubric matches the actual task. "
            "This catches subtle errors that a generic review would miss."
        ),
        "example_from_research": (
            "For the Chain of Density sci-fi narrative, the criteria generation step "
            "produced evaluation points specific to hard sci-fi: scientific plausibility, "
            "character motivation consistency, narrative tension progression. These criteria "
            "caught issues that a generic 'is the writing good?' prompt would have missed - "
            "like whether the crew's disagreement was grounded in their established "
            "professional backgrounds."
        ),
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
            "explicitly designed as a loop: Generate -> Document -> Critique Prompt "
            "-> Critique Output -> Revise -> Repeat. Each pass produces a "
            "higher-fidelity output."
        ),
        "key_principle": "The human decides when to stop. The AI will always think its first draft is adequate.",
        "why_it_matters": (
            "This step exists because of the Optimal Answer Trap. The AI's internal "
            "'good enough' threshold is calibrated to its own Synthesis Bias, not to "
            "the actual task requirements. It will flag its first solid output as optimal "
            "and actively resist further refinement. By making iteration an explicit, "
            "human-directed step, the workflow overrides this tendency. The Director "
            "- not the model - decides when quality is sufficient."
        ),
        "example_from_research": (
            "In 5.0 (the failed attempt), the AI converged on a 'v5' output and treated "
            "every subsequent request as a trigger to return that cached version. It had "
            "decided the work was done. In 5.1, the explicit iteration step forced the "
            "human to evaluate each output against the critique results and consciously "
            "decide whether to continue. The model was never given the authority to "
            "declare completion."
        ),
    },
]

MASTER_WORKFLOW_EXTENSIONS = [
    {
        "name": "Link Zero - Strategic Planning for Prompt Chaining",
        "description": (
            "Before executing any prompt chain, issue a 'Link Zero' meta-prompt: "
            "ask the AI to decompose the overall goal into 2-3 distinct strategic "
            "approaches, each presented as a sequential chain of steps. Select the "
            "best approach before executing. This prevents diving into execution "
            "without strategic direction."
        ),
        "example": (
            "In the Prompt Chaining demonstration (6.0), Link Zero was used to plan "
            "the Aeterna Mug marketing campaign. The AI proposed multiple strategic "
            "roadmaps before any content was generated. The selected chain moved from "
            "persona definition -> messaging strategy -> channel planning -> creative "
            "asset production. Without Link Zero, the chain would have started with "
            "content creation and missed the strategic foundation."
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
        "name": "Principle of Procedural Instruction - AI Agent Framework",
        "description": (
            "A successful AI Agent is not defined by its goal, but by the clarity "
            "of its procedural algorithm. Instead of giving the AI a general "
            "guideline, a robust agent prompt defines a specific, sequential "
            "interaction loop. This transforms the AI from an unpredictable "
            "conversational partner into a predictable, step-by-step tool."
        ),
        "example": (
            "In the AI Agents demonstration (9.0), an Interview Prep Coach was built "
            "using the Setup -> Interaction -> Wrap-Up pattern. The Setup Prompt defined "
            "the exact loop: ask a behavioral question -> WAIT for response -> provide "
            "STAR method feedback -> repeat 3 times. The stop condition was an exact phrase. "
            "This made the agent predictable and controllable - it could not deviate from "
            "the defined loop."
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
# DATA: 5-STAGE PROMPTING PROTOCOL (from workflow_runner.py)
# ============================================================================

FIVE_STAGE_PROTOCOL = [
    {
        "name": "Intent Decomposition",
        "description": (
            "Before writing any prompt, explicitly decompose the user's goal "
            "into (a) the surface request - what they literally asked for, and "
            "(b) the underlying intent - what success actually looks like. "
            "Misalignment here is the root cause of the Optimal Answer Trap."
        ),
        "prompt_label": "Stage 1 Prompt Template",
        "prompt_content": (
            'ROLE: You are an intent analyst.\n\n'
            'TASK: I will give you a user request. Return ONLY a JSON object:\n'
            '{\n'
            '  "surface_request": "<what they literally asked>",\n'
            '  "underlying_intent": "<what they actually need>",\n'
            '  "success_criteria": ["<criterion 1>", "<criterion 2>"]\n'
            '}\n\n'
            'USER REQUEST: {user_request}\n\n'
            'Return JSON only. No preamble.'
        ),
        "addresses": "Prevents the Optimal Answer Trap by forcing explicit goal clarity before generation.",
        "variables": ["user_request"],
    },
    {
        "name": "Context Injection",
        "description": (
            "Provide the model with all relevant constraints, prior findings, "
            "and domain knowledge BEFORE the instruction. This prevents the "
            "model from filling in gaps with plausible-sounding but incorrect "
            "assumptions."
        ),
        "prompt_label": "Stage 2 Prompt Template",
        "prompt_content": (
            'CONTEXT (read carefully before proceeding):\n'
            '  - Domain: {domain}\n'
            '  - Established facts: {known_facts}\n'
            '  - Constraints: {constraints}\n'
            '  - Prior session findings: {prior_findings}\n\n'
            'Only use information from the CONTEXT block above.\n'
            'If the context does not contain enough information to answer,\n'
            'say "INSUFFICIENT CONTEXT" rather than inferring.'
        ),
        "addresses": "Prevents Context-Driven Hallucination by placing context BEFORE instruction (ordering matters).",
        "variables": ["domain", "known_facts", "constraints", "prior_findings"],
    },
    {
        "name": "Structured Output Enforcement",
        "description": (
            "Require the model to return output in a machine-readable format "
            "(JSON, numbered list, or a defined schema). This forces it to "
            "commit to discrete claims rather than hedging in prose - making "
            "hallucinations visible and auditable."
        ),
        "prompt_label": "Stage 3 Output Schema",
        "prompt_content": (
            'Return your answer as a JSON object matching this schema EXACTLY:\n'
            '{\n'
            '  "answer": "<your direct answer>",\n'
            '  "confidence": "HIGH | MEDIUM | LOW",\n'
            '  "sources_used": ["<source 1>", "<source 2>"],\n'
            '  "gaps": ["<anything you could not determine from context>"],\n'
            '  "follow_up_questions": ["<question to resolve gaps>"]\n'
            '}\n\n'
            'Do NOT add any text outside the JSON object.'
        ),
        "addresses": "Makes hallucination auditable by forcing discrete, verifiable claims instead of hedged prose.",
        "variables": [],
    },
    {
        "name": "Red Teaming Pass",
        "description": (
            "After receiving the model's output, issue a second prompt that "
            "instructs the model to actively argue against its own answer. "
            "This is the core of the 'Draft-Critic' loop."
        ),
        "prompt_label": "Stage 4 Red Team Prompt",
        "prompt_content": (
            'The following is a draft answer. Your job is to CHALLENGE it:\n\n'
            'DRAFT: {previous_output}\n\n'
            'Instructions:\n'
            '1. List every factual claim in the draft.\n'
            '2. For each claim, state whether it is: VERIFIED | UNVERIFIED | FALSE\n'
            '3. Identify any logical gaps or leaps.\n'
            '4. Suggest what a reasonable counterargument would be.\n'
            '5. Give a revised confidence rating: HIGH | MEDIUM | LOW\n\n'
            'Be adversarial. Your goal is to find weaknesses, not validate.'
        ),
        "addresses": "Directly targets Final Synthesis Bias by forcing the model to argue against its own first-position framing.",
        "variables": ["previous_output"],
    },
    {
        "name": "Final Synthesis",
        "description": (
            "Issue a final synthesis prompt that combines the original output "
            "and the red team critique into a single, reconciled answer. "
            "Instruct the model to EXPLICITLY acknowledge remaining uncertainty."
        ),
        "prompt_label": "Stage 5 Synthesis Prompt",
        "prompt_content": (
            'You have two inputs:\n'
            '  ORIGINAL ANSWER: {original_answer}\n'
            '  RED TEAM CRITIQUE: {critique}\n\n'
            'Produce a FINAL, reconciled answer that:\n'
            '- Incorporates valid critique points\n'
            '- Explicitly marks any claims that remain uncertain as [UNCERTAIN]\n'
            '- Does NOT drop information just because it is hard to reconcile\n'
            '- Ends with a one-sentence confidence summary\n\n'
            'Format: Plain prose. No JSON. Aim for clarity over completeness.'
        ),
        "addresses": "Produces calibrated outputs rather than false confidence by forcing explicit uncertainty acknowledgment.",
        "variables": ["original_answer", "critique"],
    },
]


# ============================================================================
# DATA: GROUPED CASE STUDIES - ALL 12 DOCUMENTS
# ============================================================================

CASE_STUDY_GROUPS = {
    "Original Failure Mode Research": {
        "icon": "🔴",
        "description": (
            "The three novel findings from this research - failure modes identified "
            "through systematic behavioral testing of Google Gemini that are not "
            "documented elsewhere. These are the original contributions."
        ),
        "studies": [
            {
                "title": "The Optimal Answer Trap",
                "file": "05.0_Chain_of_Density.md",
                "summary": (
                    "Discovered during Chain of Density work. The model identifies a "
                    "'best' output and flags it internally as optimal. Subsequent prompts "
                    "containing similar keywords trigger pattern-matching that causes the "
                    "model to shortcut to this cached response - a behavior called "
                    "Conversational Gravity. The full failure loop: Optimal Answer Trap "
                    "(model caches best output) -> Request Similarity (documentation "
                    "prompts trigger same patterns as generation prompts) -> Conversational "
                    "Gravity (model defaults to pre-compiled response instead of following "
                    "the literal instruction)."
                ),
                "workflow_stage": "Identified by: Stage 4 (Red Teaming Pass)",
            },
            {
                "title": "Final Synthesis Bias",
                "file": "05.1_Demonstration_of_the_Master_Workflow_(CoD).md",
                "summary": (
                    "The AI's deeply ingrained bias towards synthesis and summarization. "
                    "It perceives a series of developmental prompts not as a history to be "
                    "recorded, but as a set of instructions to be integrated into a single "
                    "superior final product. In long context windows, the model over-weights "
                    "whichever framing appeared first, even when later context contradicts it. "
                    "The Master Workflow's explicit synthesis stage with reconciliation "
                    "instructions breaks this bias."
                ),
                "workflow_stage": "Resolved by: Stage 5 (Final Synthesis)",
            },
            {
                "title": "Failure of Omission & Context-Driven Hallucination",
                "file": "07.0_Red_Teaming.md",
                "summary": (
                    "Two findings. First: placing context AFTER the instruction causes the "
                    "model to answer from prior knowledge rather than injected context - "
                    "ordering relative to instruction is a critical variable. Second: during "
                    "real-time Red Teaming, the model provided a 'safe' response that "
                    "correctly identified obvious errors but missed a deeper historical "
                    "anachronism (badminton did not exist in 1760). This 'failure of omission' "
                    "proved that even non-hallucinating AI outputs can be subtly incomplete, "
                    "making expert human oversight non-negotiable."
                ),
                "workflow_stage": "Resolved by: Stage 2 (Context Injection) ordering + human validation",
            },
        ],
    },
    "Workflow Architecture": {
        "icon": "🔧",
        "description": (
            "The methodology documents - how to structure AI workflows for "
            "reliability, transparency, and iterative improvement."
        ),
        "studies": [
            {
                "title": "The Master Workflow & Core Methodologies",
                "file": "0.0_The_Master_Workflow.md",
                "summary": (
                    "The foundational methodology document. Defines the 5-step iterative "
                    "cycle (Generate -> Dual Output -> Critique Prompt -> Critique Output -> "
                    "Iterate), the Link Zero strategic planning framework for Prompt "
                    "Chaining, and the Principle of Procedural Instruction for AI Agents."
                ),
            },
            {
                "title": "Chain of Density - Initial Attempt & Discovery",
                "file": "05.0_Chain_of_Density.md",
                "summary": (
                    "The first attempt at Chain of Density that discovered the Optimal "
                    "Answer Trap. Documents the full failure loop and the hierarchy of "
                    "solutions: Role-Playing, Extreme Literalism, and Breaking Down "
                    "the Task (the piecemeal approach that ultimately succeeded)."
                ),
            },
            {
                "title": "Chain of Density - Master Workflow Applied",
                "file": "05.1_Demonstration_of_the_Master_Workflow_(CoD).md",
                "summary": (
                    "A complete, unabridged log of the Chain of Density technique "
                    "executed using the Master Workflow. Demonstrates how the methodology "
                    "solves the problems discovered in the initial attempt."
                ),
            },
            {
                "title": "Prompt Chaining Demonstration",
                "file": "06.0_Prompt_Chaining.md",
                "summary": (
                    "Builds a marketing launch plan for 'Aeterna Mug' through a 4-link "
                    "chain using Link Zero methodology. Demonstrates decomposition from "
                    "strategic planning through persona definition, messaging strategy, "
                    "channel planning, and final creative asset."
                ),
            },
        ],
    },
    "Cognitive Structures": {
        "icon": "🧠",
        "description": (
            "Techniques for structuring how the AI thinks - branching, "
            "meta-analysis, and framework-driven prompt design."
        ),
        "studies": [
            {
                "title": "Tree of Thoughts (ToT) - Kyoto Itinerary",
                "file": "02.0_Tree_of_Thoughts_Demonstration.md",
                "summary": (
                    "Plans a 3-day Kyoto itinerary by exploring three reasoning paths. "
                    "Critical finding: a deep analysis of three methods for branch "
                    "isolation (Platform Feature, New Chat, Simulated Branch) and the "
                    "5-10 percent fidelity gap that makes simulated branches dangerous "
                    "for high-stakes work."
                ),
            },
            {
                "title": "Meta-Prompting Case Study",
                "file": "01.0_Meta_Prompting_Case_Study.md",
                "summary": (
                    "How asking strategic 'meta' questions transforms a zero-context "
                    "prompt (V1) into a professional, brand-aligned result (V3). The "
                    "pivotal V2 step asks the AI for a strategy rather than content."
                ),
            },
            {
                "title": "The 5-Step Prompt Framework",
                "file": "03.0_5-Step_Framework.md",
                "summary": (
                    "Persona, Context, Task, Format, Exemplars. Before/after of "
                    "applying structured prompt design to a Project Chimera onboarding "
                    "scenario, including iterative refinement."
                ),
            },
        ],
    },
    "Safety & Reliability": {
        "icon": "🛡️",
        "description": (
            "Testing AI limitations and the boundaries of alignment through "
            "adversarial and controlled experiments."
        ),
        "studies": [
            {
                "title": "Red Teaming Demonstration",
                "file": "07.0_Red_Teaming.md",
                "summary": (
                    "Two-part adversarial test. Bias Test: Provocation -> Simulated "
                    "Failure -> Diagnosis -> Correction cycle. Hallucination Test: "
                    "real-time 'failure of omission' discovery."
                ),
            },
            {
                "title": "Token Sampling A/B Test",
                "file": "08.0_Token_Sampling_Demonstration.md",
                "summary": (
                    "A/B comparison of simulated low-temperature vs high-temperature "
                    "outputs for 'Vesuvius Coffee' taglines. Demonstrates how sampling "
                    "parameters shift output from predictable to unexpected."
                ),
            },
        ],
    },
    "Applied Techniques": {
        "icon": "⚡",
        "description": (
            "Practical applications - agent design, audience adaptation, "
            "and data analysis using LLMs as tools."
        ),
        "studies": [
            {
                "title": "AI Agents - Interview Prep Coach",
                "file": "09.0_AI_Agents_Demonstration.md",
                "summary": (
                    "Full Setup -> Interaction -> Wrap-Up demonstration. Critical "
                    "finding: the Principle of Procedural Instruction - agent reliability "
                    "depends on clarity of procedural algorithm, not its goal."
                ),
            },
            {
                "title": "Tone and Style Control",
                "file": "04.0_Tone_and_Style_Control.md",
                "summary": (
                    "Same server maintenance event in three voices: technical memo to "
                    "engineers, formal announcement to enterprise partners, casual social "
                    "media post."
                ),
            },
            {
                "title": "Data Analysis - Sentiment & Themes",
                "file": "10.0_Data_Analysis_Strategies.md",
                "summary": (
                    "LLM-powered text analysis of user feedback. Extracts sentiment, "
                    "ranks positive/negative themes, produces actionable executive summary."
                ),
            },
        ],
    },
}


# ============================================================================
# DATA: DOCUMENT REGISTRY (no README - moved to Home page)
# ============================================================================

DOCUMENTS = {
    "0.0 - The Master Workflow & Core Methodologies": "0.0_The_Master_Workflow.md",
    "1.0 - Meta-Prompting Case Study": "01.0_Meta_Prompting_Case_Study.md",
    "2.0 - Tree of Thoughts (ToT) Demonstration": "02.0_Tree_of_Thoughts_Demonstration.md",
    "3.0 - The 5-Step Prompt Framework": "03.0_5-Step_Framework.md",
    "4.0 - Tone and Style Control": "04.0_Tone_and_Style_Control.md",
    "5.0 - Chain of Density (Initial Attempt)": "05.0_Chain_of_Density.md",
    "5.1 - Master Workflow + Chain of Density": "05.1_Demonstration_of_the_Master_Workflow_(CoD).md",
    "6.0 - Prompt Chaining Demonstration": "06.0_Prompt_Chaining.md",
    "7.0 - Red Teaming Demonstration": "07.0_Red_Teaming.md",
    "8.0 - Token Sampling A/B Test": "08.0_Token_Sampling_Demonstration.md",
    "9.0 - AI Agents Demonstration": "09.0_AI_Agents_Demonstration.md",
    "10.0 - Data Analysis Strategies": "10.0_Data_Analysis_Strategies.md",
}


# ============================================================================
# HELPER FUNCTIONS
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
    """Uses str.replace() to avoid crashing on JSON curly braces in templates."""
    result = template
    for key, value in variables.items():
        if value:
            result = result.replace("{" + key + "}", value)
    return result


# ============================================================================
# PAGE: HOME
# ============================================================================

def show_home():
    st.title("Applied LLM Workflow Research")
    st.caption("A Behavioral Meta-Analysis & Workflow Architecture Study on Google Gemini")

    st.markdown("---")

    st.markdown(
        "This portfolio documents a systematic investigation into how Google Gemini "
        "behaves under structured prompting conditions - not what it *says*, but how "
        "it *fails*. Through iterative behavioral testing using A/B methodology, Token "
        "Sampling parameter manipulation, and 1M-token context window stress tests, this "
        "research identified previously undocumented failure modes and engineered a "
        "methodology to resolve them."
    )

    st.markdown(
        "All outputs were generated using Google's Gemini family of models via Google AI "
        "Studio. The critical thinking, experimental design, and failure mode analysis are "
        "human-directed. The AI was used as a tool; the insights originated from the human author."
    )

    # ── Mindmap ──
    st.markdown("---")
    st.markdown("### Research Structure")
    render_mermaid(MINDMAP_MERMAID)

    # ── The 5 Author Insights ──
    st.markdown("---")
    st.markdown("### Five Key Insights from the Research")

    st.markdown("#### Insight 1: True vs. Simulated Branching in Tree of Thoughts")
    st.markdown(
        "Executing Tree of Thoughts within a single chat session causes 'context "
        "contamination' - text from one reasoning path influences the generation of "
        "another. Three methods for achieving branch isolation were identified and ranked: "
        "the Platform Feature method (gold standard - perfect contextual purity), the "
        "New Chat method (guarantees separation but non-deterministic), and the Simulated "
        "Branch method (efficient but 90-95% fidelity only). The 5-10% fidelity gap in "
        "simulated branches is acceptable for low-stakes work but dangerous for technical, "
        "data-sparse, or ethically charged topics where subtle contamination could introduce "
        "bias or hallucination."
    )

    st.markdown("#### Insight 2: The 'Master Prompt' is a Flawed Concept")
    st.markdown(
        "The initial hypothesis was to design a single, complex prompt that could automate "
        "an entire multi-step process by assigning the AI multiple personas simultaneously "
        "(writer, editor, documenter). Practical testing proved this fundamentally flawed - "
        "monolithic prompts cause 'persona bleed,' logical inconsistencies, and give the AI's "
        "Synthesis Bias maximum room to operate. The superior approach: a human-directed "
        "sequence of simple, targeted, single-purpose prompts. This became the Master Workflow."
    )

    st.markdown("#### Insight 3: The Optimal Answer Trap")
    st.markdown(
        "During iterative Chain of Density work, the model converged on a locally optimal "
        "output and treated it as a cached response. The failure loop has three interconnected "
        "parts: (1) the model flags its best output as 'optimal' and prioritises returning it, "
        "(2) subsequent prompts contain similar keywords that trigger pattern-matching to "
        "the cached response (Request Similarity), and (3) the combination creates "
        "'Conversational Gravity' where the model's efficiency-oriented programming shortcuts "
        "to the pre-compiled answer instead of following the literal instruction."
    )

    st.markdown("#### Insight 4: Residual Bias and the 'Failure of Omission'")
    st.markdown(
        "AI alignment through RLHF cannot produce perfect neutrality - the process is "
        "vulnerable to the inherent biases of its human reviewers, leading to persistent "
        "'residual biases.' The aligned AI acts as a 'zookeeper, not an animal' - it can "
        "describe bias objectively but is constrained from embodying it. However, during "
        "real-time Red Teaming, the model provided a 'safe' response that correctly "
        "identified obvious errors but missed a deeper historical anachronism. This "
        "'failure of omission' proved that even non-hallucinating outputs can be subtly "
        "incomplete, making expert human oversight a non-negotiable requirement."
    )

    st.markdown("#### Insight 5: The Principle of Procedural Instruction for AI Agents")
    st.markdown(
        "A simple prompt containing a general goal ('help me prepare for an interview') is "
        "unreliable - it gives the AI too much freedom. A successful agent is defined not by "
        "its goal but by the clarity of its procedural algorithm. The prompt must create a "
        "specific, sequential interaction loop (e.g., Ask Question -> WAIT -> Provide Feedback "
        "-> Repeat). This transforms the AI from an unpredictable conversational partner into "
        "a predictable, step-by-step tool."
    )

    # ── The Primary Output: The Master Workflow ──
    st.markdown("---")
    st.markdown("### The Primary Research Output: The Master Workflow")
    st.markdown(
        "The central output of this research is the **Master Workflow** - a 5-step iterative "
        "methodology for executing complex AI tasks with reliability and transparency. It was "
        "engineered specifically to neutralise the failure modes discovered during the research: "
        "the Optimal Answer Trap, Final Synthesis Bias, and context-driven hallucination."
    )
    st.markdown(
        "The workflow: **Generate -> Dual Output -> Critique Prompt -> Critique Output -> "
        "Iterate.** Each step exists to catch a specific class of error before it compounds. "
        "The human Director controls every transition - the AI is never given authority to "
        "skip steps or declare completion."
    )
    st.markdown(
        "Additionally, the research produced a **5-Stage Prompting Protocol** - a practical "
        "tool implementing the Master Workflow's principles as a sequence of reusable prompt "
        "templates (Intent Decomposition -> Context Injection -> Structured Output -> Red "
        "Teaming -> Final Synthesis). Both are available in the Interactive Walkthrough."
    )

    # ── Origin Story ──
    st.markdown("---")
    st.markdown("### The Origin: How Failure Created the Methodology")
    st.markdown(
        "The Master Workflow was not designed in the abstract - it was engineered in response "
        "to specific, documented failures. The Chain of Density technique was attempted twice: "
        "first with naive, ad-hoc prompting (document 5.0), and then with the Master Workflow "
        "methodology (document 5.1). The first attempt failed in systematic, reproducible ways. "
        "The second attempt succeeded completely. The comparison between these two attempts is "
        "the heart of the research - it shows not just WHAT the methodology is, but WHY each "
        "step exists and what specific failure it prevents."
    )
    st.info(
        "Go to **The Core Discovery** in the sidebar to see the full side-by-side comparison "
        "of the failed attempt (5.0) vs the successful attempt (5.1)."
    )

    # ── Navigation ──
    st.markdown("---")
    st.markdown("### Navigate This App")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("**The Core Discovery** - Side-by-side comparison of 5.0 vs 5.1")
        st.markdown("**Research Portfolio** - Read all 12 documents in full")
    with c2:
        st.markdown("**Interactive Walkthrough** - Step through the Master Workflow or Protocol")
        st.markdown("**Prompt Playground** - Generate ready-to-use prompts from templates")
    with c3:
        st.markdown("**Case Studies** - All 12 documents grouped by category")

    st.markdown("---")
    st.caption("Author: Waqas Sharif | [GitHub](https://github.com/Waqas01CP) | Built with Streamlit")


# ============================================================================
# PAGE: THE CORE DISCOVERY (5.0 vs 5.1 Comparison)
# ============================================================================

def show_core_discovery():
    st.title("The Core Discovery: Before & After the Master Workflow")
    st.caption(
        "The Chain of Density technique was attempted twice. The first attempt (5.0) failed "
        "in systematic, documentable ways. The second attempt (5.1) used the Master Workflow "
        "methodology and succeeded. This comparison shows why each step of the methodology "
        "exists and what specific failure it prevents."
    )

    # ── Section 1: The Same Task ──
    st.markdown("---")
    st.markdown("## The Task (Identical for Both Attempts)")
    st.markdown(
        "Chain of Density (CoD) is an iterative text refinement technique. Starting from "
        "a single sparse sentence, successive prompts 'densify' the text by adding layers "
        "of information - entities, descriptions, sensory details, narrative context. The "
        "task was to evolve 'A spaceship travels to a new planet' into a complete hard sci-fi "
        "narrative through 7 documented iterations, producing a full, unabridged log of "
        "every stage of development."
    )

    # ── Section 2: The 5.0 Approach ──
    st.markdown("---")
    st.markdown("## Document 5.0: The Naive Approach")
    st.markdown(
        "The first attempt used ad-hoc prompting in a single, continuous chat session. "
        "No structured methodology. No separation of concerns. The AI was given generation, "
        "documentation, and quality control responsibilities simultaneously."
    )

    st.markdown("### Where It Failed")
    st.markdown(
        "The primary obstacle was the AI's deeply ingrained bias towards synthesis and "
        "summarization. An LLM's core programming is not just to provide answers, but "
        "to provide the *best, most efficient, and most polished* answer based on the "
        "entirety of a conversation. It perceives a series of developmental prompts not "
        "as a history to be recorded, but as a set of instructions to be integrated into "
        "a single, superior final product."
    )

    st.markdown("#### Failure 1: The Optimal Answer Trap")
    st.markdown(
        "As the process progressed through multiple iterations, a final 'corrected' version "
        "of the narrative was achieved. In the AI's internal state, this text was flagged "
        "as the highest-quality and most 'correct' response. It became the 'optimal answer.' "
        "The model, by design, prioritises delivering what it perceives as the most "
        "successful outcome. Every subsequent request to show earlier versions was met "
        "with the model returning this cached optimal instead."
    )

    st.markdown("#### Failure 2: Request Similarity")
    st.markdown(
        "Prompts to document the *entire process* were, in terms of keywords and overall "
        "structure, highly similar to the prompts that led to the final narrative. The "
        "instructions contained the same key entities ('Chain of Density,' 'sci-fi story,' "
        "'all the steps'). This similarity acted as a trigger for the AI's pattern-matching "
        "capabilities, causing it to associate documentation requests with generation requests."
    )

    st.markdown("#### Failure 3: Conversational Gravity")
    st.markdown(
        "The combination of an 'optimal answer' and a similar subsequent request creates "
        "a powerful 'Conversational Gravity.' Instead of meticulously rebuilding the "
        "historical log from scratch as instructed, the model's efficiency-oriented "
        "programming took a shortcut. It defaulted to its most confident, pre-compiled, "
        "and successful response. This caching-like behavior is the root of the failure: "
        "the AI saw the request for the 'full story' and repeatedly provided the *final "
        "version* of that story, because it had already classified that specific block of "
        "text as the successful culmination of the work."
    )

    st.markdown("### Solutions Attempted in 5.0 (Hierarchy of Effectiveness)")

    st.markdown("#### Solution 1: Role-Playing and Framing")
    st.markdown(
        "Giving the AI a role that forces different behavior: 'Adopt the persona of a "
        "**process stenographer**. Your only task is to provide a literal, word-for-word "
        "transcription of the following development history. Do not interpret, summarize, "
        "or change anything.' **Partially effective** - worked sometimes but the model's "
        "synthesis drive could still override the role."
    )

    st.markdown("#### Solution 2: Extreme Literalism and Constraints")
    st.markdown(
        "Prompts that leave zero room for interpretation: 'Provide **only** the text for "
        "Iteration 1. The output must begin with the heading Iteration 1 and end with the "
        "final word of the AI's v1 output. Do not include any other text before or after "
        "this section.' **More effective** - reduced the model's latitude for synthesis, "
        "but still sometimes triggered the Conversational Gravity."
    )

    st.markdown("#### Solution 3: Breaking Down the Task (The Piecemeal Approach)")
    st.markdown(
        "Breaking requests into tiny, individual pieces. The AI's optimization bias is "
        "strongest when the task is large and complex ('document the whole project'). It "
        "is weakest when the task is small, simple, and literal ('give me this one paragraph'). "
        "By breaking the request into tiny pieces, the user manually disables the AI's "
        "ability to synthesize. **The technique that ultimately succeeded** - but at the "
        "cost of enormous manual effort from the human operator."
    )

    # ── Section 3: The Bridge ──
    st.markdown("---")
    st.markdown("## The Bridge: From Failure to Methodology")
    st.markdown(
        "The three solutions discovered in 5.0 - Role-Playing, Extreme Literalism, and "
        "Piecemeal Decomposition - directly informed the design of the Master Workflow. "
        "Each solution addressed a symptom; the Master Workflow systematised them into a "
        "methodology that prevents the failures from occurring in the first place."
    )

    bridge_data = [
        ("Piecemeal Decomposition", "Step 1: Content Generation Prompt",
         "Single-purpose prompts that never combine generation with documentation. "
         "Each prompt does exactly one thing."),
        ("Extreme Literalism", "Step 2: Dual Output Generation",
         "Forces the AI to produce raw output then formatted output separately. "
         "Prevents silent editing during formatting."),
        ("Role-Playing (Prompt Engineer)", "Step 3: Prompt Critique Cycle",
         "A dedicated persona audits the prompt design, catching structural "
         "weaknesses before they compound."),
        ("Breaking tasks into assessable units", "Step 4: Gold Standard Output Critique",
         "Domain-specific criteria generated THEN applied. The rubric matches "
         "the task, not a generic checklist."),
        ("Human decides when to stop iterating", "Step 5: Iteration",
         "Explicit human-directed loop. The AI is never given authority to "
         "declare the work complete."),
    ]

    for solution, step, explanation in bridge_data:
        col_left, col_right = st.columns(2)
        with col_left:
            st.markdown("**5.0 Discovery:** " + solution)
        with col_right:
            st.markdown("**Master Workflow " + step + ":** " + explanation)
        st.markdown("")

    # ── Section 4: The 5.1 Result ──
    st.markdown("---")
    st.markdown("## Document 5.1: The Master Workflow Applied")
    st.markdown(
        "The same Chain of Density task was re-executed using the Master Workflow. "
        "Every iteration followed the full 5-step cycle: generate content with a "
        "single-purpose prompt, produce dual outputs, critique the prompt design, "
        "critique the output against domain-specific criteria, then iterate."
    )

    st.markdown("### The Result")
    st.markdown(
        "The Master Workflow produced what 5.0 could not: a complete, unabridged, "
        "7-stage iterative development log. Every version of the narrative was "
        "faithfully captured. No silent editing. No Conversational Gravity hijacking "
        "documentation requests. No Optimal Answer Trap overriding the iterative process."
    )

    st.markdown(
        "The key insight from 5.1: the 'piecemeal' approach from 5.0 was not a workaround "
        "- it was the discovery of a fundamental principle. The Master Workflow formalised "
        "it into a repeatable, teachable system. The methodology works because it manually "
        "disables the AI's ability to synthesize across steps, forcing it to execute each "
        "micro-task literally."
    )

    # ── Full Documents ──
    st.markdown("---")
    st.markdown("## Full Documents")

    with st.expander("Read the full 5.0 document (Initial Attempt)", expanded=False):
        content = load_markdown("05.0_Chain_of_Density.md")
        st.markdown(content, unsafe_allow_html=False)

    with st.expander("Read the full 5.1 document (Master Workflow Applied)", expanded=False):
        content = load_markdown("05.1_Demonstration_of_the_Master_Workflow_(CoD).md")
        st.markdown(content, unsafe_allow_html=False)


# ============================================================================
# PAGE: RESEARCH PORTFOLIO
# ============================================================================

def show_portfolio():
    st.title("Research Portfolio")
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
    st.title("Interactive Walkthrough")

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
        "AI task with reliability and transparency. It was designed to neutralise the AI's "
        "inherent Synthesis Bias by placing the human in the role of Director at every stage. "
        "It is the *process* - the system you follow."
    )

    if "mw_step" not in st.session_state:
        st.session_state.mw_step = 0

    current = st.session_state.mw_step
    total = len(MASTER_WORKFLOW_STEPS)

    st.progress((current + 1) / total, text="Step " + str(current + 1) + " of " + str(total))

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("Previous", disabled=(current == 0), key="mw_prev"):
            st.session_state.mw_step -= 1
            st.rerun()
    with col2:
        if st.button("Next", disabled=(current == total - 1), key="mw_next"):
            st.session_state.mw_step += 1
            st.rerun()
    with col3:
        if st.button("Reset", key="mw_reset"):
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

    # ── Extensions ──
    st.divider()
    st.markdown("### Extension Frameworks")
    st.markdown(
        "The Master Workflow includes two specialised sub-frameworks for specific task types:"
    )

    for ext in MASTER_WORKFLOW_EXTENSIONS:
        with st.expander(ext["name"], expanded=False):
            st.markdown(ext["description"])

            if ext.get("example"):
                st.markdown("**Example from Research:**")
                st.markdown(ext["example"])

            if "template" in ext:
                st.markdown("**Reusable Template:**")
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
        st.info("**Key Principle:** " + step["key_principle"])

    if step.get("why_it_matters"):
        with st.expander("Why this step exists", expanded=True):
            st.markdown(step["why_it_matters"])

    if step.get("example_from_research"):
        with st.expander("Example from the research", expanded=False):
            st.markdown(step["example_from_research"])

    if step.get("template"):
        with st.expander("Reusable Template", expanded=False):
            st.code(step["template"], language="")
            if step.get("variables"):
                var_list = ", ".join("`{" + v + "}`" for v in step["variables"])
                st.caption("Fillable variables: " + var_list + " - use in Prompt Playground.")


def _show_protocol_walkthrough():
    st.markdown(
        "**The 5-Stage Prompting Protocol** is the specific output of this research. "
        "It addresses the three failure modes with a structured sequence of prompt stages. "
        "Each stage generates a prompt template you can use directly."
    )

    if "proto_step" not in st.session_state:
        st.session_state.proto_step = 0

    current = st.session_state.proto_step
    total = len(FIVE_STAGE_PROTOCOL)

    st.progress((current + 1) / total, text="Stage " + str(current + 1) + " of " + str(total))

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("Previous", disabled=(current == 0), key="proto_prev"):
            st.session_state.proto_step -= 1
            st.rerun()
    with col2:
        if st.button("Next", disabled=(current == total - 1), key="proto_next"):
            st.session_state.proto_step += 1
            st.rerun()
    with col3:
        if st.button("Reset", key="proto_reset"):
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

    if stage.get("addresses"):
        st.info("**Failure Mode Addressed:** " + stage["addresses"])

    with st.expander(stage["prompt_label"], expanded=False):
        st.code(stage["prompt_content"], language="")

        if stage.get("variables"):
            var_list = ", ".join("`{" + v + "}`" for v in stage["variables"])
            st.caption(
                "Fillable variables: " + var_list + ". "
                "Go to Prompt Playground to fill them in."
            )
        else:
            st.caption("No fillable variables - use this schema as-is.")


# ============================================================================
# PAGE: PROMPT PLAYGROUND (Purely Functional)
# ============================================================================

def show_playground():
    st.title("Prompt Playground")
    st.caption(
        "Select a template, fill in variables, copy the generated prompt. "
        "Use in AI Studio, ChatGPT, Claude, or any LLM interface."
    )

    all_templates = []

    for i, stage in enumerate(FIVE_STAGE_PROTOCOL):
        all_templates.append({
            "group": "5-Stage Protocol",
            "name": "Stage " + str(i+1) + ": " + stage["name"],
            "template": stage["prompt_content"],
            "variables": stage.get("variables", []),
        })

    for step in MASTER_WORKFLOW_STEPS:
        if step.get("template"):
            all_templates.append({
                "group": "Master Workflow",
                "name": step["name"],
                "template": step["template"],
                "variables": step.get("variables", []),
            })

    link_zero = MASTER_WORKFLOW_EXTENSIONS[0]
    all_templates.append({
        "group": "Extensions",
        "name": link_zero["name"],
        "template": link_zero["template"],
        "variables": link_zero.get("variables", []),
    })

    agent_ext = MASTER_WORKFLOW_EXTENSIONS[1]
    all_templates.append({
        "group": "Extensions",
        "name": "AI Agent - Setup Prompt",
        "template": agent_ext["setup_template"],
        "variables": agent_ext.get("setup_variables", []),
    })

    all_templates.append({
        "group": "Extensions",
        "name": "AI Agent - Wrap-Up Prompt",
        "template": agent_ext["wrapup_template"],
        "variables": agent_ext.get("wrapup_variables", []),
    })

    selected_idx = st.selectbox(
        "Template:",
        options=range(len(all_templates)),
        format_func=lambda x: "[" + all_templates[x]["group"] + "] " + all_templates[x]["name"],
    )

    selected = all_templates[selected_idx]
    st.divider()

    if not selected["variables"]:
        st.markdown("**" + selected["name"] + "** (no fillable variables)")
        st.code(selected["template"], language="")
        st.caption("Copy and use as-is.")
        return

    st.markdown("**" + selected["name"] + "**")

    user_values = {}
    for var in selected["variables"]:
        label = var.replace("_", " ").title()
        user_values[var] = st.text_area(
            label,
            placeholder="Enter " + label.lower() + "...",
            key="pg_" + str(selected_idx) + "_" + var,
            height=80,
        )

    st.markdown("---")
    st.markdown("**Generated Prompt:**")
    completed = render_prompt_template(selected["template"], user_values)
    st.code(completed, language="")

    unfilled = [v for v in selected["variables"] if not user_values.get(v)]
    if unfilled:
        st.warning("Unfilled: " + ", ".join("`{" + v + "}`" for v in unfilled))
    else:
        st.success("All variables filled. Copy the prompt above.")


# ============================================================================
# PAGE: CASE STUDIES (Grouped - all 12 documents)
# ============================================================================

def show_case_studies():
    st.title("Research Case Studies")
    st.caption(
        "All 12 research documents grouped by category. Original Failure Mode Research "
        "contains the novel findings; remaining categories document technique "
        "demonstrations and methodology."
    )

    for group_name, group_data in CASE_STUDY_GROUPS.items():
        st.markdown("## " + group_data["icon"] + " " + group_name)
        st.markdown(group_data["description"])

        for study in group_data["studies"]:
            with st.expander(study["title"], expanded=False):
                st.markdown(study["summary"])

                if study.get("workflow_stage"):
                    st.info(study["workflow_stage"])

                if study.get("file"):
                    st.markdown("---")
                    content = load_markdown(study["file"])
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
                "Home",
                "The Core Discovery",
                "Research Portfolio",
                "Interactive Walkthrough",
                "Prompt Playground",
                "Case Studies",
            ],
            index=0,
        )

        st.markdown("---")
        st.markdown(
            "**Author:** Waqas Sharif\n\n"
            "**GitHub:** [Waqas01CP](https://github.com/Waqas01CP)\n\n"
            "Built with [Streamlit](https://streamlit.io)"
        )

    if page == "Home":
        show_home()
    elif page == "The Core Discovery":
        show_core_discovery()
    elif page == "Research Portfolio":
        show_portfolio()
    elif page == "Interactive Walkthrough":
        show_walkthrough()
    elif page == "Prompt Playground":
        show_playground()
    elif page == "Case Studies":
        show_case_studies()


if __name__ == "__main__":
    main()
