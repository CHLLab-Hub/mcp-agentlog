import os
import sys
from pathlib import Path

import numpy as np
import soundfile as sf
import torch


# 음성이 너무 작을 경우 전체 음량을 키워주는 함수
def peak_normalize(wav: np.ndarray, target: float = 0.9) -> np.ndarray:
    peak = float(np.max(np.abs(wav))) if wav.size else 0.0
    if peak < 1e-6: # 음성이 거의 없으면 그대로 돌려줌
        return wav
    if peak >= target: # 이미 충분히 크면 그대로 돌려줌
        return wav
    return (wav * (target / peak)).astype(np.float32)


# WAV 전체가 아닌 소리가 큰 일정 구간을 잘라주는 함수
def loudest_slice(wav: np.ndarray, sr: int, seconds: float, search_seconds: float = 600.0) -> tuple[np.ndarray, float]:
    """앞쪽 search_seconds 안에서 평균 에너지가 가장 큰 구간을 고릅니다."""
    want = int(seconds * sr)
    if wav.shape[0] <= want:
        return wav, 0.0
    limit = min(wav.shape[0], int(search_seconds * sr))
    hop = int(5 * sr)
    best_start = 0
    best_rms = -1.0
    for start in range(0, max(1, limit - want + 1), hop):
        chunk = wav[start : start + want]
        rms = float(np.sqrt(np.mean(chunk * chunk)))
        if rms > best_rms:
            best_rms = rms
            best_start = start
    return wav[best_start : best_start + want], best_start / sr


# 16kHz로 변환하고 모노(1차원 배열)로 바꿔주는 함수
def load_16k_mono(path: Path) -> np.ndarray:
    wav, sr = sf.read(str(path), always_2d=False)
    if getattr(wav, "ndim", 1) > 1:
        wav = wav.mean(axis=1)
    wav = wav.astype(np.float32)
    if int(sr) == 16000:
        return wav
    duration = wav.shape[0] / float(sr)
    n16 = int(round(duration * 16000))
    x_old = np.linspace(0.0, duration, num=wav.shape[0], endpoint=False)
    x_new = np.linspace(0.0, duration, num=n16, endpoint=False)
    return np.interp(x_new, x_old, wav).astype(np.float32)


def resolve_runtime(torch):
    """CUDA를 우선하고, 없으면 MPS, 그것도 없으면 CPU를 고릅니다."""
    requested = os.getenv("ASR_DTYPE", "").strip().lower()

    def pick_dtype(default: str):
        name = requested or default
        if name == "float32":
            return torch.float32
        if name == "float16":
            return torch.float16
        if name == "bfloat16":
            return torch.bfloat16
        print(f"알 수 없는 ASR_DTYPE={name}. {default}을 사용합니다.")
        name = default
        return {"float32": torch.float32, "float16": torch.float16, "bfloat16": torch.bfloat16}[name]

    if torch.cuda.is_available():
        return "cuda:0", pick_dtype("bfloat16"), f"CUDA {torch.cuda.get_device_name(0)}"
    if torch.backends.mps.is_available():
        return "mps", pick_dtype("float16"), "Apple MPS"
    return "cpu", pick_dtype("float32"), "CPU"


def main() -> None:
    if len(sys.argv) < 2:
        print("사용법: python <file.py> <audio.wav>")
        print("예: python 05_Qwen3_test.py sample.wav")
        sys.exit(1)

    audio_path = Path(sys.argv[1])
    if not audio_path.exists():
        print(f"파일 없음: {audio_path}")
        sys.exit(1)

    model_path = os.getenv("ASR_MODEL_PATH", "Qwen/Qwen3-ASR-1.7B")
    language = os.getenv("ASR_LANGUAGE", "Korean")
    device, dtype, device_label = resolve_runtime(torch)

    print(f"장치: {device_label} ({device}, {dtype})")
    if not device.startswith("cuda"):
        print("CUDA가 없어 이 장치로 실행합니다. 메모리가 부족하면 ASR_MODEL_PATH=Qwen/Qwen3-ASR-0.6B 를 쓰세요.")
    print(f"[1/3] 오디오 로드: {audio_path}")
    wav = load_16k_mono(audio_path)
    duration = wav.shape[0] / 16000
    peak = float(np.max(np.abs(wav))) if wav.size else 0.0
    rms = float(np.sqrt(np.mean(wav * wav))) if wav.size else 0.0
    print(f"      samples={wav.shape[0]}, duration={duration:.2f}s, peak={peak:.4f}, rms={rms:.4f}")

    # 0이면 전체를 전사합니다. 기본 20초는 RTX 3060에서 첫 테스트용입니다.
    max_seconds = float(os.getenv("ASR_MAX_SECONDS", "20"))
    if max_seconds > 0 and duration > max_seconds:
        wav, offset = loudest_slice(wav, 16000, max_seconds)
        print(
            f"      파일이 {duration:.0f}초라 {offset:.0f}초 지점부터 {max_seconds:.0f}초만 전사합니다. "
            "전체를 쓰려면 ASR_MAX_SECONDS=0 을 설정하세요."
        )

    before = float(np.max(np.abs(wav))) if wav.size else 0.0
    wav = peak_normalize(wav)
    after = float(np.max(np.abs(wav))) if wav.size else 0.0
    if after > before + 1e-6:
        print(f"      음량이 작아 peak {before:.3f} -> {after:.3f} 로 키웠습니다.")
    # 주의할 점: peak_normalize는 음량을 키우지만, 불필요한 잡음까지 키우므로, target 값을 조절해서 사용

    print(f"[2/3] Qwen3 ASR 로드 ({device}): {model_path}")
    from qwen_asr import Qwen3ASRModel

    asr = Qwen3ASRModel.from_pretrained(
        model_path,
        dtype=dtype,
        device_map=device,
        max_inference_batch_size=4,
        max_new_tokens=256,
    )

    print("[3/3] 전사 중...")
    results = asr.transcribe(audio=(wav, 16000), language=language)
    text = (getattr(results[0], "text", None) or "").strip()
    print("\n=== 결과 ===")
    print(text or "(빈 결과)")


if __name__ == "__main__":
    main()