# mcp06_project

**MeetMind** — an AI meeting assistant project. Meetings are created and analyzed in a Gradio UI, recorded speech is transcribed and split by speaker with offline models, and a chatbot answers questions based on saved meeting notes. See [docs/planning.md](docs/planning.md) for the plan.

The [exam/](exam/) folder holds small examples, one per building block of the project.

## Setup Notes

`.env`, `.venv/`, audio files, the SQLite database and enrolled voice data are not included in this repository (see [.gitignore](.gitignore)). To run the examples, prepare the environment below.

- **Packages**
  Create a virtual environment (Python 3.12) and install:
  ```
  pip install gradio fastapi uvicorn httpx pydantic langgraph openai python-dotenv
  pip install torch numpy soundfile sounddevice qwen-asr pyannote.audio
  ```
  The second line is only needed for the speech examples (05–07).

- **Environment variables** (`.env`)
  Create a `.env` file in this folder (`mcp06_project/`, not `exam/`). Each example reads only the keys it needs.
  ```
  OPENAI_API_KEY=
  OPENAI_MODEL=
  HF_TOKEN=
  SLACK_WEBHOOK_URL=
  ```
  - `OPENAI_API_KEY`: issued from the [OpenAI Platform](https://platform.openai.com/api-keys). Used by `04_memo_chat.py`.
  - `OPENAI_MODEL`: optional; falls back to `gpt-4o-mini`.
  - `HF_TOKEN`: a [Hugging Face](https://huggingface.co/settings/tokens) access token. Used by `07_pyannote.py` to download the speaker embedding model.
  - `SLACK_WEBHOOK_URL`: a Slack [Incoming Webhook](https://api.slack.com/messaging/webhooks) URL. Used by `08_mcp.py`.

  Optional tuning keys: `ASR_MODEL_PATH` (default `Qwen/Qwen3-ASR-1.7B`), `ASR_LANGUAGE` (default `Korean`), `ASR_DTYPE`, `ASR_MAX_SECONDS`, `ASR_CHUNK_SECONDS`, `ASR_SILENCE_RMS`, `ASR_MIC_DEVICE`, `MIC_DEVICE`, `SPEAKER_EMBEDDING_MODEL`, `SPEAKER_MATCH_THRESHOLD`.

> API keys, tokens and webhook URLs are personal credentials — never commit `.env`.

## Running the Examples

Run each command from the `exam/` folder.

| Example | Command | Address |
|---|---|---|
| Gradio basics | `python 01_gradio1.py` / `python 02_gradio2.py` | http://127.0.0.1:7860 / 7861 |
| FastAPI + Gradio | server `03_main.py`, then UI `python 03_app.py` in another terminal | API :8100, UI :7862 |
| Memo chatbot | `python 04_memo_chat.py`, then `python 04_memo_ui.py` in another terminal | API :8200, UI :7863 |
| ASR from a file | `python 05_Qwen3_test.py <audio.wav>` | — |
| Live ASR | `python 06_Qwen3_live.py` (`--list-devices` to find the mic) | — |
| Speaker enrollment | `python 07_pyannote.py add <name>`, then `python 07_pyannote.py enroll <name>` | — |
| Slack message | `python 08_mcp.py <message>` | — |
| SQLite | `python 09_sqlite.py` (creates `demo.db`) | — |

The ASR examples download the Qwen3-ASR model on first run; a GPU is recommended. Enrolled voice embeddings are saved to `exam/speakers/`, which is kept out of the repository because it is personal voice data.
