import streamlit as st
import pandas as pd
import os


st.set_page_config(page_title="Product Feedback", page_icon="📝", initial_sidebar_state="expanded")
st.title("🍲 PhoLM Feedback")


st.subheader("Leave Your Feedback")


rating = st.radio("Rating:", [5, 4, 3, 2, 1], index=0, format_func=lambda x: f"{x} 🍲", horizontal=True)
name = st.text_input("Tên:")
email = st.text_input("Email:")
comment = st.text_area("Feedback:")
submit_button = st.button("Submit")


csv_file = "./db/feedback.csv"


def append_feedback_to_csv(data, file_path):
    
    if not os.path.isfile(file_path):
        
        pd.DataFrame(data).to_csv(file_path, index=False, mode='a', header=True)
    else:
        
        pd.DataFrame(data).to_csv(file_path, index=False, mode='a', header=False)


if submit_button:
    
    feedback_data = {
        "Tên": [name],
        "Email": [email],
        "Nhận xét": [comment],
        "Độ hài lòng": [rating]
    }

    
    feedback_df = pd.DataFrame(feedback_data)

    
    append_feedback_to_csv(feedback_data, csv_file)

    
    st.success("Thank you for your feedback!")

    
    st.write("### Feedback received:")
    st.dataframe(feedback_df)
