import streamlit as st
import pandas as pd
import subprocess
from datetime import datetime
import plotly.express as px
import sys


get_data = subprocess.Popen([f'{sys.executable}', './utils/get_data.py'])


dataframe = pd.read_csv('./db/data_usage.csv')
feedback = pd.read_csv('./db/feedback.csv')


now = datetime.now().strftime('%Y-%m-%d')

st.set_page_config(page_title="Report", initial_sidebar_state="expanded")
st.title("🍲 PhoLM Report")

# 
st.header("Analysis Report: PhoLM Studio")
st.write(f"Từ 21-07-2024 đến {datetime.now().strftime('%d-%m-%Y')}")
st.write("---")


#
st.subheader("Tổng quan về dự án")
st.write("\n")
total_used, total_in_day, total_feedback = st.columns(3)

total_used.metric(
    label="Số lượt dùng:",
    value=int(dataframe["num_used"].sum())
)

total_in_day.metric(
    label="Số lượt dùng hôm nay",
    value=int(dataframe[dataframe["date"] == now]["num_used"].sum())
)

total_feedback.metric(
    label="Số lượt feedback",
    value= int(feedback.index[-1]) + 1
)


# 
st.write("---")
st.subheader("Số lượt dùng theo thời gian")
st.area_chart(dataframe,x="date",y='num_used',color=(255,127,80,0.5),x_label="Ngày",y_label="Lượt sử dụng")


# 
st.write("---")
st.subheader("Mức độ hài lòng")
st.bar_chart(feedback["Độ hài lòng"].value_counts(),x_label="Đánh giá",y_label="Số lượng",color=(255,127,80,0.5))


# 
st.write("---")
st.subheader("Tỉ lệ hài lòng")
fig = px.pie(values=feedback["Độ hài lòng"].value_counts(), names=feedback["Độ hài lòng"].unique())
st.plotly_chart(fig)