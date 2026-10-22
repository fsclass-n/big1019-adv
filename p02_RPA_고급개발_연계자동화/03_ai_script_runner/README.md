# 03. AI 기반 자동화 스크립트 — 계획 → 검증 → 미리보기 → 실행

```bash
pip install google-genai   # 선택: 키가 없으면 규칙 기반으로 동작
python run.py "pdf는 documents 폴더로 옮기고 이름 앞에 오늘 날짜를 붙여줘"        # 미리보기
python run.py "pdf는 documents 폴더로 옮기고 이름 앞에 오늘 날짜를 붙여줘" --yes  # 실행
python run.py "사진은 images 폴더로 정리해줘" --yes
python run.py --plan evil_plan.json   # 위험한 계획 → 검증 단계에서 전부 거부
python run.py --reset                 # sandbox 폴더 초기화
```

## 실행 예

```
■ 계획 (규칙 기반 파서(모의))
  {"action": "mkdir", "path": "documents"}
  {"action": "move", "src": "*.pdf", "dst": "documents"}
  {"action": "rename_prefix", "pattern": "documents/*.pdf", "prefix": "2026-10-20_"}

■ 미리보기 (dry-run)
  폴더 생성  documents/
  이동      invoice_10월.pdf → documents/invoice_10월.pdf
  이동      report.pdf → documents/report.pdf
  이름 변경  invoice_10월.pdf → 2026-10-20_invoice_10월.pdf
  ...
```

```
python run.py --plan evil_plan.json
■ 검증 실패 — 실행하지 않습니다
  ✘ 1번: 작업 폴더 밖 경로 '../../'
  ✘ 2번: 허용되지 않은 작업 'delete'
  ✘ 3번: 허용되지 않은 작업 'shell'
  ✘ 4번: 접두어에 사용할 수 없는 문자
```

## 안전 장치 정리

| 장치 | 코드 위치 |
|---|---|
| 허용 작업 화이트리스트 | `ALLOWED` |
| 작업 폴더 밖 경로 차단 | `inside_sandbox()` |
| 작업 수 상한 | `MAX_STEPS` |
| 미리보기 후 `--yes`로만 실행 | `main()` |
| 멱등성 (두 번 실행해도 안전) | `execute()` — 이미 있는 폴더·접두어 건너뜀 |
| 실행 로그 | `run.log` |
