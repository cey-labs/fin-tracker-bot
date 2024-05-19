#  Copyright (c) 2024.  Tharuka Pavith
#  For the full license text, see the LICENSE file.

from typing import Sequence
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain.memory import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from dotenv import load_dotenv

from bot.prompts import SYSTEM_MESSAGE
from bot.tools.user_tools import get_user_by_id_tool, get_user_by_email_tool
from bot.tools.account_tools import create_account_tool, get_account_by_user_id_tool
from bot.tools.transaction_tools import create_transaction_tool, get_transactions_by_account_id_tool

load_dotenv()

tools: Sequence = [get_user_by_id_tool, get_user_by_email_tool,
                   create_account_tool, get_account_by_user_id_tool,
                   create_transaction_tool, get_transactions_by_account_id_tool]

llm = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_MESSAGE),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

agent = create_openai_tools_agent(llm=llm, tools=tools, prompt=prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False)

chat_history_for_chain = ChatMessageHistory()


def get_openai_tools_agent():
    conversational_agent_executor = RunnableWithMessageHistory(
        agent_executor,
        lambda session_id: chat_history_for_chain,
        input_messages_key="input",
        output_messages_key="output",
        history_messages_key="chat_history",
    )
    return conversational_agent_executor


if __name__ == '__main__':

    agent_executor = get_openai_tools_agent()
    while True:
        user_msg = input("[user]>>> ")
        if user_msg == "/exit":
            break

        result = agent_executor.invoke(
            {"input": user_msg},
            {"configurable": {"session_id": "unused"}},
        )
        print("[assistant]>>> ", result["output"])
