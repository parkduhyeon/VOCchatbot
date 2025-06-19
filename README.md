# AICC VOC chatbot

## 목차
1. 개요 및 구조
2. 1차 구현 (하나의 Flow 완성)
3. 2차 구현 (수정 및 고도화)
4. 개선 필요 사항
5. 추가 고도화 필요 사항

## 개요
- AICC(AI Contact Center) 서비스: 일반 상담원 대신 응대하는 상담형 AI 봇 서비스를 고객사에게 제공하는 서비스 (B2B / B2G)
- AICC 서비스에서 고객사들의 VOC를 RAG를 통해 분석하고 답변하는 AI 챗봇 구현
   
## 구조
- UI: Streamlit
- 데이터: AISearch(RAG) / 프롬프트 엔지니어링(더미 데이터 생성)

- 챗봇 / LLM: Azure OPENAI (gpt-4o-mini / text-embedding-3-small)
- PPT: Gamma.app (AI)

## 1차 구현 (하나의 Flow 완성)
1. 학습용 PDF 더미 데이터 생성
   - 초기 생성: Claude 활용하여 생성 -> 퀄리티가 좋았으나, 리소스 문제로 다량 생산 부족
   - ChatGPT를 통해 더미 데이터 생성 코드를 작성 -> 퀄리티가 낮지만, 다량 생성 가능
   - ![프롬프트 엔지니어링](https://github.com/user-attachments/assets/cefc8d2d-6034-4092-b3f6-d72dd299dbe7)
   - ![image](https://github.com/user-attachments/assets/8839428d-eb4d-428a-ac68-81ae5a90b25a)

2. Azure resource create
   - 리소스 그룹 / storage / aisearch / openai

3. RAG 모델 생성
   - RAG 생성 후 질문 시, 데이터를 원활하게 가져오지 못하는 이슈 발생
   - Blob Storage -> AI Search 로 데이터를 가져올 때, 데이터 벡터화를 하지 않고 가져와 생긴 이슈
   - 데이터 벡터화 후 연결 확인
  
4. 웹 앱 및 Streamlit 구현
   - Azure 웹 앱 사용 / UI: Streamlit 으로 구현
   - https://duhyeon-webapp.azurewebsites.net/

## 2차 구현 (수정 및 고도화)
1. 프롬프트 엔지니어링으로 답변 Case 구분
   - RAG를 통해 검색되지 않는 데이터는 "해당 내용의 VOC는 조회되지 않습니다." 라고 답변하도록 학습
     -> 기존 LLM이 가지고 있는 지식을 활용하지 않고, 데이터를 통해서만 답변하도록 유도
   - ![image](https://github.com/user-attachments/assets/edc00b86-ad88-46d9-8a61-5c19a4d41516)

2. 더미 데이터 개수 증가&다양한 답변 생성 하도록 데이터 생성 코드 수정

## 개선/고도화 필요사항
1. 데이터가 들어가 있음에도 불구하고, 조회되지 않는다는 답변 출력
 - ![image](https://github.com/user-attachments/assets/fcd0699e-48e8-42cc-978b-d32b6ec6fe89)

   -> 벡터 검색의 확률적 특성 때문
   -> 데이터의 양질 문제도 존재

2. 답변의 신뢰도 문제
   -> 답변을 하면, 실제로 이전에 진행되었던 voc를 다운로드받을 수 있게 구현 필요

