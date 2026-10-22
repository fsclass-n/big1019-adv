# 01. MLflow 실험 추적 & 모델 레지스트리 (무료, 로컬)

```bash
pip install mlflow scikit-learn
python train.py
mlflow ui --backend-store-uri sqlite:///mlflow.db     # http://127.0.0.1:5000
```

## 하는 일

1. 와인 분류 데이터로 로지스틱 회귀를 **10가지 설정**(스케일링 여부 × 규제 강도 C)으로 학습
2. 실행(run)마다 **파라미터·성능·모델 파일**을 MLflow에 기록
3. F1 점수가 가장 높은 모델을 **레지스트리에 등록**하고 `champion` 별칭 부여
4. `models:/wine-classifier@champion` 주소로 모델을 불러와 예측

## 실행 결과

```
lr_scale0_C0.001     accuracy=0.796  f1=0.766
lr_scale0_C0.1       accuracy=0.981  f1=0.981
lr_scale1_C0.01      accuracy=1.000  f1=1.000
...
최고 모델: lr_scale1_C0.01 (f1=1.000) → wine-classifier v1 @champion
```

같은 모델이라도 **전처리(스케일링)와 하이퍼파라미터**에 따라 성능이 크게 달라집니다. 이런 차이를 기록 없이 기억하기는 불가능하기 때문에 실험 추적이 필요합니다.

## MLflow UI에서 해볼 것

- **Experiments → wine-classification**: 10개 run을 표로 보고 `f1_macro` 기준 정렬
- run 여러 개 체크 → **Compare**: 파라미터와 성능의 관계를 그래프로 확인
- **Models → wine-classifier**: 버전과 `champion` 별칭 확인
- `train.py`를 한 번 더 실행하면 버전 2가 생깁니다 → 별칭만 옮기면 서비스 모델이 교체됩니다

## 생성되는 파일 (Git에 올리지 않음)

- `mlflow.db` — 실험 기록 DB
- `mlruns/` — 모델 파일(아티팩트)
