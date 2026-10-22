# 기여 가이드 (팀 규칙 예시)

## 브랜치
- `main`: 배포 가능 상태. 직접 push 금지, PR로만 merge
- `feature/<이슈번호>-<설명>`, `fix/<이슈번호>-<설명>`

## 커밋 메시지 (Conventional Commits)
```
feat: 새 기능      fix: 버그 수정      refactor: 동작 변화 없는 구조 개선
docs: 문서         test: 테스트        chore: 빌드·설정
```
예: `feat: 주문 기간 필터 추가 (#21)`

## Pull Request
1. PR 템플릿을 채운다 (`Closes #이슈번호` 포함)
2. 400줄 이하로 작게 나눈다
3. CI(린트·테스트) 통과 + 리뷰 1명 이상 승인 후 merge
4. merge 방식: **Squash and merge** (커밋 이력을 깔끔하게)

## 코드 리뷰 말머리
`[필수]` 꼭 고쳐야 함 · `[제안]` 고려해 주세요 · `[질문]` 궁금해요 · `[사소]` 오타·취향
