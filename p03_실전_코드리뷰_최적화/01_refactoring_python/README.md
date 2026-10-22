# 01. Python 리팩토링 & 성능 최적화

```bash
pip install pytest ruff
pytest -q                                  # before/after 결과가 같은지 확인 (리팩토링 안전망)
python benchmark.py                        # 속도 비교
python -m cProfile -s cumtime before.py    # 프로파일링: 어디서 시간이 오래 걸리는지
ruff check before.py after.py              # 린터가 찾은 문제 비교
```

## 1단계: 직접 리뷰해 보기

`before.py`를 읽고 리뷰 코멘트를 5개 이상 적어 보세요. 그다음 아래 정답과 비교합니다.

<details><summary>리뷰 포인트 정답</summary>

| # | 문제 | 분류 | after.py의 해결 |
|---|---|---|---|
| 1 | `proc`, `d`, `v`, `r`, `t`, `s` — 의미 없는 이름 | 가독성 | `build_report`, `orders`, `vip_customers` |
| 2 | 한 함수가 가격 계산·보고서·중복 검사를 모두 함 | 단일 책임 | `subtotal`, `final_price`, `find_duplicate_ids`로 분리 |
| 3 | `0.1`, `5000`, `50000`, `3000` 매직 넘버 | 유지보수 | 이름 있는 상수 |
| 4 | **이중 반복문으로 중복 검사 → O(n²)** | **성능** | `Counter`로 O(n) |
| 5 | `in v` (리스트 검색)를 주문마다 반복 → O(n×m) | 성능 | `set`으로 O(1) |
| 6 | `dup` 리스트에 `not in` 검사 | 성능 | Counter 결과 사용 |
| 7 | 문자열 `+=` 반복 연결 | 성능 | 리스트 → `"".join()` |
| 8 | `!= None` | 컨벤션 | `is not None` 또는 `dict.get` 활용 |
| 9 | 쿠폰 중첩 if, `s = s + 0` 같은 의미 없는 코드 | 가독성 | `max(..., 0)`, 조건 하나로 단순화 |
| 10 | `range(len(d))` 인덱스 반복 | 파이썬다움 | 직접 반복, `zip` |
</details>

## 2단계: 성능 측정 결과 (예시, PC마다 다름)

```
주문   500건 | before      57.8 ms | after     1.9 ms |     30배 빠름
주문  1000건 | before     207.2 ms | after     4.1 ms |     50배 빠름
주문  2000건 | before     880.9 ms | after     3.7 ms |    236배 빠름
주문  4000건 | before    4378.8 ms | after    10.7 ms |    411배 빠름
```

주문 수가 늘어날수록 차이가 커집니다. **알고리즘(자료구조) 개선이 가장 큰 성능 향상**을 가져옵니다.

## 3단계: 도전 과제

- `final_price`에 "주말 5% 추가 할인" 규칙을 추가하고 테스트를 먼저 작성해 보세요 (TDD).
