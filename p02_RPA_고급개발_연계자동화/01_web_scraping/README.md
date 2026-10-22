# 01. 웹 스크래핑 — 연습용 서점 사이트

[books.toscrape.com](https://books.toscrape.com)은 **스크래핑 연습용으로 만들어진 공개 사이트**입니다.

```bash
pip install requests beautifulsoup4 pandas openpyxl
python scrape_books.py --pages 3
```

결과: `output/books.csv`, `output/books.xlsx` (전체 시트 + 평점별 통계 시트)

## 코드에서 볼 부분

| 함수 | 포인트 |
|---|---|
| `fetch()` | 타임아웃, 상태 코드 확인, 실패 시 재시도 |
| `parse_page()` | CSS 선택자 `article.product_pod`, `p.price_color` 로 값 추출 |
| `main()` | 페이지 사이 `delay`, `utf-8-sig`로 엑셀 한글 깨짐 방지, 시트 2개 저장 |

## 도전 과제

1. 각 책의 상세 페이지(`링크`)에 들어가 **상품 설명**까지 수집하기
2. 가격이 £20 이하이고 평점 4 이상인 책만 별도 시트로 저장하기
3. 브라우저 개발자 도구(F12)로 다른 정보(카테고리)의 선택자를 찾아 추가하기
