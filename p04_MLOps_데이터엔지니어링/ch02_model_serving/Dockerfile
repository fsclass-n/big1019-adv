# 모델 서빙 컨테이너
#   docker build -t iris-api .
#   docker run --rm -p 8000:8000 iris-api      →  http://localhost:8000  (API 문서: /docs)
FROM python:3.11-slim

WORKDIR /app
# 이 이미지에 필요한 패키지만 설치 (저장소 루트 requirements.txt 는 빌드 폴더 밖이라 직접 지정)
RUN pip install --no-cache-dir "scikit-learn>=1.4" "joblib>=1.3" "fastapi>=0.110" "uvicorn[standard]>=0.29"

COPY train.py app.py index.html ./
# 이미지 빌드 시 학습해 모델을 포함 (실무에서는 MLflow·S3 등 레지스트리에서 내려받는 방식을 많이 씀)
RUN python train.py

RUN useradd --create-home appuser
USER appuser

EXPOSE 8000
HEALTHCHECK CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
