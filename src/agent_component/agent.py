
from langchain.chat_models import init_chat_model
from langchain_core.messages import BaseMessage, AIMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import  RunnablePassthrough, Runnable

from prompt.prompt_library import create_chat_prompt, SYS_REASONER_PROMPT, REASONER_AGENT

from typing import TypedDict,Annotated
from operator import add

from src.utils import result_template
from src.agent_component import TOOL_MODELS, LLM_MODELS, TOP_K
from src.agent_component.tools import retriever
from src.rag_component.astradb import AstraDB
class AgentState(TypedDict):
    query: str
    # chat_history: list[BaseMessage]
    context: str
    answer: str
    # messages: Annotated[list[BaseMessage], add]
    # tool_calls: dict[str,dict] = {}

class Agents:

    def __init__(
            self, 
            # tool_models :list[dict[str,str]] = TOOL_MODELS,
            llm_models :list[dict[str,str]] = LLM_MODELS
        ):
        """
        Initializes the AI agent with a model name and a system prompt.

        Args:
            model_name (str): Name of the model to load (e.g., "mixtral-8x7b-32768").
            system_prompt (str): Instruction message to guide the assistant’s behavior.
        """

        # self.tool_models = tool_models
        self.llm_models = llm_models



        self.parser = StrOutputParser()



    def get_llm(self, model_name:str, temperature:float=0.2, max_tokens:int=-1):

        """
        Returns the initialized LLM model.

        Args:
            model_name (str): Name of the model to load (e.g., "mixtral-8x7b-32768").
            temperature (float): The temperature to use for the model.
            max_tokens (int): Maximum number of tokens to generate. If -1, no limit is applied.
        """
        if max_tokens == -1:
            return init_chat_model(model=f"groq:{model_name}", temperature=temperature, max_retries=3)
        
        return init_chat_model(model=f"groq:{model_name}", temperature=temperature, max_tokens=max_tokens, max_retries=3)
    
    def response_llm_manager(
            self,query:dict,models:list[str] | list[dict[str,str]],
            previous_chain:Runnable = RunnablePassthrough(), next_chain:Runnable  = RunnablePassthrough(), 
            temperature:float=0.2, max_tokens:int=-1, config:dict={}, **kwargs
        )->BaseMessage|str: 

        """
        Runs a query against a list of models.

        Args:
            query (dict): The query to run.
            models (list[str]): The list of models to run the query against.
            previous_chain (Runnable, optional): The previous chain to run. Defaults to RunnablePassthrough().
            next_chain (Runnable, optional): The next chain to run. Defaults to RunnablePassthrough().
            temperature (float, optional): The temperature to use. Defaults to 0.2.
            max_tokens (int, optional): The maximum number of tokens to generate. Defaults to -1.
            config (dict, optional): Additional configuration. Defaults to {}.
            **kwargs: Additional keyword arguments.

        Returns:
            BaseMessage: The response from the model.
        """
        for model in models:
            print(f"Invoking LLM with model: {model}, temperature: {temperature}, max_tokens: {max_tokens}")
            try:
                llm = (
                    self.get_llm(list(model.keys())[0], temperature=temperature, max_tokens=list(model.values())[0])
                    if isinstance(model, dict) else
                    self.get_llm(model, temperature=temperature, max_tokens=max_tokens)
                )

                if kwargs.get('tools', None):llm = llm.bind_tools(kwargs['tools'])

                chain = previous_chain | llm | next_chain

                response = chain.invoke(
                    query,
                    config={
                        "configurable": { **config ,"max_retries": 3 }        
                    }
                )
                return response
            
            except Exception as e:
                print(f"Failed to invoke LLM with model {model}")
                print(f"Error: {e}")
                continue

        print("All models failed, returning None.")
        return AIMessage(content="Unable to generate response for this following query")
    
    def rag_retriever(self,state: AgentState) -> AgentState:
        vector_db = AstraDB()
        docs = vector_db.rag_retrieve(state["query"], k=TOP_K)

        formatted_docs = "/n/n".join(
            f"**Metadata**: {doc.metadata}\n**Content**: {doc.page_content}"
            for doc in docs
        )

        return AgentState(
            context=formatted_docs,
            query=state["query"],
        )

    def insurance_agent(self, state: AgentState)-> AgentState:
        """
        Reasoner agent that takes the messages from the other agents and 
        generate a final answer based on the tool calls from the other agents.
        
        Args:
            state (AgentState): The state of the conversation.
            
        Returns:
            dict: A dictionary containing the messages, tool calls and agent message.
        """

        if state['context']:

            answer = self.response_llm_manager(
                query={"query": state["query"], "context": state["context"]},
                models=self.llm_models,
                previous_chain=REASONER_AGENT,
                next_chain=self.parser,
                temperature=0.1,
            )


        else:
            print("issues")
            answer = self.response_llm_manager(
                query=[SystemMessage(content=f"Close the final answer for query: {state['query']} ")] + state["messages"],
                models=self.llm_models,
                temperature=0, 
                max_tokens=500,
            )

        
            
        return AgentState(
            query=state["query"],
            context=state["context"],
            answer=answer
            # messages=state["messages"] + [response],
            # tool_calls=state["tool_calls"]
        )