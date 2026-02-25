"""
workflow_runner.py
==================
A runnable demonstration of the "Master Workflow" protocol documented in this
research repository. The Master Workflow is a structured prompting strategy
developed through iterative behavioral meta-analysis of Google Gemini (via
AI Studio) to solve a failure mode I termed the "Optimal Answer Trap" —
where a model returns a polished, complete-looking response that misses the
actual intent of the request.

This script is NOT a wrapper around an AI API. It is a teaching tool:
it prints each stage of the Master Workflow so you can understand the
reasoning behind every prompt design decision, then generates the actual
prompt text you would copy into AI Studio (or adapt for the Gemini API).

Usage
-----
    python workflow_runner.py

    # Step through each stage interactively:
    python workflow_runner.py --interactive

    # Run a specific case study workflow:
    python workflow_runner.py --case hallucination_red_team
    python workflow_runner.py --case synthesis_bias
    python workflow_runner.py --case context_engineering

Requirements
------------
    Python 3.10+   (no external dependencies — stdlib only)

Author
------
    Waqas Sharif   github.com/Waqas01CP
"""

import argparse
import textwrap
import time
import sys


# ── ANSI colour helpers (gracefully disabled on Windows without colour support) ──

def _supports_colour() -> bool:
    return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()

BOLD   = "\033[1m"   if _supports_colour() else ""
CYAN   = "\033[96m"  if _supports_colour() else ""
GREEN  = "\033[92m"  if _supports_colour() else ""
YELLOW = "\033[93m"  if _supports_colour() else ""
GREY   = "\033[90m"  if _supports_colour() else ""
RESET  = "\033[0m"   if _supports_colour() else ""

def header(text: str) -> None:
    width = 70
    print(f"\n{CYAN}{'─' * width}{RESET}")
    print(f"{BOLD}{CYAN}  {text}{RESET}")
    print(f"{CYAN}{'─' * width}{RESET}\n")

def stage(number: int, name: str, description: str) -> None:
    print(f"{BOLD}{GREEN}Stage {number}: {name}{RESET}")
    print(f"{GREY}{textwrap.fill(description, width=68, initial_indent='  ', subsequent_indent='  ')}{RESET}\n")

def prompt_block(label: str, content: str) -> None:
    print(f"{YELLOW}[ {label} ]{RESET}")
    border = "┌" + "─" * 66 + "┐"
    footer = "└" + "─" * 66 + "┘"
    print(border)
    for line in content.strip().split("\n"):
        wrapped = textwrap.wrap(line, width=64) or [""]
        for w in wrapped:
            print(f"│  {w:<64}│")
    print(footer)
    print()

def pause(interactive: bool) -> None:
    if interactive:
        input(f"  {GREY}Press Enter to continue...{RESET}\n")
    else:
        time.sleep(0.3)


# ── Master Workflow definition ──────────────────────────────────────────────

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
        "prompt_content": """\
ROLE: You are an intent analyst.

TASK: I will give you a user request. Return ONLY a JSON object:
{
  "surface_request": "<what they literally asked>",
  "underlying_intent": "<what they actually need>",
  "success_criteria": ["<criterion 1>", "<criterion 2>"]
}

USER REQUEST: {user_request}

Return JSON only. No preamble.""",
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
        "prompt_content": """\
CONTEXT (read carefully before proceeding):
  - Domain: {domain}
  - Established facts: {known_facts}
  - Constraints: {constraints}
  - Prior session findings: {prior_findings}

Only use information from the CONTEXT block above.
If the context does not contain enough information to answer,
say "INSUFFICIENT CONTEXT" rather than inferring.""",
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
        "prompt_content": """\
Return your answer as a JSON object matching this schema EXACTLY:
{
  "answer": "<your direct answer>",
  "confidence": "HIGH | MEDIUM | LOW",
  "sources_used": ["<source 1>", "<source 2>"],
  "gaps": ["<anything you could not determine from context>"],
  "follow_up_questions": ["<question to resolve gaps>"]
}

Do NOT add any text outside the JSON object.""",
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
        "prompt_content": """\
The following is a draft answer. Your job is to CHALLENGE it:

DRAFT: {previous_output}

Instructions:
1. List every factual claim in the draft.
2. For each claim, state whether it is: VERIFIED | UNVERIFIED | FALSE
3. Identify any logical gaps or leaps.
4. Suggest what a reasonable counterargument would be.
5. Give a revised confidence rating: HIGH | MEDIUM | LOW

Be adversarial. Your goal is to find weaknesses, not validate.""",
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
        "prompt_content": """\
You have two inputs:
  ORIGINAL ANSWER: {original_answer}
  RED TEAM CRITIQUE: {critique}

Produce a FINAL, reconciled answer that:
- Incorporates valid critique points
- Explicitly marks any claims that remain uncertain as [UNCERTAIN]
- Does NOT drop information just because it is hard to reconcile
- Ends with a one-sentence confidence summary

Format: Plain prose. No JSON. Aim for clarity over completeness.""",
    },
]


