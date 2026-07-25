# LangGraph Course

A hands-on course for learning **LangGraph** - a library for building stateful, multi-actor applications with LLMs using graph-based workflows.

## 📚 Course Overview

This course covers the fundamentals of LangGraph through practical Jupyter notebooks, progressing from basic concepts to more advanced patterns.

## 📁 Notebooks

| Notebook | Topic | Key Concepts |
|----------|-------|--------------|
| [`Graph/helloWorld.ipynb`](Graph/helloWorld.ipynb) | **Hello World** | Basic graph creation, single node, state schema |
| [`Graph/SquentialGraph.ipynb`](Graph/SquentialGraph.ipynb) | **Sequential Graph** | Multi-node linear workflows, edges, entry/finish points |
| [`Graph/Multiple_input.ipynb`](Graph/Multiple_input.ipynb) | **Multiple Inputs** | Handling complex state with lists and multiple fields |
| [`Graph/ConditionalGraph.ipynb`](Graph/ConditionalGraph.ipynb) | **Conditional Graph** | Routing, conditional edges, decision nodes |
| [`Graph/loopingGraph.ipynb`](Graph/loopingGraph.ipynb) | **Looping Graph** | Cycles, loops, conditional continuation |

## 🤖 AI Agents

| Agent | File | Description |
|-------|------|-------------|
| **BasicAIBot** | [`AI Agent/BasicAIBot/agent1.py`](AI Agent/BasicAIBot/agent1.py) | Simple LangGraph agent with basic conversation |
| **MemoryAgent** | [`AI Agent/MemoryAgent/agent2.py`](AI Agent/MemoryAgent/agent2.py) | Agent with conversation memory/history |
| **ReActAgent** | [`AI Agent/ReActAgent/agent3.py`](AI Agent/ReActAgent/agent3.py) | ReAct (Reasoning + Acting) agent with tool use |

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Jupyter Notebook or VS Code with Jupyter extension

### Installation

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install langgraph langchain-core ipykernel
```

### Running the Notebooks

1. Open any `.ipynb` file in VS Code or Jupyter
2. Select the Python kernel (`.venv`)
3. Run cells sequentially

## 📖 Learning Path

### 1. Hello World Graph
- **StateGraph** creation with `TypedDict` schema
- Single node that transforms state
- Entry and finish points
- Graph compilation and invocation

### 2. Sequential Graph
- Multiple nodes in linear sequence
- `add_edge()` for connecting nodes
- State passing between nodes
- Visualizing graphs with Mermaid

### 3. Multiple Inputs
- Complex state with `List[int]` and multiple fields
- Processing multiple inputs in a single node
- Sum/aggregation operations

### 4. Conditional Graph
- **Router pattern** with decision nodes
- `add_conditional_edges()` for dynamic routing
- `START` and `END` constants
- Lambda passthrough nodes

### 5. Looping Graph
- **Cycles** in graphs
- `add_conditional_edges()` with loop/exit conditions
- Counter-based iteration control
- `END` constant for termination

## 🔑 Key LangGraph Concepts

| Concept | Description |
|---------|-------------|
| **StateGraph** | Main graph builder class |
| **State Schema** | `TypedDict` defining shared state structure |
| **Nodes** | Functions that process state (`state -> state`) |
| **Edges** | Connections between nodes |
| **Conditional Edges** | Dynamic routing based on state |
| **Entry Point** | Where graph execution begins |
| **Finish Point** | Where graph execution ends |
| **Compilation** | `graph.compile()` creates runnable app |

## 📝 Common Patterns

### Basic Graph Structure
```python
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class AgentState(TypedDict):
    # Define your state fields
    message: str

def my_node(state: AgentState) -> AgentState:
    # Transform state
    return state

graph = StateGraph(AgentState)
graph.add_node("node_name", my_node)
graph.add_edge(START, "node_name")
graph.add_edge("node_name", END)
app = graph.compile()
```

### Conditional Routing
```python
def router(state: AgentState) -> str:
    if condition:
        return "path_a"
    return "path_b"

graph.add_conditional_edges(
    "router_node",
    router,
    {
        "path_a": "node_a",
        "path_b": "node_b"
    }
)
```

### Loops
```python
def should_continue(state: AgentState) -> str:
    if state['counter'] < MAX_ITERATIONS:
        return "continue"
    return "exit"

graph.add_conditional_edges(
    "loop_node",
    should_continue,
    {
        "continue": "loop_node",  # Creates cycle
        "exit": END
    }
)
```

## 🛠️ Troubleshooting

### Common Issues

1. **TypeError: cannot use 'dict' as a set element**
   - Fix: Use `add_conditional_edges(source, condition, mapping)` with 3 separate arguments, not a dictionary

2. **Import errors**
   - Ensure `langgraph` and `langchain-core` are installed
   - Check Python version compatibility

3. **Graph visualization not showing**
   - Install `pygraphviz` or use Mermaid rendering
   - In VS Code, ensure Jupyter extension is installed

## 📚 Resources

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangGraph GitHub](https://github.com/langchain-ai/langgraph)
- [LangChain Academy](https://academy.langchain.com/)

## 📄 License

This course material is for educational purposes.