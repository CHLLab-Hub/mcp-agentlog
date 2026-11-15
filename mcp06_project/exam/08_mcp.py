import os
import sys
import httpx
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MAX_CHARS = 3500


def load_dotenv() -> None:
    env_path = ROOT / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def webhook_url() -> str:
    load_dotenv()
    return os.getenv("SLACK_WEBHOOK_URL", "").strip()


def send_text(text: str) -> None:
    message = text.strip()
    if not message:
        print("보낼 문장이 비어 있습니다.")
        sys.exit(1)
    if len(message) > MAX_CHARS:
        message = message[:MAX_CHARS]
        print(f"문장이 길어 {MAX_CHARS}자까지만 보냅니다.")

    url = webhook_url()
    if not url.startswith("https://"):
        print("SLACK_WEBHOOK_URL이 없습니다.")
        print("프로젝트 루트 .env 에 슬랙 Incoming Webhook 주소를 넣으세요.")
        print("만드는 순서는 examples/06-mcp/README.md 에 있습니다.")
        sys.exit(1)

    response = httpx.post(url, json={"text": message}, timeout=20.0)
    if response.status_code >= 400:
        print(f"슬랙이 전송을 거부했습니다 ({response.status_code}).")
        print("웹훅이 취소됐거나 주소가 잘린 경우입니다. README의 채널 연결부터 다시 만드세요.")
        sys.exit(1)
    print("슬랙으로 보냈습니다.")


def main() -> None:
    if len(sys.argv) > 1:
        send_text(" ".join(sys.argv[1:]))
        return
    print("슬랙에 올릴 문장을 입력하세요.")
    send_text(input("> "))


if __name__ == "__main__":
    main()