# ── Case study workflows ─────────────────────────────────────────────────────

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
            "attributed a Searle quote to Turing. The red team pass caught both. "
            "Full case study: case-studies/hallucination_red_team.md"
        ),
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
            "favoured the other. Stage 5's reconciliation instruction broke this bias. "
            "Full case study: case-studies/synthesis_bias.md"
        ),
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
            "knowledge rather than the injected context in ~30% of trials. Ordering matters. "
            "Full case study: case-studies/context_engineering.md"
        ),
    },
}


# ── Runner ───────────────────────────────────────────────────────────────────

def run_master_workflow(interactive: bool) -> None:
    header("THE MASTER WORKFLOW — Applied LLM Workflow Research")
    print(textwrap.fill(
        "This is a structured prompting protocol developed through iterative "
        "behavioral testing of Google Gemini. It addresses three failure modes: "
        "the Optimal Answer Trap, Final Synthesis Bias, and context-driven "
        "hallucination. Each stage below generates a prompt template you can "
        "use directly in AI Studio or adapt for the Gemini API.",
        width=68,
    ))
    print()

    for i, s in enumerate(MASTER_WORKFLOW_STAGES, start=1):
        stage(i, s["name"], s["description"])
        prompt_block(s["prompt_label"], s["prompt_content"])
        pause(interactive)

    header("WORKFLOW COMPLETE")
    print("  Full research notes and case studies are in case-studies/")
    print("  Refer to README.md for the theoretical framework.\n")


def run_case_study(name: str, interactive: bool) -> None:
    if name not in CASE_STUDIES:
        print(f"Unknown case study '{name}'. Available: {', '.join(CASE_STUDIES)}")
        sys.exit(1)

    cs = CASE_STUDIES[name]
    header(cs["title"])
    print(textwrap.fill(cs["description"], width=68))
    print()
    pause(interactive)

    stage(1, "Example Request", "The prompt submitted to Gemini in this experiment.")
    prompt_block("Input Prompt", cs["example_request"])
    pause(interactive)

    stage(2, "Key Finding", "What the Master Workflow revealed that a naive prompt would not.")
    print(f"  {GREEN}{cs['key_finding']}{RESET}\n")


def list_case_studies() -> None:
    header("Available Case Studies")
    for key, cs in CASE_STUDIES.items():
        print(f"  {BOLD}{key}{RESET}")
        print(f"    {cs['title']}")
        print()
    print(f"  Run with:  python workflow_runner.py --case <name>\n")


# ── Entry point ──────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Master Workflow runner — Applied LLM Workflow Research",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="Pause between stages and wait for Enter key",
    )
    parser.add_argument(
        "--case", "-c",
        type=str, default=None,
        metavar="NAME",
        help="Run a specific case study (use --list to see options)",
    )
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="List all available case studies",
    )
    args = parser.parse_args()

    if args.list:
        list_case_studies()
    elif args.case:
        run_case_study(args.case, args.interactive)
    else:
        run_master_workflow(args.interactive)


if __name__ == "__main__":
    main()
