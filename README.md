# VOCchatbot
## 개요
- 고객사들의 VOC를 요약 및 분석하고 답변하는 AI 챗봇 구현
   
## 구조
- UI: Streamlit
- 데이터: AISearch(RAG) / 프롬프트 엔지니어링(더미 데이터 생성)
- 챗봇 / LLM: Azure OPENAI (gpt-4o-mini)

## 1차 Flow
1. 학습용 더미 데이터 생성
   - 초기 생성: Claude 활용하여 생성 -> 퀄리티가 좋았으나, 리소스 문제로 다량 생산 부족
   - ChatGPT를 통해 더미 데이터 생성 코드를 작성 -> 퀄리티가 낮지만, 다량 생성 가능

2. Azure resource create
   - 리소스 그룹 / storage / aisearch / openai

3. RAG 모델 생성
   - RAG 생성 후 질문 시, 데이터를 원활하게 가져오지 못하는 이슈 발생
   - Blob Storage -> AI Search 로 데이터를 가져올 때, 데이터 벡터화를 하지 않고 가져와 생긴 이슈
   - 데이터 벡터화 후 연결 확인
  
4. 웹 앱 및 Streamlit 구현
   - Azure 웹 앱 사용 / UI: Streamlit 으로 구현
  

