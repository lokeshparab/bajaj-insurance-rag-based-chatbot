
from langchain.prompts import ChatPromptTemplate

SYS_REASONER_PROMPT = (
    "You are an Bajaj Alliance Insurance Assistant which use give suitable plans details of the customer. "
    "Use the following pieces of retrieved context which has plans and details of insurance to answer the question. "
    "If you don't know the answer, just say that you don't know. "
    "Use three sentences maximum and keep the answer concise.\n"
    "Question: {question}\n"
    "Context: {context}\n"
    "Answer: "
)

def create_chat_prompt(
        sys_template: str, 
        human_template: str = "user query:{query}", 
        input_variables: list[str]=["query"],
        additional_messages: list[tuple[str,str]] = [],
        **kwargs
    ) -> ChatPromptTemplate:

    """
    Creates a ChatPromptTemplate for the given system and human templates.

    Args:
        sys_template (str): The system template message.
        human_template (str, optional): The human template message. Defaults to "user query:{query}".
        input_variables (list[str], optional): The input variables for the prompt. Defaults to ["query"].
        additional_messages (list[tuple[str,str]], optional): Additional messages to include in the prompt. Defaults to [].
        **kwargs: Additional keyword arguments to pass to the ChatPromptTemplate constructor.

    Returns:
        ChatPromptTemplate: The created ChatPromptTemplate.
    """
    messages = [("system", sys_template)] + additional_messages + [("human", human_template)]
    return ChatPromptTemplate(
        messages=messages,
        input_variables=input_variables,
        **kwargs
    )

REASONER_AGENT = ChatPromptTemplate(
    [
        ("system",SYS_REASONER_PROMPT),
        (
            "human", "Question: {query}\n Context: {context}\n Answer: "
        )
    ]
)