#  Copyright (c) 2024.  Tharuka Pavith
#  For the full license text, see the LICENSE file.

from typing import Optional, Type

from langchain.tools import BaseTool, tool
from langchain.pydantic_v1 import BaseModel, Field
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from dotenv import load_dotenv
import requests
from enum import Enum
from datetime import datetime, timezone
import os

load_dotenv()

BASE_URL = os.environ["FINTRACKER_BASE_URL"]


class CreateTransactionInput(BaseModel):
    account_id: int = Field(description="id of the account")
    amount: float = Field(description="transaction amount")
    transaction_type: str = Field(description="transaction type: 'CASH_IN' or 'CASH_OUT'")
    description: str = Field(description="transaction description")


class CreateTransactionTool(BaseTool):
    name = "create_transaction_tool"
    description = "useful to create a transaction for a account is given"
    args_schema: Type[BaseModel] = CreateTransactionInput

    def _run(self, account_id: int, amount: float, transaction_type: str, description: str,
             run_manager: Optional[CallbackManagerForToolRun] = None
             ) -> str:
        """Use the tool to create a new transaction"""
        if transaction_type not in ("CASH_OUT", "CASH_IN"):
            return "Error occurred: transaction_type should be 'CASH_OUT' or 'CASH_IN'"
        headers = {
            "Content-Type": "application/json",
            # TODO: authentication headers
        }
        transaction_data = {
            "amount": amount,
            "description": description,
            "type": transaction_type,
            "timestamp": str(datetime.now(timezone.utc))
        }

        try:
            response = requests.post(f"{BASE_URL}/transactions/{account_id}", json=transaction_data,
                                     headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors

            if response.status_code == 200:  # 201 Created
                created_transaction = response.json()
                return f"Transaction created: {created_transaction}"
            else:
                return f"Unexpected response: {response.status_code} - {response.text}"

        except requests.exceptions.RequestException as error:
            return f"An error occurred: {error}"


create_transaction_tool = CreateTransactionTool()


@tool
def get_transactions_by_account_id_tool(account_id: int) -> str:
    """Look for the transactions with the given account id"""
    response = requests.get(f"{BASE_URL}/transactions/{account_id}")
    if response.status_code == 200:
        data = response.json()
        if len(data) == 0:
            return "Warning: No transactions found in this account!"
        else:
            return data
    else:
        return f"Error: {response.status_code}"
