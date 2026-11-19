"""tools.py - actuators for the ReAct agent (Lab 2, Step 2).

Both tools take one string and return one string. They never raise:
failures come back as text so the agent sees them as Observations.
"""
import ast
import json
import operator as op
import urllib.error
import urllib.parse
import urllib.request

OPS = {ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul,
       ast.Div: op.truediv, ast.USub: op.neg}


def _eval(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in OPS:
        return OPS[type(node.op)](_eval(node.left), _eval(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in OPS:
        return OPS[type(node.op)](_eval(node.operand))
    raise ValueError("Unsupported expression")


def calculator(expression: str) -> str:
    """Safely evaluate + - * / and unary minus using ast (never eval)."""
    try:
        expr = expression.replace(",", "")
        return str(_eval(ast.parse(expr, mode="eval").body))
    except Exception as e:
        return f"Error: {e}"


def wiki_lookup(title: str) -> str:
    """Return the first ~800 characters of a Wikipedia page summary."""
    url = ("https://en.wikipedia.org/api/rest_v1/page/summary/"
           + urllib.parse.quote(title.strip().replace(" ", "_")))
    req = urllib.request.Request(url, headers={"User-Agent": "DCIT403-lab"})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.load(r).get("extract", "")[:800] or f"No summary for '{title}'."
    except urllib.error.HTTPError:
        return f"No Wikipedia page found for '{title}'."
    except Exception as e:  # network down, timeout, bad JSON ...
        return f"Error: could not reach Wikipedia ({e})."


TOOLS = {"calculator": calculator, "wiki_lookup": wiki_lookup}

if __name__ == "__main__":  # Step 2 checkpoint: test tools directly
    print(calculator("4*185 + 3*95"))
    print(calculator("1,200 - 1025"))
    print(calculator("__import__('os')"))   # must be an Error
    print(wiki_lookup("Accra"))
    print(wiki_lookup("Zzzqx not a real page"))
