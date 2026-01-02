from agents.planner_agent import planner_agent

state = {
    "resume_text": "test resume",
    "user_intent": "test intent"
}

out = planner_agent(state)
print(out)
