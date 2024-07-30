import streamlit as st
from utils.models import Model
from langchain.vectorstores import FAISS

from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate

import uuid

embedding = Model.embed_model()
llm = Model.llm_model()


def generate_session_id():
    return str(uuid.uuid4())


def clear_history():

    st.session_state.messages = [
        {"role": "assistant", "content": "Hãy tải lên tài liệu của bạn và đặt câu hỏi với tôi."}
    ]


def get_conversational_chain():

    prompt_template = """
    You are provided with content through document files. Based on the content of document files to do what users request and respond to
    in Vietnamese. If the request is not in the provided content then simply reply "Tôi không tìm thấy trong nội dung được cung cấp".\n\n
    Context:\n {context}?\n
    Question: \n{question}\n
    Answer:
    Answer:
    """

    prompt = PromptTemplate(template=prompt_template,input_variables=["context","question"])
    chain = load_qa_chain(llm=llm, chain_type="stuff", prompt=prompt)

    return chain


def get_response(user_question, session_id):

    db = FAISS.load_local(f"./db/faiss_index_{session_id}", embedding, allow_dangerous_deserialization=True)
    docs = db.similarity_search(user_question)

    chain = get_conversational_chain()
    respone = chain({"input_documents": docs, "question": user_question}, return_only_outputs=True)

    return respone