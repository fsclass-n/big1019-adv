"""LangChain용 Gemini 모델 생성.

Gemini 키는 저장소 루트의 .env 파일에서 읽는다.
  GEMINI_API_KEY=발급받은키
  GEMINI_MODEL=gemini-flash-latest      (선택, 생략하면 기본값)
키가 없으면 None을 돌려 각 예제가 가짜 모델(모의 모드)로 동작하게 한다.
"""
import os
from pathlib import Path

from dotenv import load_dotenv

ROOT_ENV = Path(__file__).resolve().parents[2] / ".env"  # big1019-adv/.env (이 파일 기준 두 단계 위)
load_dotenv(ROOT_ENV)  # .env 의 키=값 을 환경 변수로 등록 (파일이 없으면 아무 일도 하지 않음)

MODEL = os.getenv("GEMINI_MODEL", "gemini-flash-latest")


def has_key():
    return bool(os.getenv("GEMINI_API_KEY"))


def mode():
    return f"Gemini {MODEL}" if has_key() else "모의 모드 (루트 .env에 GEMINI_API_KEY 없음)"


def gemini_or_none(temperature=0.3):
    if not has_key():
        return None
    from langchain_google_genai import ChatGoogleGenerativeAI

    return ChatGoogleGenerativeAI(model=MODEL, google_api_key=os.getenv("GEMINI_API_KEY"), temperature=temperature)
