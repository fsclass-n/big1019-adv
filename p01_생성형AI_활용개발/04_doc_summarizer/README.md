# 04. 회의록 요약 & 보고서 생성 (무료)

```bash
pip install google-genai      # 키가 없으면 설치하지 않아도 오프라인 모드로 동작
python summarize.py sample_meeting.txt
```

결과 파일

- `output/summary.txt` — 3줄 요약
- `output/report.md` — 결정사항·할 일 표·다음 회의가 정리된 보고서

## 두 모드 비교

| | 키 없음 (오프라인) | 키 있음 (Gemini) |
|---|---|---|
| 요약 | 단어 빈도가 높은 문장 3개를 **추출** | 내용을 이해해 새 문장으로 **생성** |
| 정보 추출 | 정규식 (`OO은 X월 Y일까지 ...`) | JSON 모드 (`response_mime_type`) |
| 긴 문서 | - | 3,000자 단위 Map-Reduce |

두 모드로 각각 실행해 결과를 비교해 보세요. 오프라인 모드는 문장 형식이 조금만 달라도 할 일을 못 찾지만, LLM은 유연하게 찾아냅니다.

## 도전 과제

1. 본인 팀의 실제 회의록 텍스트로 실행해 보기
2. `render_report()`를 바꿔 `python-docx`로 Word 파일 만들기
