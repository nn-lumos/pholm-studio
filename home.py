import streamlit as st
import os

from utils.prepare_vector_db import get_documents, get_chunks, get_vector_store
from utils.component import generate_session_id, get_response, clear_history
from utils.models import Model


embedding = Model.embed_model()
llm = Model.llm_model()


def main():


    if "session_id" not in st.session_state:

        st.session_state.session_id = generate_session_id()

    session_id = st.session_state.session_id


    with st.sidebar:

        documents = st.file_uploader("",type=['txt','doc','docx','pdf'],accept_multiple_files=True)
        
        if st.button("Tải lên"):
            with st.spinner("Đang xử lý..."):
                raw_chunk = get_documents(documents)
                chunks = get_chunks(raw_chunk)
                get_vector_store(chunks,session_id)
                st.success("Tải lên thành công!")

    st.title("PhoLM Studio")
    st.sidebar.button("Xóa lịch sử", on_click=clear_history)

    if "messages" not in st.session_state:
        
        st.session_state.messages = [
            {"role": "assistant", "content": "Hãy tải lên tài liệu của bạn và đặt câu hỏi với tôi."}
        ]

    for messages in st.session_state.messages:
        with st.chat_message(messages["role"]):
            st.write(messages["content"])

    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        
        if st.session_state.messages[-1]["role"] != "assistant":
            with st.chat_message("assistant"):
                with st.spinner("Đang tìm câu trả lời..."):
                    response = get_response(prompt,session_id)
                    placeholder = st.empty()
                    full_response = ''
                    for item in response["output_text"]:
                        full_response += item
                        placeholder.markdown(full_response)
                    placeholder.markdown(full_response)

                if response is not None:
                    messages = {"role": "assistant", "content": full_response}
                    st.session_state.messages.append(messages)


if __name__ == "__main__":

    main()
    
