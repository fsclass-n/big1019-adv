"""LangChain용 Gemini 모델 생성.

Gemini 키는 저장소 루트의 .env 파일에서 읽는다.
  GEMINI_API_KEY=발급받은키
  GEMINI_MODEL=gemini-3.1-flash-lite    (선택, 생략하면 기본값)
키가 없으면 None을 돌려 각 예제가 가짜 모델(모의 모드)로 동작하게 한다.

무료 한도는 모델마다 따로 계산된다. gemini-flash-latest 는 최신 Flash 모델(하루 20회 등 한도가 작음)을
가리키므로, 실습에는 한도가 넉넉한 Flash-Lite 모델을 기본값으로 쓴다.
"""
import os
import re
from pathlib import Path

from dotenv import load_dotenv

ROOT_ENV = Path(__file__).resolve().parents[2] / ".env"  # big1019-adv/.env (이 파일 기준 두 단계 위)
load_dotenv(ROOT_ENV)  # .env 의 키=값 을 환경 변수로 등록 (파일이 없으면 아무 일도 하지 않음)

MODEL = os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite")


def has_key():
    return bool(os.getenv("GEMINI_API_KEY"))


def mode():
    return f"Gemini {MODEL}" if has_key() else "모의 모드 (루트 .env에 GEMINI_API_KEY 없음)"


def gemini_or_none(temperature=0.3):
    if not has_key():
        return None
    from langchain_google_genai import ChatGoogleGenerativeAI

    # max_retries=1, timeout=30: 한도 초과·장애 시 오래 기다리지 않고 바로 오류를 알려준다
    return ChatGoogleGenerativeAI(model=MODEL, google_api_key=os.getenv("GEMINI_API_KEY"), temperature=temperature,
                                  max_retries=1, timeout=30)


def explain_error(e):
    """LLM 호출 오류를 (HTTP 상태 코드, 사용자에게 보여줄 메시지)로 바꾼다."""
    text = str(e)
    if "RESOURCE_EXHAUSTED" in text or "429" in text:
        period = "하루" if "per day" in text else "분당"
        retry = re.search(r"retry in ([\dhm]*\d+)(?:\.\d+)?s", text)  # 예: "retry in 18h48m25.88s"
        wait = f" — {retry.group(1).replace('h', '시간 ').replace('m', '분 ')}초 후 다시 가능" if retry else ""
        return 429, (f"Gemini 무료 사용량({period} 한도)을 초과했습니다{wait}. "
                     f"잠시 후 다시 시도하거나 루트 .env 의 GEMINI_MODEL 을 다른 모델로 바꾸세요. (현재: {MODEL})")
    if "API key not valid" in text or "API_KEY_INVALID" in text:
        return 401, "Gemini API 키가 올바르지 않습니다. 루트 .env 의 GEMINI_API_KEY 를 확인하세요."
    if "NOT_FOUND" in text or "404" in text:
        return 400, f"모델 '{MODEL}' 을(를) 찾을 수 없습니다. 루트 .env 의 GEMINI_MODEL 을 확인하세요."
    return 502, f"Gemini 호출 실패: {text[:200]}"
