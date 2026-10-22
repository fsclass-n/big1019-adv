# 02. UI 자동화 — 엑셀 명단을 웹 폼에 자동 입력 (Playwright)

```bash
pip install playwright openpyxl
# PC에 Edge 또는 Chrome이 있으면 바로 실행됩니다. 없으면 한 번만:
playwright install chromium

python auto_fill.py --show   # 브라우저가 직접 입력하는 모습 확인
python auto_fill.py          # 화면 없이 실행
```

- `form.html` — 연습용 "사내 교육 신청 시스템" (처리 지연을 일부러 넣어 둠)
- `applicants.xlsx` — 첫 실행 시 자동 생성되는 명단 (직접 수정해도 됨)
- 결과: `output/result.xlsx`(성공/실패 기록), `output/screenshot.png`

## 확인할 점

1. **명단의 4번째 사람(`없는과정`)은 실패**하지만 자동화는 멈추지 않고 다음 사람을 처리합니다.
2. `time.sleep()` 없이 `wait_for()`로 "신청 완료" 메시지를 기다립니다. 지연이 랜덤이어도 안정적으로 동작합니다.
3. 선택자를 `get_by_label("이름")`처럼 **사람이 보는 이름표 기준**으로 써서 HTML 구조가 바뀌어도 잘 깨지지 않습니다.

## 도전 과제

- 결과 테이블(`#rows tr`)을 읽어 엑셀 명단과 건수가 일치하는지 검증하는 코드를 추가해 보세요.
- `playwright codegen form.html` 명령으로 마우스 조작을 코드로 녹화해 보세요.
