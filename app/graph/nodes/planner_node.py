from agents.planner import create_plan
from graph.state import ResearchState

def task_planner(state : ResearchState) : 
    query = state['rewritten_query']

    tasks = create_plan(query)

    return { 'research_tasks' : tasks }