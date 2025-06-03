from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from random import random
from view_graph_image import generate_graph_structure

class DataState(TypedDict):
    message: str
    logs: list[dict]
    task_type: str
    status: str
    user_name: str
    
    
def supervisor_node(state: DataState) -> DataState:
    if state["status"] == "Failed" or random() > 0.5:
        state["task_type"] = "Technical Support"
        state["logs"].append({"task_type": "technical support", "role": "engineer"})
        print(state["logs"])
        return state
    else:
        state["task_type"] = "Sales Support"
        state["logs"].append({"task_type": "sales support", "role": "sales"})
        print(state["logs"])
        return state
    
    
def engineer_node(state: DataState) -> DataState:
    rad_val = random()
    if rad_val > 0.5:
        print(f"engineer: {rad_val}")
        state["status"] = "Successful"
        state["logs"].append({"engineer_status": "Successful"})
        print(state["status"])
        return state
    else:
        print(f"engineer: {rad_val}")
        print(rad_val)
        state["status"] = "Failed"
        state["logs"].append({"engineer_status": "Failed"})
        print(state["status"])
        return state
    
    
def sales_node(state: DataState) -> DataState:
    rad_val = random()
    if rad_val > 0.5:
        print(f"sales: {rad_val}")
        state["status"] = "Successful"
        state["logs"].append({"sales_status": "Successful"})
        print(state["status"])
        return state
    else:
        print(f"sales: {rad_val}")
        state["status"] = "Failed"
        state["logs"].append({"sales_status": "Failed"})
        print(state["status"])
        return state
    
    
def generate_response_node(state: DataState) -> DataState:
    state["message"] = f"Thank you {state['user_name']} for contacting us.\nYour request has been {state['status']} submitted.\nWe will get back to you as soon as possible."
    # print(state["message"])
    return state

def supervisor_router(state: DataState):
    # This assumes state["task_type"] is set to "Technical Support" or "Sales Support"
    return state["task_type"]   

def sub_router(state: DataState):
    return state["status"]

graph_builder = StateGraph(DataState)

graph_builder.add_node("Supervisor", supervisor_node)
graph_builder.add_node("Engineer", engineer_node)
graph_builder.add_node("Sales", sales_node)
graph_builder.add_node("Generate Response", generate_response_node)


graph_builder.add_edge(START, "Supervisor")

graph_builder.add_conditional_edges(
    "Supervisor",
    supervisor_router,
    {
        "Technical Support": "Engineer",
        "Sales Support": "Sales",
    },
)
#
graph_builder.add_conditional_edges(
    "Engineer",
    sub_router,
    {
        "Successful": "Generate Response",
        "Failed": "Supervisor",
    },
)
#
graph_builder.add_conditional_edges(
    "Sales",
    sub_router,
    {
        "Successful": "Generate Response",
        "Failed": "Supervisor",
    },
)

graph_builder.add_edge("Generate Response", END)

graph = graph_builder.compile()

generate_graph_structure(graph)

result = graph.invoke({"user_name": "John", "logs": [], "status": "", "message": "", "task_type": ""})

print(result["message"])



