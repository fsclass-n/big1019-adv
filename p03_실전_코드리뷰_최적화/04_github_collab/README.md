# 04. GitHub 협업 & 프로젝트 관리

## 구성

| 파일 | 용도 | 사용법 |
|---|---|---|
| `.github/PULL_REQUEST_TEMPLATE.md` | PR 작성 양식 | 저장소 루트의 `.github/`로 복사하면 PR 작성 시 자동 표시 |
| `.github/ISSUE_TEMPLATE/bug_report.yml` | 버그 신고 **폼** (입력칸·드롭다운) | 〃 |
| `.github/ISSUE_TEMPLATE/feature_request.md` | 기능 요청 양식 | 〃 |
| `.github/CODEOWNERS` | 경로별 자동 리뷰어 지정 | 아이디를 팀원 계정으로 수정 |
| `.github/workflows/ci.yml` | PR마다 린트·테스트 자동 실행 | 〃 |
| `CONTRIBUTING.md` | 팀 협업 규칙 | 저장소 루트에 두기 |
| `conflict_lab.py` | **충돌 해결 연습** (로컬, 인터넷 불필요) | `python conflict_lab.py` |

> 이 폴더의 `.github/`는 하위 폴더에 있어서 **이 저장소에서는 동작하지 않습니다.** 본인 실습 저장소의 루트로 복사해 사용하세요.

## 실습 1: 충돌 해결 (혼자, 5분)

```bash
python conflict_lab.py
```

임시 폴더에 두 브랜치가 같은 줄을 고친 저장소가 만들어지고, 충돌 상태가 됩니다. 안내에 따라 직접 해결해 보세요.

## 실습 2: 팀 협업 시나리오 (2~4명, 40분)

| 단계 | 할 일 | 담당 |
|---|---|---|
| 1 | GitHub에서 새 저장소 생성, 위 `.github/` 파일과 `CONTRIBUTING.md` 추가 | 조장 |
| 2 | Settings → Branches → `main` 보호 규칙: **PR 필수, 승인 1명, CI 통과 필수** | 조장 |
| 3 | Projects(보드) 생성: Todo / In Progress / Review / Done | 조장 |
| 4 | 기능 이슈 3개 등록 (템플릿 사용), 담당자·라벨 지정, 보드에 추가 | 전원 |
| 5 | 각자 `feature/<번호>-설명` 브랜치에서 작업 → PR (`Closes #번호`) | 전원 |
| 6 | 서로 PR 리뷰: `[제안]`, `[질문]` 말머리로 코멘트 1개 이상 | 전원 |
| 7 | 승인·CI 통과 후 Squash and merge → 이슈 자동 종료, 보드 Done 확인 | 작성자 |
| 8 | 같은 파일 같은 줄을 두 명이 수정해 **충돌을 만들고 해결** | 2명 |

## gh CLI로 빠르게 (선택)

```bash
gh issue create --title "[Feature] 주문 기간 필터" --label enhancement
gh pr create --fill --base main
gh pr review 3 --approve --body "LGTM! [사소] 변수명만 확인 부탁드려요"
gh pr merge 3 --squash --delete-branch
```
