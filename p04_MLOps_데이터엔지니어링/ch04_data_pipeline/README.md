# 04. 데이터 파이프라인 — 날씨 ETL (Open-Meteo, 무료·키 불필요)

```bash
pip install pandas numpy requests
python pipeline.py --days 7
```

```
[Extract]   Open-Meteo API: 186행
[Transform] 입력 행 191 / 중복 제거 후 186 / 기온 이상치 2 / 결측치(보간 전) 11
[Validate]  통과
[Load]      186행 적재 → weather.db (테이블 누적 186행)

서울 일별 날씨 리포트
        날짜  최저기온  최고기온  평균기온  평균습도  강수량
2026-10-13  14.8  19.6  17.7  85.0 20.5
...
```

## 단계별 코드

| 단계 | 함수 | 하는 일 |
|---|---|---|
| Extract | `extract()` | 공개 API 호출 (실패 시 샘플 데이터로 대체) |
| (실습용) | `inject_dirty_data()` | 결측·이상치(85℃)·`"N/A"` 문자열·중복 행을 일부러 섞음 |
| Transform | `transform()` | 중복 제거 → 타입 변환 → 이상치 제거 → 보간 → 파생 변수(날짜·시간·주말) |
| Validate | `validate()` | 중복·결측·범위 검사, 실패 시 적재 중단 |
| Load | `load()` | SQLite `ON CONFLICT DO UPDATE` (UPSERT) |
| Report | `daily_report()` | SQL 집계 → `daily_report.csv` |

## 확인해 볼 것

1. 두 번 연속 실행해도 `테이블 누적` 행 수가 늘지 않습니다 → **멱등성**
2. `--clean-only`로 실행하면 이상치·결측치 수가 0이 됩니다 → 오염 주입의 효과 비교
3. `validate()`의 기온 범위를 `between(-40, 20)`으로 바꾸면 검증 실패로 적재가 중단됩니다

## 자동 실행 (스케줄링)

- Windows: 작업 스케줄러 → 매일 07:00 `python pipeline.py --days 1`
- macOS/Linux: `crontab -e` → `0 7 * * * cd /경로 && python pipeline.py --days 1`
- 실무: Apache Airflow DAG로 `extract >> transform >> validate >> load >> report` 구성

> 초기화하려면 `weather.db` 파일을 삭제하세요.
