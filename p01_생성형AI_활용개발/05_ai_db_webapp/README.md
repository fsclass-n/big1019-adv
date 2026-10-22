# 05. AI 메모장 — FastAPI + SQLite + Gemini (무료)

```bash
pip install fastapi "uvicorn[standard]" google-genai
uvicorn app:app --reload
```

- 화면: http://127.0.0.1:8000
- API 문서(Swagger): http://127.0.0.1:8000/docs
- DB 파일: `notes.db` (처음 실행 시 자동 생성, SQLite 뷰어로 열어볼 수 있음)

## API

| Method | URL | 설명 |
|---|---|---|
| POST | `/notes` | 메모 저장 (AI가 요약·태그 생성) |
| GET | `/notes?tag=회의` | 메모 목록 / 태그 검색 |
| DELETE | `/notes/{id}` | 메모 삭제 |
| POST | `/ask` | 저장된 메모를 근거로 질문에 답변 (간단한 RAG) |

## 테스트

```bash
pip install pytest httpx
pytest test_app.py -v
```

테스트는 임시 DB와 모의 모드로 실행되어 API 키가 필요 없습니다. SQL 인젝션 입력(`' OR 1=1 --`)이 막히는지도 확인합니다.

## 코드에서 볼 부분

- `analyze()` — AI 호출 실패 시 규칙 기반으로 대체(Fallback)해 **AI 장애가 서비스 장애가 되지 않게** 함
- `list_notes()` — `?` 파라미터 바인딩
- `ask()` — 관련 메모 검색 → 프롬프트에 근거로 삽입 → 답변 (RAG의 기본 구조)
- `ai_source` 컬럼 — AI 결과의 출처 기록
