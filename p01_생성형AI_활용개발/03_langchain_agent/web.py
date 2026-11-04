"""LangChain 에이전트 & 파이프라인 브라우저 실습 서버.

실행: uvicorn web:app --reload  →  http://127.0.0.1:8000
"""
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

import agent
import llm
import pipeline

app = FastAPI(title="LangChain 에이전트 & 파이프라인")


class Question(BaseModel):
    question: str = Field(min_length=1, max_length=300)


class Article(BaseModel):
    article: str = Field(min_length=10, max_length=5000)


@app.get("/")
def index():
    return FileResponse(Path(__file__).parent / "index.html")


@app.get("/api/info")
def info():
    # 키 값 자체는 절대 응답에 넣지 않고, 설정 여부만 알려준다
    return {"mode": llm.mode(), "env_file": str(llm.ROOT_ENV), "env_exists": llm.ROOT_ENV.exists()}


@app.get("/api/sample")
def sample():
    return {"article": pipeline.ARTICLE.strip()}


@app.post("/api/agent")
def run_agent(body: Question):
    return call_llm(agent.run_agent, body.question)


@app.post("/api/pipeline")
def run_pipeline(body: Article):
    return call_llm(pipeline.run_pipeline, body.article)


def call_llm(func, arg):
    """LLM 오류(한도 초과·키 오류 등)를 500 대신 이해하기 쉬운 메시지로 돌려준다."""
    try:
        return func(arg)
    except Exception as e:  # Gemini 라이브러리마다 예외 종류가 달라 메시지 내용으로 구분
        status, message = llm.explain_error(e)
        raise HTTPException(status, message) from e
