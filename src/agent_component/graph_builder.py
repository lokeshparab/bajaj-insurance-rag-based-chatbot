from src.agent_component.agent import Agents, AgentState
from langgraph.graph import StateGraph

def build_insurance_agent_graph() -> StateGraph:
    agent = Agents()
    graph = StateGraph(AgentState)


    graph.add_sequence([agent.rag_retriever, agent.insurance_agent])

    graph.set_entry_point(agent.rag_retriever)
    graph.set_finish_point(agent.insurance_agent)

    app = graph.compile()
    app.get_graph().draw_mermaid_png(output_file_path="static/workflow.png")
    return app