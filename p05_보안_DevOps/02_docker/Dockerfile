# ---- 1단계: 의존성 설치 (빌드 도구가 필요한 작업은 여기서) ----
FROM python:3.11-slim AS builder
WORKDIR /build
# 이 이미지에 필요한 패키지만 설치 (저장소 루트 requirements.txt 는 빌드 폴더 밖이라 직접 지정)
RUN pip install --no-cache-dir --prefix=/install "fastapi>=0.110" "uvicorn[standard]>=0.29" "redis>=5.0"

# ---- 2단계: 실행 이미지 (필요한 것만 복사 → 작고 안전) ----
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /install /usr/local
COPY app/ ./app/

# root가 아닌 사용자로 실행
RUN useradd --create-home --uid 10001 appuser
USER appuser

ENV PYTHONUNBUFFERED=1 APP_VERSION=v1
EXPOSE 8000
HEALTHCHECK --interval=10s --timeout=3s CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
