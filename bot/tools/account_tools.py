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
import os

load_dotenv()

BASE_URL = os.environ["FINTRACKER_BASE_URL"]


class CreateAccountInput(BaseModel):
    user_id: int = Field(description="id of the user")
    account_name: str = Field(description="account name")
    description: str = Field(description="account description")


class CreateAccountTool(BaseTool):
    name = "create_account_tool"
    description = "useful to create account for user when user id, account name and description is given"
    args_schema: Type[BaseModel] = CreateAccountInput

    def _run(self, user_id: int, account_name: str, description: str,
             run_manager: Optional[CallbackManagerForToolRun] = None
             ) -> str:
        """Use the tool to create a new user account"""
        headers = {
            "Content-Type": "application/json",
            # TODO: authentication headers
        }
        account_data = {
            "name": account_name,
            "description": description
        }

        try:
            response = requests.post(f"{BASE_URL}/accounts/{user_id}", json=account_data,
                                     headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors

            if response.status_code == 200:  # 200 Created
                created_transaction = response.json()
                return f"Account created: {created_transaction}"
            else:
                return f"Unexpected response: {response.status_code} - {response.text}"

        except requests.exceptions.RequestException as error:
            return f"An error occurred: {error}"


create_account_tool = CreateAccountTool()


@tool
def get_account_by_user_id_tool(user_id: int) -> str:
    """Look for the account with the given user id"""
    response = requests.get(f"{BASE_URL}/accounts/{user_id}")
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return f"Error: {response.status_code}"
