import os
import sys

import numpy as np


def peak_normalize(wav: np.ndarray, target: float = 0.9) -> np.ndarray:
    peak = float(np.max(np.abs(wav))) if wav.size else 0.0
    if peak < 1e-6 or peak >= target:
        return wav
    return (wav * (target / peak)).astype(np.float32)


def list_devices() -> None:
    import sounddevice as sd

    print(sd.query_devices())


def main() -> None:
    if "--list-devices" in sys.argv:
        list_devices()
        return

    import sounddevice as sd
    import torch
    from qwen_asr import Qwen3ASRModel

    if not torch.cuda.is_available():
        print("CUDA GPU를 찾지 못했습니다. NVIDIA 드라이버와 CUDA용 PyTorch를 확인하세요.")
        sys.exit(1)

    model_path = os.getenv("ASR_MODEL_PATH", "Qwen/Qwen3-ASR-1.7B")
    language = os.getenv("ASR_LANGUAGE", "Korean")
    dtype_name = os.getenv("ASR_DTYPE", "bfloat16").lower()
    dtype = torch.float16 if dtype_name == "float16" else torch.bfloat16
    chunk_seconds = float(os.getenv("ASR_CHUNK_SECONDS", "4"))
    silence_rms = float(os.getenv("ASR_SILENCE_RMS", "0.01"))
    sample_rate = 16000
    device_index = os.getenv("MIC_DEVICE", "").strip()
    mic_device = int(device_index) if device_index else None

    print(f"GPU: {torch.cuda.get_device_name(0)}")
    print(f"모델 로드: {model_path}")

    asr = Qwen3ASRModel.from_pretrained(
        model_path,
        dtype=dtype,
        device_map="cuda:0",
        max_inference_batch_size=1,
        max_new_tokens=128,
    )

    print()
    print(f"마이크를 엽니다. {chunk_seconds:.0f}초마다 전사합니다. 종료는 Ctrl+C")
    print("조용하면 건너뛰고, 말하면 그 구간의 글자가 바로 출력됩니다.")
    print()

    lines: list[str] = []
    try:
        with sd.InputStream(
            samplerate=sample_rate,
            channels=1,
            dtype="float32",
            device=mic_device,
            blocksize=int(sample_rate * chunk_seconds),
        ) as stream:
            while True:
                audio, overflowed = stream.read(int(sample_rate * chunk_seconds))
                wav = np.asarray(audio, dtype=np.float32).reshape(-1)
                rms = float(np.sqrt(np.mean(wav * wav))) if wav.size else 0.0
                if overflowed:
                    print("(마이크 버퍼가 밀렸습니다. 말을 조금 천천히 해보세요.)")
                if rms < silence_rms:
                    print(f"... 조용함 (rms={rms:.4f})")
                    continue
                wav = peak_normalize(wav)
                results = asr.transcribe(audio=(wav, sample_rate), language=language)
                text = (getattr(results[0], "text", None) or "").strip()
                if not text:
                    print("... 인식된 문장 없음")
                    continue
                lines.append(text)
                print(f">> {text}")
    except KeyboardInterrupt:
        print("\n종료합니다.")

    except Exception as exc:
        print(f"마이크를 열지 못했습니다: {exc}")
        print("장치 목록: python 06_Qwen3_live.py --list-devices")
        print("다른 마이크를 쓰려면: $env:MIC_DEVICE=\"1\"")
        sys.exit(1)

    print("\n=== 지금까지의 전사 ===")
    print("\n".join(lines) if lines else "(없음)")


if __name__ == "__main__":
    main()