# 사용자의 입력을 받아 줄 서버
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import uvicorn

app = FastAPI(
    title="FastAPI 미니 예제",
    description="회의 메모를 메모리에만 잠깐 저장하는 아주 작은 API",
    version="1.0.0",
)

_MEMOS: list[dict] = []
_NEXT_ID = 1

class MemoCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100) # 제목(1 ~ 100자)
    content: str = ""

class Memo(BaseModel):
    id: int
    title: str
    content: str 
    created_at: str # 생성날짜


# 127.0.0.1: 자기 자신의 컴퓨터 주소
# 8100: FastAPI 서버가 실행되는 포트
# 127.0.0.1:8100/health
@app.get("/health")
def health():
    return {"status": "ok", "time": datetime.now().isoformat(timespec="seconds")}

@app.post("/memos", response_model=Memo)
def create_memo(payload: MemoCreate):
    global _NEXT_ID
    memo = {
        "id": _NEXT_ID,
        "title": payload.title,
        "content": payload.content,
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }
    _NEXT_ID += 1
    _MEMOS.append(memo)
    return memo

# 127.0.0.1:8100/memos
@app.get("/memos", response_model=list[Memo])
def list_memos():
    return list(reversed(_MEMOS))

# 127.0.0.1:8100/memos/(memo_id): 메모 return
@app.get("/memos/{memo_id}", response_model=Memo)
def get_memo(memo_id: int):
    for memo in _MEMOS:
        if memo["id"] == memo_id:
            return memo
    raise HTTPException(status_code=404, detail="메모를 찾을 수 없습니다.")

@app.delete("/memos/{memo_id}")
def delete_memo(memo_id: int):
    for i, memo in enumerate(_MEMOS):
        if memo["id"] == memo_id:
            _MEMOS.pop(i)
            return {"deleted": True, "id": memo_id}
    raise HTTPException(status_code=404, detail="메모를 찾을 수 없습니다.")


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8100, reload=False)