# 03. LangChain 파이프라인 & 에이전트 (무료)

```bash
pip install langchain-core langchain-google-genai
python pipeline.py
python agent.py "오늘 날짜와 12345 * 678 의 결과를 알려줘"
```

| 파일 | 내용 |
|---|---|
| `llm.py` | Gemini 모델 생성 (키 없으면 None) |
| `pipeline.py` | 프롬프트 → LLM → 파서 체인을 두 단계로 연결 (요약 → 제목) |
| `agent.py` | 계산기·날짜 도구를 쓰는 에이전트 루프 직접 구현 |

## 실행 예 (모의 모드)

```
[모델] ScriptedLLM (모의)
질문: 오늘 날짜와 12345 * 678 의 결과를 알려줘

[1단계] 도구 호출 get_today({}) → 2026-10-20 (화요일)
[1단계] 도구 호출 calculator({'expression': '12345 * 678'}) → 8369910
[2단계] 최종 답변 → 도구 실행 결과를 정리하면: 2026-10-20 (화요일) / 8369910
```

키를 설정하면 Gemini가 **스스로** 어떤 도구를 쓸지 결정합니다. 질문을 바꿔 보며 도구를 고르는지 관찰하세요.

## 도전 과제

1. 원화를 달러로 바꾸는 `krw_to_usd(amount: int)` 도구를 추가하기 (환율은 고정값)
2. `pipeline.py`에 "요약을 영어로 번역" 단계를 하나 더 연결하기
