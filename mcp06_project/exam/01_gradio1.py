import gradio as gr


def greet(name: str) -> str:
    name = (name or "").strip()
    if not name:
        return "이름을 입력해 주세요."
    return f"안녕하세요, {name}님! 프로젝트 예제에 오신 것을 환영합니다."


demo = gr.Interface(
    fn=greet,
    inputs=gr.Textbox(label="이름", placeholder="예: 김사과"),
    outputs=gr.Textbox(label="결과"),
    title="01. Gradio 미니 예제",
    description="함수 하나를 웹 UI로 만든 가장 작은 예제입니다.",
)

if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7860)