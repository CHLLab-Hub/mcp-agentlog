# mcp05_agent

## Setup Notes

`.env` and `.venv/` are not included in this repository (see `.gitignore`). To reproduce [01_Agent.ipynb](01_Agent.ipynb), prepare the environment below.

- **Packages**
  Create a virtual environment (Python 3.12) and install:
  ```
  pip install ipykernel langgraph langchain langchain-openai langchain-tavily python-dotenv
  ```

- **Environment variables** (`.env`)
  Create a `.env` file in this folder. It is loaded by `load_dotenv()` in the notebook.
  ```
  OPENAI_API_KEY=
  OPENAI_MODEL=
  TAVILY_API_KEY=
  ```
  - `OPENAI_API_KEY`: issued from the [OpenAI Platform](https://platform.openai.com/api-keys).
  - `OPENAI_MODEL`: name of the chat model to use. Optional; the notebook falls back to `gpt-4o-mini` when it is not set.
  - `TAVILY_API_KEY`: issued from [Tavily](https://app.tavily.com/). Read from the environment by `TavilySearch`.

> API keys are personal credentials — they are not bundled in this repository. Never commit `.env`.

- **Which sections need a key**
  Sections 1–3 (AI Agent, RAG, LangGraph) run without any key. From section 4 (Tool Calling) the notebook calls the OpenAI API, and section 5 (Web Search) also calls the Tavily API. Both are billed or quota-limited per request.
