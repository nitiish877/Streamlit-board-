import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sea
import numpy as np
df=pd.read_json("student_sessional_dataset.json")

df["status"]=np.where(df["marks"]>=76,"pass","fail")
df["result_date"]=pd.to_datetime(df["result_date"])
df["month"]=df["result_date"].dt.month_name()
fig,ax=plt.subplots()
st.header("Student Analysis")
select=st.selectbox("Filter",["Student","Branch","Subject","Exam Trend","Top Student","Weak Student"])
if select=="Branch":
    button=st.radio("Performance:",["Branch vs marks","Branch vs Pass rate"])
    if button=="Branch vs marks":
        sea.barplot(data=df,x=df["branch"],y=df["marks"])
        plt.title("Branch vs marks")
        st.pyplot(plt)

    elif button=="Branch vs Pass rate":
        a=df.groupby("branch")["status"].value_counts(normalize=True)*100
        a=a.unstack().plot(kind="bar")
        plt.title("Branch vs Pass rate")
        plt.xlabel("Branch")
        plt.ylabel("Pass Rate")
        st.pyplot(plt)

elif select=="Subject":
    button=st.radio("Performance",["Subject vs Marks","Subject vs Pass rate"])
    if button=="Subject vs Marks":
        sea.barplot(data=df,x=df["subject"],y=df["marks"])
        plt.xticks(rotation=78)
        st.pyplot(plt)

    elif button=="Subject vs Pass rate" :
        a=df.groupby("subject")["status"].value_counts(normalize=True)*100
        a=a.unstack().plot(kind="bar")
        plt.title("Subject vs Pass rate")
        plt.xlabel("Subject")
        plt.ylabel("Pass Rate")
        st.pyplot(plt)

elif select=="Exam Trend":
    button=st.radio("Exam Trend",["Sessional Exam Trend","Exam vs Marks"])
    if button=="Sessional Exam Trend":
        sea.lineplot(data=df,x=df["sessional_exam"],y=df["marks"])
        plt.title("Exam Trend")
        st.pyplot(plt)

    elif button=="Exam vs Marks":
        sea.barplot(data=df,x=df["month"],y=df["marks"],color="#7c5fd4")    
        plt.title("Exam vs Marks")
        st.pyplot(plt)

elif select=="Top Student":
    st.write("Top Student")
    n=st.number_input("How much student:",step=1)
    if n:
        top=(df.groupby(["roll_no","student_name","branch"])["marks"].
             mean().
             sort_values(ascending=False))
        st.write(top.head(n)) 

        if st.button("Graph"):
            top.head(n).plot(kind="bar")
            plt.title("Top Student")
            plt.xlabel("Student")
            plt.ylabel("Marks")
            st.pyplot(plt)

elif select=="Weak Student":
    n=st.number_input("How much student:",step=1)
    if n:
        top=(df.groupby(["roll_no","student_name","branch"])["marks"].
             mean().
             sort_values(ascending=True))
        st.write(top.head(n)) 

        if st.button("Graph"):
            top.head(n).plot(kind="bar")
            plt.title("Weak Student")
            plt.xlabel("Student")
            plt.ylabel("Marks")
            st.pyplot(plt)

elif select=="Student":
    roll=st.text_input("Roll no.:")
    if roll:
        a=df[df["roll_no"]==int(roll)]
        a.drop(columns=["status","month"],inplace=True)
        st.write(a)

plt.tight_layout()
