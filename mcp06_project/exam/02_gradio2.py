import gradio as gr


def make_meeting(title: str, people: str) -> str:
    title = (title or "").strip()
    if not title:
        return "제목을 입력하세요."
    names = [p.strip() for p in (people or "").split(",") if p.strip()]
    return (
        f"### 회의 생성됨\n"
        f"- 제목: **{title}**\n"
        f"- 참가자: {', '.join(names) or '(없음)'}"
    )


def summarize(text: str) -> str:
    text = (text or "").strip()
    if not text:
        return "회의록이 비어 있습니다."
    lines = [ln for ln in text.splitlines() if ln.strip()]
    return f"발화 {len(lines)}줄 / 앞부분: {lines[0][:40] if lines else ''}"


with gr.Blocks(title="Gradio Tabs 예제") as demo:
    gr.Markdown("# Gradio Tabs 미니 예제\n본편의 탭 UI를 아주 작게 축소한 버전입니다.")

    with gr.Tab("회의 생성"):
        title = gr.Textbox(label="제목", value="주간 회의")
        people = gr.Textbox(label="참가자(쉼표)", value="김매니저, 이개발")
        btn1 = gr.Button("생성", variant="primary")
        out1 = gr.Markdown()
        btn1.click(make_meeting, inputs=[title, people], outputs=out1)

    with gr.Tab("간단 요약"):
        raw = gr.Textbox(label="회의록", lines=6, value="김: 목표 공유\n이: API 완료 예정")
        btn2 = gr.Button("요약")
        out2 = gr.Markdown()
        btn2.click(summarize, inputs=raw, outputs=out2)


if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7861)