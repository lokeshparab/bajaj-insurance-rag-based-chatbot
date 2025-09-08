from src.agent_component.agent import Agents, AgentState
from langgraph.graph import StateGraph

from logger.custom_logger import CustomLogger
from exception.custom_exception import CustomException
import sys

logging = CustomLogger().get_logger(__file__)

def build_insurance_agent_graph() -> StateGraph:

    try:
        logging.info("Intializing insurance agent graph")
        agent = Agents()
        graph = StateGraph(AgentState)


        logging.info("Adding sequence paths to the graph")
        graph.add_sequence([agent.rag_retriever, agent.insurance_agent])

        graph.set_entry_point(agent.rag_retriever.__name__)
        graph.set_finish_point(agent.insurance_agent.__name__)

        logging.info("Compiling the graph and generating workflow image")
        app = graph.compile()
        app.get_graph().draw_mermaid_png(output_file_path="static/img/workflow.png")

        logging.info("Insurance agent graph initialized successfully")
        return app
    
    except Exception as e:
        app_exc = CustomException(e, sys)
        logging.error("Failed to build insurance agent graph")
        logging.error(app_exc)