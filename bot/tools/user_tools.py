#  Copyright (c) 2024.  Tharuka Pavith
#  For the full license text, see the LICENSE file.

from langchain.tools import tool
from dotenv import load_dotenv
import requests
import os

load_dotenv()

BASE_URL = os.environ["FINTRACKER_BASE_URL"]


@tool
def get_user_by_email_tool(email: str) -> str:
    """Look for the user with a given email address"""
    response = requests.get(f"{BASE_URL}/users/email/{email}")
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return f"Error: {response.status_code}"


@tool
def get_user_by_id_tool(user_id: int) -> str:
    """Look for the user with the given user id"""
    response = requests.get(f"{BASE_URL}/users/{user_id}")
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return f"Error: {response.status_code}"
