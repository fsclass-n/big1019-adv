# 03. SageMaker 스크립트 모드 — 로컬 무료 실습 + AWS 실행(선택)

## A. 로컬에서 무료로 (AWS 계정 불필요)

```bash
pip install scikit-learn pandas joblib
python local_test.py
```

```
[1] 학습 데이터 준비: 150행 → ...\opt\ml\input\data\train
[2] Training Job 흉내: train.py --n_estimators 50 --learning_rate 0.1
    로그: validation_accuracy=0.9667 | 모델 파일: ['model.joblib']
[3] Endpoint 요청 흉내
    요청: {"instances": [[5.1, 3.5, 1.4, 0.2], [6.7, 3.0, 5.2, 2.3]]}
    응답: {"predictions": [{"class": "setosa", ...}, {"class": "virginica", ...}]}
```

`local_test.py`는 SageMaker 컨테이너와 **같은 폴더 구조(`/opt/ml/...`)와 환경 변수**를 만들어 `train.py`를 실행합니다. 여기서 성공하면 SageMaker에서도 거의 그대로 동작합니다.

| 파일 | SageMaker에서의 역할 |
|---|---|
| `train.py` | Training Job 컨테이너에서 실행되는 학습 코드 |
| `inference.py` | Endpoint 컨테이너가 호출하는 `model_fn / input_fn / predict_fn / output_fn` |
| `local_test.py` | 위 두 파일을 로컬에서 검증 |
| `sagemaker_run.py` | 실제 AWS에 학습·배포·**삭제**까지 수행 (유료) |

## B. 실제 AWS SageMaker 실행 (선택, 유료)

> 💰 `ml.m5.large` 학습 몇 분 + `ml.t2.medium` 엔드포인트 몇 분이면 보통 수백 원 수준이지만, **엔드포인트를 삭제하지 않으면 계속 과금**됩니다. 신규 계정 프리티어 범위와 요금은 [SageMaker 요금](https://aws.amazon.com/sagemaker/pricing/)에서 확인하세요.

1. **예산 알림 먼저**: Billing → Budgets → 월 $5 예산 + 이메일 알림
2. IAM 역할 생성: 신뢰 대상 `SageMaker`, 정책 `AmazonSageMakerFullAccess` (실습용. 운영은 최소 권한)
3. 실행

```bash
pip install sagemaker boto3
aws configure
export SAGEMAKER_ROLE_ARN=arn:aws:iam::<계정ID>:role/<역할이름>    # PowerShell: $env:SAGEMAKER_ROLE_ARN="..."
python sagemaker_run.py
```

4. 끝난 뒤 콘솔에서 **SageMaker → Inference → Endpoints** 가 비어 있는지 꼭 확인
