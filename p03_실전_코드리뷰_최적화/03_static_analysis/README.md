# 03. 정적 분석 — Ruff(바로 실습) + SonarQube(Docker 선택)

## A. Ruff로 Python 정적 분석 (설치 1분)

```bash
pip install ruff
ruff check .                 # ruff.toml 의 규칙으로 legacy_app.py 분석
ruff check . --statistics    # 규칙별 개수 요약
ruff check . --fix           # 자동 수정 가능한 것(안 쓰는 import 등) 수정
```

### 실행 결과

```
legacy_app.py:2:8:   F401 `os` imported but unused
legacy_app.py:7:15:  S105 Possible hardcoded password assigned to: "DB_PASSWORD"
legacy_app.py:12:17: S608 Possible SQL injection vector through string-based query construction
legacy_app.py:16:23: B006 Do not use mutable data structures for argument defaults
legacy_app.py:22:12: S602 `subprocess` call with `shell=True` identified, security issue
legacy_app.py:25:5:  C901 `grade` is too complex (7 > 6)
legacy_app.py:40:9:  E722 Do not use bare `except`
legacy_app.py:45:9:  SIM115 Use a context manager for opening files
legacy_app.py:46:12: S307 Use of possibly insecure function; consider using `ast.literal_eval`
Found 12 errors.
```

| 코드 | 문제 | 고치는 법 |
|---|---|---|
| S105 | 비밀번호 하드코딩 | `os.environ["DB_PASSWORD"]` |
| S608 | SQL 문자열 연결 → SQL 인젝션 | `cur.execute("... WHERE name = ?", (username,))` |
| B006 | 기본값이 리스트 → 호출할 때마다 **같은 리스트가 공유**되는 버그 | `tags=None` 후 `tags = tags or []` |
| S602 | `shell=True` + 사용자 입력 → 명령어 주입 | `subprocess.run(["tar", "czf", "backup.tgz", path])` |
| C901 | 분기가 너무 많음 | 점수 구간을 리스트로 만들어 반복 |
| E722/S110 | 모든 예외를 삼키고 무시 | 구체적인 예외만 잡고 로그 남기기 |
| SIM115 | 파일을 닫지 않음 | `with open(path) as f:` |
| S307 | `eval()` → 임의 코드 실행 | `json.load()` 또는 `ast.literal_eval()` |

**도전**: `legacy_app.py`를 고쳐 `ruff check .` 결과를 0개로 만들어 보세요.

## B. SonarQube (Docker Desktop 필요, 선택)

```bash
docker compose up -d           # http://localhost:9000 접속, admin / admin 로그인 후 비밀번호 변경
```

1. **Create a local project** → Project key: `static-analysis-practice`
2. **Locally** 분석 선택 → 토큰 생성 (`sqp_...`)
3. 스캐너 실행 (Docker로 설치 없이)

```bash
# macOS / Linux / Git Bash
docker run --rm --network host -e SONAR_HOST_URL=http://localhost:9000 \
  -e SONAR_TOKEN=발급받은토큰 -v "$(pwd):/usr/src" sonarsource/sonar-scanner-cli
# Windows Docker Desktop은 SONAR_HOST_URL=http://host.docker.internal:9000 사용
```

4. 대시보드에서 Bugs / Vulnerabilities / Security Hotspots / Code Smells 확인

> Docker가 없다면 **SonarQube Cloud**(공개 GitHub 저장소 무료) 또는 VS Code의 **SonarQube for IDE** 확장(무료)으로 같은 규칙을 체험할 수 있습니다.
