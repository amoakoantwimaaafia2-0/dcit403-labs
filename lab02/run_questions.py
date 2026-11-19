"""run_questions.py - run the Kumasi tailor-shop questions, one trace each.

    python run_questions.py          # all six
    python run_questions.py 4 6      # only questions 4 and 6

Rephrase question 6 (or edit QUESTIONS) until you get a failure worth writing up.
"""
import os
import sys

from react_agent import run_and_save

QUESTIONS = {
    1: "I have GHS 2,000. I want to buy 12 yards of kente at GHS 95 per yard and "
       "30 packs of buttons at GHS 8 each. How much will I have left?",
    2: "What is the capital of the Ashanti Region, and how much do I earn if I "
       "sell 15 shirts at GHS 140 each?",
    3: "In what year did Ghana become independent, and how many years before "
       "2026 was that?",
    4: "Tell me about the Glimmerwick Fabric Fair.",
    5: "Write one polite sentence to thank a customer.",
    6: "shirts 15 each cost 140 also buttons how many total??",
}

if __name__ == "__main__":
    if "ANTHROPIC_API_KEY" not in os.environ:
        sys.exit("Set ANTHROPIC_API_KEY first.")
    chosen = [int(a) for a in sys.argv[1:]] or list(QUESTIONS)
    for n in chosen:
        print(f"\n{'=' * 60}\nQUESTION {n}\n{'=' * 60}")
        run_and_save(QUESTIONS[n])
