import os
from pathlib import Path
from typing import TypedDict

import uvicorn
from fastapi import FastAPI, HTTPException
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, Field

MEMOS = [
    {
        "id": 1,
        "title": "스프린트 일정",
        "content": "백엔드 API 연동은 수요일까지 완료한다. UI 초안은 금요일까지 제출한다.",
    },
    {
        "id": 2,
        "title": "역할 분담",
        "content": "테스트 케이스는 이개발이 작성한다. 중간 점검 회의는 다음 주 월요일이다.",
    },
    {
        "id": 3,
        "title": "저장 방식",
        "content": "회의 메모는 SQLite에 저장하기로 결정했다. 벡터 DB는 이번 스프린트에서 쓰지 않는다.",
    },
]

class ChatState(TypedDict):
    question: str
    history: str
    context: str
    answer: str

class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1)
    history: str = ""

class ChatResponse(BaseModel):
    answer: str


def load_env() -> None:
    """프로젝트 루트 .env를 읽습니다. 이미 설정된 환경 변수는 그대로 둡니다."""
    try:
        from dotenv import load_dotenv
    except ImportError:
        return
    root = Path(__file__).resolve().parents[1] # 현재 파일 위치에서 1단계 위에 있는 폴더를 가리킵니다.
    load_dotenv(root / ".env")

load_env()

app = FastAPI(
    title="메모 챗봇",
    description="미리 저장한 메모만 근거로 답하는 LangGraph API",
    version="1.0.0",
)


def load_memos(state: ChatState) -> dict:
    """미리 저장해 둔 메모 전체를 답변 근거로 넣습니다."""
    context = memo_context()
    print(f"[node:load_memos] 메모 {len(MEMOS)}개")
    return {"context": context}

def memo_context() -> str:
    blocks = []
    for memo in MEMOS:
        blocks.append(f"#{memo['id']} {memo['title']}\n{memo['content']}")
    return "\n\n".join(blocks)

def answer(state: ChatState) -> dict:
    """메모 안에서만 LLM이 답하게 합니다."""
    from openai import OpenAI

    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    history = state["history"].strip() or "(None)"
    response = client.chat.completions.create(
        model=model,
        temperature=0.2,
        messages=[
            {
                "role": "system",
                "content": (
                    "당신은 회의 메모 도우미입니다. "
                    "아래 메모에 적힌 내용만 근거로 한국어로 짧게 답하세요. "
                    "메모에 없는 내용은 추측하지 말고, 메모에 없다고 말하세요. "
                    "답변 앞에 '질문:'이나 '답변:' 같은 말은 붙이지 마세요."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"메모:\n{state['context']}\n\n"
                    f"이전 대화:\n{history}\n\n"
                    f"질문: {state['question']}"
                ),
            },
        ],
    )
    text = (response.choices[0].message.content or "").strip()
    print(f"[node:answer] {model}")
    return {"answer": text}

def build_graph():
    graph = StateGraph(ChatState)
    graph.add_node("load_memos", load_memos)
    graph.add_node("answer", answer)
    graph.add_edge(START, "load_memos")
    graph.add_edge("load_memos", "answer")
    graph.add_edge("answer", END)
    return graph.compile()

GRAPH = build_graph()


# 127.0.0.1:8200/health
@app.get("/health")
def health():
    return {
        "status": "ok",
        "memos": len(MEMOS),
        "openai_configured": bool(os.getenv("OPENAI_API_KEY", "").strip()),
    }

@app.get("/memos")
def list_memos():
    return MEMOS

@app.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest):
    question = payload.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="질문을 입력하세요.")
    if not os.getenv("OPENAI_API_KEY", "").strip():
        raise HTTPException(
            status_code=500,
            detail="OPENAI_API_KEY가 없습니다. 프로젝트 루트 .env에 키를 넣어 주세요.",
        )
    result = GRAPH.invoke(
        {
            "question": question,
            "history": payload.history,
            "context": "",
            "answer": "",
        }
    )
    return {"answer": result["answer"]}


if __name__ == "__main__":
    uvicorn.run("04_memo_chat:app", host="127.0.0.1", port=8200, reload=False)