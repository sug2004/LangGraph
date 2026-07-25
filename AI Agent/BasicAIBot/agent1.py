from typing import TypedDict,List
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage
from langchain_openrouter import ChatOpenRouter
from dotenv import load_dotenv
load_dotenv()

class AgentState(TypedDict):
    messages: List[HumanMessage]


llm = ChatOpenRouter(
    model="openrouter/free",
)

def process(state:AgentState)-> AgentState:
    """ This node will solve the user request """
    response = llm.invoke(state['messages'])
    print(f"\nAI:{response.content}")
    return state

graph = StateGraph(AgentState)
graph.add_node("process",process)
graph.add_edge(START,"process")
graph.add_edge("process", END)
agent = graph.compile()


# from IPython.display import Image,display
# display(Image(agent.get_graph().draw_mermaid_png()))


user_Input = input("Enter: ")
while user_Input != "exit":
    agent.invoke({"messages":[HumanMessage(content=user_Input)]})
    user_Input = input("Enter: ")