from langchain_core.messages import RemoveMessage
from langchain_core.runnables import RunnableConfig

# from langchain_community.chat_models.fake import FakeListChatModel
from philoagents.application.conversation_service.workflow.chains import (
    get_conversation_summary_chain,
    get_philosopher_response_chain,
)
from philoagents.application.conversation_service.workflow.state import PhilosopherState
from philoagents.config import settings

# from typing import Any


# class FakeChatModel(FakeListChatModel):
#     async def ainvoke(self, input: Any, config: Any = None):
#         if isinstance(input, dict):
#             messages = input.get("messages", [])
#         elif isinstance(input, list):
#             messages = input
#         else:
#             raise ValueError(
#                 f"Invalid input type {type(input)}. Expected dict or list of BaseMessages."
#             )

#         return await super().ainvoke(messages, config)


async def conversation_node(state: PhilosopherState, config: RunnableConfig):
    summary = state.get("summary", "")
    conversation_chain = get_philosopher_response_chain()

    response = await conversation_chain.ainvoke(
        {
            "messages": state["messages"],
            "philosopher_context": state["philosopher_context"],
            "philosopher_name": state["philosopher_name"],
            "philosopher_perspective": state["philosopher_perspective"],
            "philosopher_style": state["philosopher_style"],
            "summary": summary,
        },
        config,
    )

    return {"messages": response}


async def summarize_conversation_node(state: PhilosopherState):
    summary = state.get("summary", "")
    summary_chain = get_conversation_summary_chain(summary)

    response = await summary_chain.ainvoke(
        {
            "messages": state["messages"],
            "philosopher_name": state["philosopher_name"],
            "summary": summary,
        }
    )

    delete_messages = [
        RemoveMessage(id=m.id)
        for m in state["messages"][: -settings.TOTAL_MESSAGES_AFTER_SUMMARY]
    ]

    return {"summary": response.content, "messages": delete_messages}
