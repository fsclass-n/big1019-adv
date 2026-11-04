# 실행: pytest ex06_pytest.py -v      (ch06_fastAPI 폴더에서)
# ex01 ~ ex05 의 API 를 서버를 띄우지 않고 TestClient 로 자동 테스트한다.
import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# ex02 를 import 하기 전에 DB_HOST 를 빈 값으로 → .env 의 실제 TiDB 대신 SQLite 사용 (실제 DB 를 건드리지 않음)
os.environ["DB_HOST"] = ""

import ex01_uvicorn  # noqa: E402
import ex02_sqlalchemy  # noqa: E402
import ex03_pydantic  # noqa: E402
import ex04_apirouter  # noqa: E402
import ex05_jwt  # noqa: E402


# ---------------------------------------------------------------- ex01: 기본 라우팅
def test_ex01_root():
  client = TestClient(ex01_uvicorn.app)
  res = client.get("/")
  assert res.status_code == 200
  assert "message" in res.json()


def test_ex01_path_and_query():
  client = TestClient(ex01_uvicorn.app)
  assert client.get("/items/5", params={"q": "hello"}).json() == {"item_id": 5, "query_string": "hello"}
  assert client.get("/items/5").json()["query_string"] is None  # q 생략 → 기본값 None


def test_ex01_type_validation():
  res = TestClient(ex01_uvicorn.app).get("/items/abc")
  assert res.status_code == 422
  assert res.json()["detail"][0]["type"] == "int_parsing"


def test_ex01_html_escape():
  res = TestClient(ex01_uvicorn.app).get("/hello", params={"name": "<script>"})
  assert "&lt;script&gt;" in res.text and "<script>" not in res.text  # XSS 방지 확인


# ---------------------------------------------------------------- ex02: DB (테스트 전용 DB 로 교체)
@pytest.fixture
def db_client():
  """테스트마다 새 메모리 DB 를 만들고, get_db 의존성을 그 DB 로 바꿔 끼운다."""
  engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
  ex02_sqlalchemy.Base.metadata.create_all(bind=engine)
  TestSession = sessionmaker(bind=engine)

  def override_get_db():
    db = TestSession()
    try:
      yield db
    finally:
      db.close()

  ex02_sqlalchemy.app.dependency_overrides[ex02_sqlalchemy.get_db] = override_get_db
  yield TestClient(ex02_sqlalchemy.app)
  ex02_sqlalchemy.app.dependency_overrides.clear()  # 다른 테스트에 영향이 없도록 원래대로


def test_ex02_create_and_list(db_client):
  res = db_client.post("/users/", params={"name": "홍길동", "email": "hong@example.com"})
  assert res.status_code == 200
  assert res.json()["user"]["id"] == 1
  assert [u["email"] for u in db_client.get("/users/").json()] == ["hong@example.com"]


def test_ex02_duplicate_email(db_client):
  db_client.post("/users/", params={"name": "a", "email": "dup@example.com"})
  res = db_client.post("/users/", params={"name": "b", "email": "dup@example.com"})
  assert res.status_code == 400
  assert len(db_client.get("/users/").json()) == 1  # rollback → 두 번째는 저장되지 않음


def test_ex02_db_is_isolated(db_client):
  assert db_client.get("/users/").json() == []  # 앞 테스트의 데이터가 남아 있지 않음


# ---------------------------------------------------------------- ex03: Pydantic 검증 (parametrize)
@pytest.mark.parametrize("body, status, error_type", [
    ({"name": "노트북", "price": 1000, "tax": 100}, 200, None),
    ({"name": "a", "price": 1000}, 422, "string_too_short"),
    ({"name": "노트북", "price": 0}, 422, "greater_than"),
    ({"price": 1000}, 422, "missing"),
    ({"name": "노트북", "price": "abc"}, 422, "float_parsing"),
])
def test_ex03_validation(body, status, error_type):
  res = TestClient(ex03_pydantic.app).post("/items/", json=body)
  assert res.status_code == status
  if error_type:
    assert res.json()["detail"][0]["type"] == error_type


def test_ex03_total_price():
  res = TestClient(ex03_pydantic.app).post("/items/", json={"name": "노트북", "price": 1000, "tax": 100})
  assert res.json()["data"]["total_price"] == 1100


# ---------------------------------------------------------------- ex04: 라우터
def test_ex04_routers():
  client = TestClient(ex04_apirouter.app)
  assert client.get("/users/").status_code == 200
  assert client.get("/items/").json()[0]["item_name"] == "노트북"
  assert client.post("/users/", params={"name": "kim"}).json()["message"] == "유저 'kim' 생성 완료!"
  assert client.get("/orders/").status_code == 404  # 등록하지 않은 라우터


# ---------------------------------------------------------------- ex05: JWT 인증
@pytest.fixture
def jwt_client():
  return TestClient(ex05_jwt.app)


@pytest.fixture
def token(jwt_client):
  res = jwt_client.post("/login", data={"username": "haewon", "password": "password123"})
  return res.json()["access_token"]


def test_ex05_login_fail(jwt_client):
  res = jwt_client.post("/login", data={"username": "haewon", "password": "wrong"})
  assert res.status_code == 401


def test_ex05_protected_without_token(jwt_client):
  assert jwt_client.get("/users/me").status_code == 401


def test_ex05_protected_with_token(jwt_client, token):
  res = jwt_client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
  assert res.status_code == 200
  assert res.json()["username"] == "haewon"


def test_ex05_tampered_token(jwt_client, token):
  res = jwt_client.get("/users/me", headers={"Authorization": f"Bearer {token[:-3]}abc"})
  assert res.status_code == 401  # 서명 불일치


def test_ex05_expired_token(jwt_client, monkeypatch):
  monkeypatch.setattr(ex05_jwt, "ACCESS_TOKEN_EXPIRE_MINUTES", -1)  # 테스트 동안만 값 변경 → 이미 만료된 토큰
  expired = jwt_client.post("/login", data={"username": "haewon", "password": "password123"}).json()["access_token"]
  assert jwt_client.get("/users/me", headers={"Authorization": f"Bearer {expired}"}).status_code == 401


def test_ex05_secret_key_from_env(monkeypatch, jwt_client, token):
  monkeypatch.setattr(ex05_jwt, "SECRET_KEY", "different-key")  # 서명 키가 바뀌면 기존 토큰은 무효
  assert jwt_client.get("/users/me", headers={"Authorization": f"Bearer {token}"}).status_code == 401
