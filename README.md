# FinTracker Bot

FinTracker Bot is an LLM-powered chatbot that helps users manage their finances through intelligent conversations.It integrates with the FinTracker API to provide personalized insights and financial management tools. 

## Key Features (Planned)

* **Multiple Platforms:**  Initially supporting a web-based widget, with plans to expand to a Telegram bot.
* **LLM-Powered:** Uses a Large Language Model (LLM) for natural language understanding and response generation.
* **Financial Insights:** Provides users with summaries of their financial data and spending analysis.

## Project Structure

* **`bot/`:**  Core chatbot logic (LLM interaction, API calls).
* **`platforms/`:** Platform-specific implementations (Telegram, web GUI).
* **`config/`:** (Optional) Configuration files for the bot.
* **`tests/`:**  Unit and integration tests.

## Getting Started

1. **Prerequisites:**
   * Python 3.7+
   * Access to the [FinTracker API](https://github.com/cey-labs/fin-tracker-backend) (running locally)
   * [OpenAI API key](https://platform.openai.com/) 

2. **Installation:**
   * Setup the project in your local environment.
   ```bash
   git clone https://github.com/cey-labs/fin-tracker-bot.git
   cd fin-tracker-bot
   pip install -r requirements.txt
   ```
   * Create a `.env` file and add following variables.
   ```commandline
   OPENAI_API_KEY="<paste your OpenAI API key here>"
   FINTRACKER_BASE_URL="http://localhost:8000"
   ```
3. **Running:**
   * Run `/bot/conversational_agent.py` to run bot in commandline.
