import uuid
from typing import Any, Union

from langchain_core.messages import AIMessage, HumanMessage

from philoagents.application.conversation_service.workflow.graph import (
    create_workflow_graph,
)
from philoagents.application.conversation_service.workflow.state import PhilosopherState


async def get_response(
    messages: str | list[str] | list[dict[str, Any]],
    philosopher_id: str,
    philosopher_name: str,
    philosopher_perspective: str,
    philosopher_style: str,
    philosopher_context: str,
    new_thread: bool = False,
) -> tuple[str, PhilosopherState]:
    """
    Run a conversation through the workflow graph.

    Args:
        messages: Input messages to start the conversation. Can be:
            - A single string (assumed to be from the human)
            - A list of strings (all assumed to be from the human)
            - A list of dictionaries with 'role' and 'content' keys
              (e.g., {'role': 'user', 'content': 'Hello'})
        philosopher_name: Name of the philosopher
        philosopher_perspective: Philosopher's perspective on the topic
        philosopher_style: Style of conversation (e.g., "Socratic")
        philosopher_context: Additional context about the philosopher

    Returns:
        tuple[str, PhilosopherState]: A tuple containing:
            - The content of the last message in the conversation.
            - The final state after running the workflow.

    Raises:
        RuntimeError: If there's an error running the conversation workflow.
    """

    graph_builder = create_workflow_graph()
    graph = graph_builder.compile()

    thread_id = philosopher_id if not new_thread else f"{philosopher_id}-{uuid.uuid4()}"
    config = {"configurable": {"thread_id": thread_id}}

    try:
        output_state = await graph.ainvoke(
            {
                "messages": __format_messages(messages=messages),
                "philosopher_name": philosopher_name,
                "philosopher_perspective": philosopher_perspective,
                "philosopher_style": philosopher_style,
                "philosopher_context": philosopher_context,
            },
            config=config,
        )
        last_message = output_state["messages"][-1]
        return last_message.content, PhilosopherState(**output_state)
    except Exception as e:
        raise RuntimeError(f"Error running conversation workflow: {str(e)}") from e


def __format_messages(
    messages: Union[str, list[dict[str, Any]]],
) -> list[Union[HumanMessage, AIMessage]]:
    """Convert various message formats to a list of LangChain message objects.

    Args:
        messages: Input messages, which can be:
            - A single string (assumed to be from the human)
            - A list of strings (all assumed to be from the human)
            - A list of dictionaries with 'role' and 'content' keys (e.g., {'role': 'user', 'content': 'Hello'})

    Returns:
        List[Union[HumanMessage, AIMessage]]: A list of LangChain-compatible message objects.
    """

    if isinstance(messages, str):
        return [HumanMessage(content=messages)]

    if isinstance(messages, list):
        if not messages:
            return []

        if (
            isinstance(messages[0], dict)
            and "role" in messages[0]
            and "content" in messages[0]
        ):
            result = []
            for msg in messages:
                if msg["role"] == "user":
                    result.append(HumanMessage(content=msg["content"]))
                elif msg["role"] == "assistant":
                    result.append(AIMessage(content=msg["content"]))
            return result

        return [HumanMessage(content=message) for message in messages]

    return []
