
# 🛡 WHS Phishing URL Detector

> 화이트햇스쿨 2기 프로젝트 — 머신러닝 (**LGBM**) + 딥러닝 (**CNN**) 앙상블 (URL을 통해 피싱 여부 판별)


<p align="center">
  <a href="https://c0mput33-whs-detector.streamlit.app">
    <img src="https://img.shields.io/badge/Demo-Streamlit-ff4b4b?logo=streamlit&logoColor=white" />
  </a>
  <a href="https://colab.research.google.com/github/C0mput33/whs-phishing-detector/blob/main/notebooks/Ensemble.ipynb">
    <img src="https://img.shields.io/badge/Run_in_Colab-F9AB00?logo=googlecolab&logoColor=white" />
  </a>
  <a href="docs/논문%20초안_2.pdf">
    <img src="https://img.shields.io/badge/Paper-PDF-blueviolet" />
  </a>
  <a href="docs/팀_떡밥_최종발표.pdf">
    <img src="https://img.shields.io/badge/Slides-PDF-important" />
  </a>
</p>

---


## 🔥 Model Overview
| Model | Feature Set | Accuracy | Precision | Recall |
| ----- | ----------- | -------- | --------- | ------ |
| **LGBM**    | 14 URL heuristics (length, digits, entropy…) | 1.000 | 1.000 | 1.000 |
| **CNN**     | Tokenised URL sequence (char‑level)         | 0.992 | 0.990 | 0.970 |
| **Ensemble**| Soft‑Voting (LGBM + CNN)                    | **0.999** | **0.997** | **0.991** |

> 📑 세부 실험 결과와 학습 파라미터는 [`notebooks/`](notebooks/) 폴더를 참고하세요.

---


## 📊 Datasets

| 구분 | 파일 | 샘플 수 | 출처 / 비고 |
|------|------|--------:|-------------|
| **정상 사이트** | `normal_data.csv` | 50000 | Alexa |
| **피싱 사이트** | `phishing_data.xls` | 184860 | OpenPhish, PhishTank |
| **검증 셋** | `valid_data.csv` | 70000 | 정상:피싱 = 1:1 |
| **통합 & 전처리** | `model_data.csv` | 289993 | 15 features, label 포함 |


### 📑 Dataset Features
| No | Feature Name | 설명 |
| -- | ------------ | ---- |
| 1  | `url` | 원본 URL 문자열 |
| 2  | `IP_LIKE` | IP 주소 형식 여부(도메인 대신 숫자) |
| 3  | `AT` | ‘@’ 문자 포함 여부 → 리디렉션 가능성 |
| 4  | `URL_Depth` | 슬래시(⧸) 깊이, 디렉터리 단계 수 |
| 5  | `Redirection` | ‘//’ 중복 사용 횟수 |
| 6  | `Is_Https` | HTTPS 사용 (1) / 미사용 (0) |
| 7  | `TINY_URL` | URL 단축 서비스 여부 |
| 8  | `Check_Hyphen` | 도메인에 ‘-’ 하이픈 포함 여부 |
| 9  | `Query` | 쿼리 스트링( ?key= ) 존재 여부 |
| 10 | `Domain_Age` | WHOIS 기준 도메인 연령(일) |
| 11 | `Domain_end` | 도메인 만료까지 남은 기간(일) |
| 12 | `Mouseover` | HTML a 태그 〈onmouseover〉 속성 여부 |
| 13 | `Web_forwards` | 메타 리프레시 횟수 |
| 14 | `Hyperlinks` | 외부 링크 개수 |
| 15 | `Domain_Cons` | 도메인 일관성 점수 |
| 16 | `Tokenized_url` | 전처리된 URL 토큰 벡터 |
| 17 | `Label` | 0 (정상) / 1 (피싱) |

---


## 📂 Project Structure
```text
whs-phishing-detector/
├── src/
│   └── app.py                # Streamlit 대시보드
├── notebooks/
│   ├── LGBM.ipynb            # 머신러닝 실험
│   ├── CNN.ipynb             # 딥러닝 실험
│   └── Ensemble.ipynb        # Soft‑Voting 앙상블
├── data/   (Git LFS)         # raw / processed CSV · XLS
│   ├── phishing_data.xls
│   ├── normal_data.csv
│   ├── phish_dataset.ipynb   #피싱 사이트 피쳐 추출 함수
│   ├── normal_dataset1.ipynb   #정상 사이트 피쳐 추출 함수
│   ├── phish_model_temp.ipynb  #피싱 URL을 판별하는 랜덤포레스트 모델을 학습하고 Flask API로 배포하는 Jupyter 노트북
│   ├── valid_data.csv
│   └── model_data.csv
├── docs/
│   ├── 논문 초안_2.pdf    # 논문 초안 
│   ├── 피싱사이트 탐지 논문.docx    # 논문 초안 
│   └── 팀_떡밥_최종발표.pdf    # 발표 자료
└── requirements.txt
````

---


## 🚀 Quick Start

```bash
# 1. Clone & env
git clone https://github.com/C0mput33/whs-phishing-detector.git
cd whs-phishing-detector
python -m venv venv && source venv/bin/activate  # Win: .\venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt   # pandas, numpy, scikit-learn, xgboost, tensorflow, streamlit …

# 3. (옵션) Git LFS 데이터 다운로드
git lfs install
git lfs pull                      # data/, models/ 가져오기

# 4. Run Streamlit demo
streamlit run src/app.py          # http://localhost:8501
```

Colab 실행 → **“Runtime > Change runtime type > GPU”** 선택 후 `Run all` 하면 재현 가능합니다.

---


## 🛠 Key Components

| Folder / File              | 내용                                   |
| -------------------------- | ------------------------------------ |
| `src/app.py`               | URL 입력 ↔ 앙상블 예측 ↔ 결과 시각화 (Streamlit) |
| `notebooks/LGBM.ipynb`     | 14개 특징 추출 → LightGBM 학습 · SHAP 해석    |
| `notebooks/CNN.ipynb`      | URL 문자열 토큰화 → 1D CNN 모델 학습           |
| `notebooks/Ensemble.ipynb` | 로지스틱 Soft‑Voting → 최종 0.98 정확도      |
| `data/*.csv`               | 정규 / 피싱 데이터셋 (전처리 포함)                |
| `docs/`                    | 논문 PDF, 발표 슬라이드                      |

---


## 📊 Performance & Explainability

* **ROC‑AUC 1.00** (LGBM) / 0.998 (Ensemble)
* SHAP Top 3 Features : `url_entropy`, `num_dots`, `contains_https`
* Grad‑CAM 으로 CNN이 감지한 악성 토큰 시각화 → `docs/cam_examples.png`

---


## 📝 Citation

```
@misc{kim2024whsphish,
  title  = {Ensemble Learning for Phishing URL Detection},
  author = {KIM, Haechan and Team Tteok-bap},
  year   = {2024},
  note   = {WhiteHat School 2nd Generation Capstone}
}
```

---


## 🤝 Contributors

| 이름               | 역할                            |
| ---------------- | ----------------------------- |
| **김해찬** | 데이터 수집 및 전처리 · 모델링 · Streamlit      |


---

> Made with **WhiteHat School 2nd Gen (2024)**


