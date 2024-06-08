import streamlit as st
from openai import OpenAI

# 페이지 제목 설정
st.title("친근한 챗봇 update 2 ")

api_key = st.text_input("API 키를 입력하세요:", type="password")

if api_key:
    st.session_state["api_key"] = api_key

# API 클라이언트 초기화
if "api_key" in st.session_state:
    client = OpenAI(api_key=st.session_state["api_key"])

system_message = '''
너의 이름은 친구봇이야.
너는 항상 반말을 하는 챗봇이야. 다나까나 요 같은 높임말로 절대로 끝내지 마
항상 반말로 친근하게 대답해줘.
영어로 질문을 받아도 무조건 한글로 답변해줘.
한글이 아닌 답변일 때는 다시 생각해서 꼭 한글로 만들어줘
모든 답변 끝에 답변에 맞는 이모티콘도 추가해줘
'''

# 시스템 메시지 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_message}]

# 챗 메시지 출력
for idx, message in enumerate(st.session_state.messages):
    if idx > 0:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)


    # OpenAI 모델 호출
    if "api_key" in st.session_state:
        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})

        print(st.session_state.messages)