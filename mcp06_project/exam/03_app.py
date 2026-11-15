# 사용자가 볼 화면
import httpx
import gradio as gr

BASE = "http://127.0.0.1:8100"

# 앱과 서버 연결
def api(method: str, path: str, payload: dict | None = None):
    """FastAPI에 요청을 보내고 JSON을 돌려준다. 실패하면 사람이 읽을 문구를 던진다."""
    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.request(method, f"{BASE}{path}", json=payload)
    except httpx.ConnectError as exc:
        raise ConnectionError(
            "FastAPI에 연결하지 못했습니다. 다른 터미널에서 `python main.py`를 먼저 실행하세요."
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

def health_text() -> str:
    try:
        data = api("GET", "/health")
    except (ConnectionError, RuntimeError) as exc:
        return f"**Disconnected** - {exc}"
    return f"**Connected**\n\n`{BASE}` — status=`{data.get('status')}` / time=`{data.get('time')}`"

# 메모 불러오기, 생성
def load_memos() -> tuple[list[dict], str | None]:
    try:
        return api("GET", "/memos"), None
    except (ConnectionError, RuntimeError) as exc:
        return [], str(exc)

def format_list(memos: list[dict]) -> str:
    if not memos:
        return "_저장된 메모가 없습니다._"
    lines = ["| id | 제목 | 작성 |", "|---:|---|---|"]
    for memo in memos:
        lines.append(f"| {memo['id']} | {memo['title']} | {memo['created_at']} |")
    return "\n".join(lines)

def as_choices(memos: list[dict], selected: str | None = None) -> gr.Dropdown:
    choices = [f"{memo['id']} | {memo['title']}" for memo in memos]
    if selected not in choices:
        selected = choices[0] if choices else None
    return gr.Dropdown(choices=choices, value=selected)

def format_memo(memo: dict) -> str:
    body = memo.get("content") or "(내용 없음)"
    return (
        f"### #{memo['id']} {memo['title']}\n"
        f"- 작성: {memo['created_at']}\n\n"
        f"{body}"
    )

def create_memo(title: str, content: str):
    title = (title or "").strip()
    if not title:
        memos, error = load_memos()
        message = f"**Disconnected** - {error}" if error else "제목을 입력하세요."
        return message, format_list(memos), as_choices(memos)

    try:
        memo = api("POST", "/memos", {"title": title, "content": content or ""})
        memos, _ = load_memos()
    except (ConnectionError, RuntimeError) as exc:
        return str(exc), gr.skip(), gr.skip()

    label = f"{memo['id']} | {memo['title']}"
    return format_memo(memo), format_list(memos), as_choices(memos, label)

# 목록 새로고침
def refresh():
    memos, error = load_memos()
    if error:
        status = f"**Disconnected** - {error}"
    else:
        status = health_text()
    return status, format_list(memos), as_choices(memos)

# ID로 파싱하여 메모 선택 후 상세보기
def parse_id(label: str | None) -> int | None:
    if not label:
        return None
    return int(str(label).split("|", 1)[0].strip())

def show_memo(label: str | None):
    memo_id = parse_id(label)
    if memo_id is None:
        return "메모를 선택하세요."
    try:
        return format_memo(api("GET", f"/memos/{memo_id}"))
    except (ConnectionError, RuntimeError) as exc:
        return str(exc)


# 메모 삭제
def remove_memo(label: str | None):
    memo_id = parse_id(label)
    if memo_id is None:
        return "삭제할 메모를 선택하세요.", gr.skip(), gr.skip()
    try:
        api("DELETE", f"/memos/{memo_id}")
        memos, _ = load_memos()
    except (ConnectionError, RuntimeError) as exc:
        return str(exc), gr.skip(), gr.skip()
    return f"#{memo_id} 메모를 삭제했습니다.", format_list(memos), as_choices(memos)


with gr.Blocks(title="FastAPI + Gradio") as demo:
    gr.Markdown(
        "# Gradio → FastAPI\n"
        "이 화면은 HTML이 아니라 Gradio입니다. 버튼을 누르면 `httpx`가 "
        f"`{BASE}`의 REST API를 호출합니다.\n\n"
        "먼저 다른 터미널에서 `python app.py`를 실행하세요."
    )
    status = gr.Markdown()
    check_btn = gr.Button("연결 확인")

    with gr.Row():
        with gr.Column():
            gr.Markdown("## 메모 작성")
            title = gr.Textbox(label="제목", placeholder="예: 스프린트 메모")
            content = gr.Textbox(
                label="내용",
                lines=4,
                placeholder="예: API 연동 일정 공유",
            )
            create_btn = gr.Button("저장", variant="primary")
        with gr.Column():
            gr.Markdown("## 결과")
            created = gr.Markdown()

    gr.Markdown("## 저장된 메모")
    refresh_btn = gr.Button("목록 새로고침")
    table = gr.Markdown()
    picker = gr.Dropdown(label="메모 선택", choices=[])
    with gr.Row():
        show_btn = gr.Button("상세 보기")
        delete_btn = gr.Button("삭제")
    detail = gr.Markdown()

    check_btn.click(health_text, outputs=status)
    create_btn.click(create_memo, inputs=[title, content], outputs=[created, table, picker])
    refresh_btn.click(refresh, outputs=[status, table, picker])
    show_btn.click(show_memo, inputs=picker, outputs=detail)
    delete_btn.click(remove_memo, inputs=picker, outputs=[detail, table, picker])
    demo.load(refresh, outputs=[status, table, picker])


if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7862)