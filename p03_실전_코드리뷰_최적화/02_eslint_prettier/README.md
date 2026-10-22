# 02. ESLint + Prettier 실습 (Node.js)

```bash
npm install
npm run lint            # ① 문제 찾기
npm run format:check    # ② 포맷이 맞지 않는 파일 확인
npm run lint:fix        # ③ 자동으로 고칠 수 있는 것 고치기 (var→const 등)
npm run format          # ④ Prettier로 포맷 통일
npm run lint            # ⑤ 남은 문제는 사람이 직접 수정
```

## ① `npm run lint` 결과 (cart.js)

```
src/cart.js
   2:1   error    Unexpected var, use let or const instead                      no-var
   3:7   error    'unused' is assigned a value but never used                   no-unused-vars
   5:1   warning  Function 'total' has a complexity of 7. Maximum allowed is 6  complexity
   7:9   error    Unexpected var, use let or const instead                      no-var
   8:15  error    Expected '===' and instead saw '=='                           eqeqeq
  ...
  17:5   warning  'cart' is never reassigned. Use 'const' instead               prefer-const
  19:26  error    'discont' is not defined                                      no-undef

✖ 11 problems (8 errors, 3 warnings)
```

| 규칙 | 의미 | 실행하면 생길 일 |
|---|---|---|
| `no-undef` | 선언 안 된 변수 `discont` (오타) | **실행 시 ReferenceError로 프로그램 중단** |
| `eqeqeq` | `==` 사용 | `0 == ""`가 `true` 같은 함정 |
| `no-unused-vars` | 안 쓰는 변수 | 남은 코드, 오타 신호 |
| `complexity` | if-else 분기가 너무 많음 | 테스트·수정이 어려움 → 객체 매핑으로 개선 |

`--fix`로 고쳐지지 않는 `no-undef`, `complexity`는 사람이 수정해야 합니다. 완성본은 `src/cart_fixed.js`를 참고하세요.

## VS Code 연동 (추천)

1. 확장 설치: **ESLint**, **Prettier - Code formatter**
2. 설정(`settings.json`)

```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.codeActionsOnSave": { "source.fixAll.eslint": "explicit" }
}
```

저장할 때마다 자동으로 포맷·수정됩니다.
