import os
import streamlit as st

import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.embeddings import HuggingFaceEmbeddings



genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

class Model:


    def embed_model():

        model_path = "bkai-foundation-models/vietnamese-bi-encoder"
        
        model_kwargs = {'device': 'cpu'}
        embeddings = HuggingFaceEmbeddings(
            model_name=model_path,
            model_kwargs=model_kwargs,
)

        return embeddings
    

    def llm_model():

        model = ChatGoogleGenerativeAI(model="models/gemini-1.5-pro", client=genai, temperature=0.3)

        return model