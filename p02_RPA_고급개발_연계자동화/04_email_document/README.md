# 04. 이메일 & 문서 처리 자동화 — 수료증 메일 머지

실제 메일은 발송되지 않습니다. 내 PC의 **테스트 메일 서버**가 메일을 받아 `inbox/` 폴더에 저장합니다.

```bash
pip install aiosmtpd python-docx openpyxl

# 방법 1: 터미널 두 개
python mail_server.py        # 터미널 1
python mail_merge.py         # 터미널 2

# 방법 2: 한 번에
python mail_merge.py --demo
```

## 결과

| 위치 | 내용 |
|---|---|
| `members.xlsx` | 명단 (첫 실행 시 자동 생성, 직접 수정 가능) |
| `output/수료증_이름.docx` | 개인별 Word 수료증 |
| `output/send_result.xlsx` | 건별 발송 성공/실패 기록 |
| `inbox/*.eml` | 테스트 서버가 받은 메일 (메일 프로그램이나 메모장으로 열기) |

명단의 `박지훈`은 이메일 주소가 잘못되어 **실패로 기록되고, 나머지는 계속 발송**됩니다.

## 실제 Gmail로 보내려면 (선택)

1. Google 계정 → 보안 → 2단계 인증 켜기 → **앱 비밀번호** 발급
2. 코드 수정

```python
smtp = smtplib.SMTP("smtp.gmail.com", 587)
smtp.starttls()
smtp.login(os.environ["GMAIL_USER"], os.environ["GMAIL_APP_PASSWORD"])
```

> 비밀번호를 코드에 쓰지 말고 환경 변수로 관리하세요. 처음에는 **본인 주소로 1건만** 테스트하세요.
