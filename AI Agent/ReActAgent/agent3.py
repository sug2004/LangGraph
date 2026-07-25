from typing import Annotated, Sequence, TypedDict
# Annoted - provides additional context without affecting the type itself
# Sequence - To automatically handle the state update for sequence such as adding new message toa chat history
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage # The foundational class for all message types in LangGraph
from langchain_core.messages import ToolMessage # Passes data back to LLM after it calls a tool such as the content and result
from langchain_core.messages import SystemMessage # Message for providing instructions to the LLM
from langchain_openrouter import ChatOpenRouter
from langchain_core.tools import tool
from langgraph.graph.message import add_messages 
# add_message is a Reducer function that states the rule that control how to update from node to combine with existing state
# without reducer function, updates would be replaced with the existing value entirely 
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import BaseMessage, AIMessage # The foundational class for all message types in LangGraph

load_dotenv()

class AgentState(TypedDict):
    messages : Annotated[Sequence[BaseMessage],add_messages]

@tool
def add(a: int, b:int):
    """This is an addition function that adds 2 numbers together"""

    return a + b 

@tool
def subtract(a: int, b: int):
    """Subtraction function"""
    return a - b

@tool
def multiply(a: int, b: int):
    """Multiplication function"""
    return a * b

tools = [add, subtract, multiply]




# LLM
llm = ChatOpenRouter(model="openrouter/free").bind_tools(tools=tools)

# node
def model_call(state: AgentState) -> AgentState:
    system_prompt = SystemMessage(content="You are my AI assistant, please answer my query to the best of your ability.")
    response = llm.invoke([system_prompt] + state["messages"])
    return {"messages": [response]}

# coditional node
def should_continue(state:AgentState):
    """ Function to decide what to do next """
    messages = state["messages"]
    last_message = messages[-1]
    if not last_message.tool_calls:
        return "end"
    else:
        return "continue"

# init Graph
graph = StateGraph(AgentState)
graph.add_node("our_agent", model_call)


tool_node = ToolNode(tools=tools)# adding tools as a node in the graph
graph.add_node("tools", tool_node)

graph.set_entry_point("our_agent")

graph.add_conditional_edges(
    "our_agent",
    should_continue,
    {
        "continue": "tools",
        "end": END,
    },
)

graph.add_edge("tools", "our_agent")

app = graph.compile()


# Helper Function
def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        
        if isinstance(message, tuple):
            print(message)
        elif isinstance(message, AIMessage) and message.tool_calls:
            for tool_call in message.tool_calls:
                print(f"\n🔧 Tool Call: {tool_call['name']}")
                print(f"   Args: {tool_call['args']}")
        elif isinstance(message, ToolMessage):
            print(f"\n✅ Tool Result ({message.name}): {message.content}")
        else:
            message.pretty_print()

inputs = {"messages": [("user", "Add 40 + 12 and then multiply the result by 6. Also tell me a joke please.")]}
print_stream(app.stream(inputs, stream_mode="values"))