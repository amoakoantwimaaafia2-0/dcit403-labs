# Lab 2: Architectures: A ReAct Agent From Scratch: Concept Check

Answer in your own words before the Wednesday session (independent work). Your answers feed Section 2 of your lab report (Concept and classical root).

## Q1. Classify a thermostat, a chess engine and a ReAct agent as reactive, deliberative or hybrid, with one reason each.

_Your answer:_Thermostat: reactive. It maps the current temperature straight to an action with a condition-action rule (if too cold, heat on). It has no model of the world, no memory and no planning.
Chess engine: deliberative. It keeps an internal model of the board and searches possible future move sequences to pick the move that best serves its goal of winning.
ReAct agent: hybrid. The Thought is a deliberative layer that plans across steps, while each Action reacts to the latest Observation. It combines planning with quick responses to new percepts.


## Q2. In the trace above, which lines are percepts, and which are actions?

_Your answer:_Percepts: The Observation: lines (Observation: 1025 and Observation: 175) are percepts, because they are new information coming from the environment (the tool) back to the agent. The original question is also a percept.
Actions: The Action: and Action Input: lines are actions, including the final finish, which delivers the answer to the user.
Neither: The Thought: lines are internal reasoning (deliberation), not percepts or actions.


## Q3. Why do we pass `stop=["Observation:"]` when calling the model?

_Your answer:_Without a stop sequence, the model keeps generating after it writes an Action and invents its own Observation, so it would make up the tool result and carry on with false information. The stop sequence ends generation right after Action Input. This lets our code run the real tool and supply the true Observation, so the agent’s percepts come from the environment and not from its imagination.


## Q4. Map the trace above to the BDI terms belief, desire and intention.

_Your answer:_Beliefs: What the agent holds true, which is the conversation so far: the GHS 1,200 budget, the quantities and prices, and the observations (1025, then 175). Beliefs update after each Observation.
Desire: The goal of finding out how much money is left after the purchases, which is what the user wants answered.
Intention: The plan the agent has committed to in its Thoughts, which is to compute the total cost first and then subtract it from the budget. Each tool call is one step of executing that plan, and finish completes it.

