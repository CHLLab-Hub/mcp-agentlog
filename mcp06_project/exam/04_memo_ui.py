import gradio as gr
import httpx

BASE = "http://127.0.0.1:8200"

def send_question(message: str, history: str, transcript: str):
    message = (message or "").strip()
    history = history or ""
    transcript = transcript or ""
    if not message:
        return history, transcript, ""
    try:
        data = api(
            "POST",
            "/chat",
            {"question": message, "history": history},
            timeout=120.0,
        )
        reply = data.get("answer") or "(빈 답변)"
    except (ConnectionError, RuntimeError) as exc:
        reply = str(exc)
    history = f"{history}\n질문: {message}\n답변: {reply}".strip()
    transcript = f"{transcript}\n\n**나:** {message}\n\n{reply}".strip()
    return history, transcript, ""


def clear_chat():
    return "", "", ""


def api(method: str, path: str, payload: dict | None = None, timeout: float = 10.0):
    """FastAPI에 요청을 보내고 JSON을 돌려준다. 실패하면 사람이 읽을 문구를 던진다."""
    try:
        with httpx.Client(timeout=timeout) as client:
            response = client.request(method, f"{BASE}{path}", json=payload)
    except httpx.ConnectError as exc:
        raise ConnectionError(
            "FastAPI에 연결하지 못했습니다. 다른 터미널에서 `python memo_chat.py`를 먼저 실행하세요."
        ) from exc

    if response.status_code >= 400:
        detail = response.text
        try:
            detail = response.json().get("detail", detail)
        except Exception:
            pass
        raise RuntimeError(f"API 오류 ({response.status_code}): {detail}")

    if not response.content:
        return {}
    return response.json()

def format_memos(memos: list[dict]) -> str:
    if not memos:
        return "_저장된 메모가 없습니다._"
    blocks = ["## 저장된 메모"]
    for memo in memos:
        blocks.append(f"**#{memo['id']} {memo['title']}**\n\n{memo['content']}")
    return "\n\n".join(blocks)

def refresh():
    try:
        health = api("GET", "/health")
        memos = api("GET", "/memos")
    except (ConnectionError, RuntimeError) as exc:
        return f"**Disconnected** — {exc}", "_메모를 불러오지 못했습니다._"
    key = "Key O" if health.get("openai_configured") else "Key X"
    status = f"**Connected**\n\n`{BASE}` — 메모 {health.get('memos', 0)}개 / {key}"
    return status, format_memos(memos)


with gr.Blocks(title="메모 챗봇") as demo:
    gr.Markdown(
        "# 메모 챗봇\n"
        "이 화면은 Gradio입니다. 질문을 보내면 `httpx`가 "
        f"`{BASE}/chat` 을 호출하고, FastAPI 안의 LangGraph가 메모를 근거로 답합니다.\n\n"
        "먼저 다른 터미널에서 `python memo_chat.py`를 실행하세요."
    )
    status = gr.Markdown()
    memos = gr.Markdown()
    history = gr.State("")
    transcript = gr.Markdown()
    question = gr.Textbox(
        label="질문",
        placeholder="예: API 연동은 언제까지야?",
    )
    with gr.Row():
        send_btn = gr.Button("보내기", variant="primary")
        clear_btn = gr.Button("대화 지우기")

    send_btn.click(
        send_question,
        inputs=[question, history, transcript],
        outputs=[history, transcript, question],
    )
    question.submit(
        send_question,
        inputs=[question, history, transcript],
        outputs=[history, transcript, question],
    )
    clear_btn.click(clear_chat, outputs=[history, transcript, question])
    demo.load(refresh, outputs=[status, memos])


if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7863)