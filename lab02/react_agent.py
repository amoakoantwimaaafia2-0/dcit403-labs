"""react_agent.py - ReAct loop from scratch (Lab 2, Steps 3-5). Standard library only.

    export ANTHROPIC_API_KEY=...
    python react_agent.py "I have GHS 2,000. I want to buy 12 yards of kente ..."

Each run prints the full trace and saves it to evidence/trace_<n>.txt.
"""
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

from tools import TOOLS

MODEL = os.environ.get("MODEL", "claude-sonnet-5-5")
EVIDENCE = Path(__file__).parent / "evidence"

SYSTEM = """You are a helpful assistant for a tailor with a small shop in Kumasi, Ghana.
You help with costs, earnings and quick facts by alternating Thought, Action and Action Input.
Money is in Ghana cedis (GHS).

Tools:
- calculator: evaluates arithmetic (+ - * /). Action Input is an expression, e.g. 4*185 + 3*95
- wiki_lookup: returns a Wikipedia summary. Action Input is a page title, e.g. Bono East Region
- finish: ends the task. Action Input is your final answer to the user.

Reply in EXACTLY this format on every step:
Thought: <your reasoning>
Action: calculator | wiki_lookup | finish
Action Input: <input for the tool, or the final answer if finish>

After an Action the system replies with "Observation: ...". Never write an
Observation yourself. Do not do arithmetic in your head: use the calculator."""

ACTION_RE = re.compile(r"Action:\s*(\w+)\s*\nAction Input:\s*(.*)", re.DOTALL)


# ---------- model call (raw HTTPS, no SDK) ----------
def call_model(system: str, transcript: str) -> str:
    body = {
        "model": MODEL,
        "max_tokens": 400,
        "system": system,
        "stop_sequences": ["Observation:"],   # model must not invent observations
        "messages": [{"role": "user", "content": transcript}],
    }
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=json.dumps(body).encode(),
        headers={"x-api-key": os.environ["ANTHROPIC_API_KEY"],
                 "anthropic-version": "2023-06-01",
                 "content-type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.load(r)
    return "".join(b.get("text", "") for b in data["content"]).strip()


# ---------- parser ----------
def parse(text: str):
    m = ACTION_RE.search(text)
    if not m:
        return None, None
    return m.group(1).strip(), m.group(2).strip()


# ---------- the loop ----------
def run_agent(question: str, max_steps: int = 6, model=call_model, log=print):
    """Return the final answer, or None if max_steps was reached."""
    transcript = f"Question: {question}\n"
    log(f"Question: {question}")
    for step in range(1, max_steps + 1):
        log(f"\n--- step {step} ---")
        try:
            reply = model(SYSTEM, transcript)
        except Exception as e:                      # API/network failure: stop cleanly
            log(f"[model call failed: {e}]")
            return None
        log(reply)
        transcript += reply + "\n"

        action, arg = parse(reply)
        if action is None:                          # unparseable -> corrective observation
            obs = ("Error: could not parse your reply. Reply in exactly this format:\n"
                   "Thought: <reasoning>\nAction: calculator | wiki_lookup | finish\n"
                   "Action Input: <input>")
        elif action == "finish":
            log("\n[finish]")
            return arg
        elif action not in TOOLS:                   # unknown action -> corrective observation
            obs = (f"Error: unknown action '{action}'. "
                   "Valid actions are: calculator, wiki_lookup, finish.")
        else:
            obs = TOOLS[action](arg)

        log(f"Observation: {obs}")
        transcript += f"Observation: {obs}\n"

    log(f"\n[stopped: reached max_steps={max_steps} without finish]")
    return None


def next_trace_path() -> Path:
    EVIDENCE.mkdir(exist_ok=True)
    nums = [int(m.group(1)) for p in EVIDENCE.glob("trace_*.txt")
            if (m := re.match(r"trace_(\d+)\.txt", p.name))]
    return EVIDENCE / f"trace_{max(nums, default=0) + 1}.txt"


def run_and_save(question: str, **kw):
    """Run one question, print the trace and save it to evidence/trace_<n>.txt."""
    lines = []

    def log(s):
        print(s)
        lines.append(s)

    answer = run_agent(question, log=log, **kw)
    log(f"\nFINAL ANSWER: {answer}")
    path = next_trace_path()
    path.write_text("\n".join(lines) + "\n")
    print(f"[trace saved to {path}]")
    return answer


def main():
    if len(sys.argv) < 2:
        sys.exit('usage: python react_agent.py "your question"')
    if "ANTHROPIC_API_KEY" not in os.environ:
        sys.exit("Set ANTHROPIC_API_KEY first.")
    run_and_save(" ".join(sys.argv[1:]))


if __name__ == "__main__":
    main()
