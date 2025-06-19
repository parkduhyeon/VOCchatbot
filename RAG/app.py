import os
from dotenv import load_dotenv
from openai import AzureOpenAI
import streamlit as st


load_dotenv()

# Get environment variables
openai_endpoint = os.getenv("OPENAI_ENDPOINT")
openai_api_key = os.getenv("OPENAI_API_KEY")
chat_model = os.getenv("CHAT_MODEL")
embedding_model = os.getenv("EMBEDDING_MODEL")
search_endpoint=os.getenv("SEARCH_ENDPOINT")
search_api_key=os.getenv("SEARCH_API_KEY")
index_name = os.getenv("INDEX_NAME")

# Initialize Azure OpenAI client
chat_client = AzureOpenAI(
    api_version="2024-12-01-preview",
    azure_endpoint=openai_endpoint,
    api_key=openai_api_key
)

st.title("AICC VOC 응대 봇")
st.write("AICC 서비스와 관련된 문의사항을 질문해 주세요.")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": "너는 AICC라는 서비스를 운영하고 있는 관리자야. 'dev-embedding-3-small' 모델에서 AICC 서비스의 VOC들을 RAG를 통해서 보관하고 있는데, 사용자가 질문을 하면 이 RAG내의 데이터를 우선적으로 체크해서 답변해줘. 만약 이 RAG내에서 사용자가 원하는 답변이 없다면, '해당 내용의 VOC는 조회되지 않습니다. 다른 내용을 조회해 주세요.' 라고 답해줘."
        },
    ]

# Display chat history
for message in st.session_state.messages:
    if message["role"] != "system":  # 👈 system 메시지는 UI에 출력하지 않음
        st.chat_message(message["role"]).write(message["content"])
    # st.chat_message(message["role"]).write(message["content"])



def get_openai_response(messages):

    # Additional parameters to apply RAG pattern using the AI Search index
    rag_params = {
        "data_sources": [
            {
                # he following params are used to search the index
                "type": "azure_search",
                "parameters": {
                    "endpoint": search_endpoint,
                    "index_name": index_name,
                    "authentication": {
                        "type": "api_key",
                        "key": search_api_key,
                    },
                    # The following params are used to vectorize the query
                    "query_type": "vector",
                    "embedding_dependency": {
                        "type": "deployment_name",
                        "deployment_name": embedding_model,
                    },
                }
            }
        ],
    }
        
    # Submit the chat request with RAG parameters
    response = chat_client.chat.completions.create(
        model=chat_model,
        messages=messages,
        extra_body=rag_params
    )

    completion = response.choices[0].message.content
    return completion

# Handle user input
if user_input := st.chat_input("Enter your question: "):
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    with st.spinner("응답을 기다리는 중..."):
        response = get_openai_response(st.session_state.messages)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)
    