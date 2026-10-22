# 02. 모델 서빙 — FastAPI 예측 API + Docker

```bash
pip install -r requirements.txt
python train.py                 # model/model.joblib, model/metadata.json 생성
uvicorn app:app --reload        # http://127.0.0.1:8000/docs 에서 /predict 직접 호출
pip install pytest httpx && pytest -q
```

## API

| Method | URL | 설명 |
|---|---|---|
| GET | `/health` | 상태 확인 (로드밸런서·모니터링용) |
| GET | `/model-info` | 모델 버전, 정확도, 클래스 목록 |
| POST | `/predict` | 1~100건 일괄 예측, 확률·처리 시간 반환 |

```bash
curl -X POST http://127.0.0.1:8000/predict -H "Content-Type: application/json" \
  -d '{"items":[{"sepal_length":5.1,"sepal_width":3.5,"petal_length":1.4,"petal_width":0.2}]}'
```

```json
{"model_version":"202610201830","latency_ms":0.9,"predictions":[{"class":"setosa","probability":0.9812}]}
```

## Docker (Docker Desktop 필요)

```bash
docker build -t iris-api .
docker run --rm -p 8000:8000 iris-api
```

## 서빙 설계 포인트

| 포인트 | 코드 |
|---|---|
| 모델은 서버 시작 시 1번만 로딩 | `app.py` 상단 `joblib.load` |
| 입력 검증 (범위·개수) → 잘못된 입력은 422 | `Flower`, `Batch` (Pydantic `Field`) |
| 응답에 모델 버전 포함 → 어떤 모델이 예측했는지 추적 | `model_version` |
| 학습·서빙 라이브러리 버전 기록 | `metadata.json`의 `sklearn_version` |
| 헬스체크 | `/health`, Dockerfile `HEALTHCHECK` |
| 컨테이너를 root가 아닌 사용자로 실행 | Dockerfile `USER appuser` |
