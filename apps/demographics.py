import streamlit as st
import pandas as pd
import plotly.express as px
import  matplotlib.pyplot as plt
import seaborn as sns

def app():
    st.title("Demographics")
    st.write(""" 
    - Gender
    - Date
    """)    


    @st.cache
    # Load data
    def load_data():
        df = pd.read_csv("main_file_dataset.csv")
        return df
    df = load_data()
    df_gender = df[(df.Author_Identity=="Male")| (df.Author_Identity=="Female")]

    @st.cache
    def load_gender_pie():
        fig = px.pie(df_gender, names='Author_Identity',title="Gender Distribution")
        return fig
    fig = load_gender_pie()
    st.plotly_chart(fig)

    st.header("Time Distribution")
    # select only collection heads, with available year
    df_year = df[~df.Collection_Head.isnull()]
    df_year = df_year[~df_year.Year.isnull()]
    df_year = df_year[~df_year.Start.isnull()]
    #convert to numeric
    df_year.Start = pd.to_numeric(df_year.Start)
    df_year.End = pd.to_numeric(df_year.End)
    # select appropriate dates
    df_year = df_year[df_year.Start<df_year.End]
    df_year = df_year[(df_year.Start>1700) & (df_year.End>1700)]

    fig = plt.figure(figsize=(15,10))
    sns.histplot(df_year["Start"],stat="probability")
    plt.title("Records vs Time")
    plt.xlabel("Year")
    plt.ylabel("Percentage")
    fg = plt.gca()
    fg.set_yticklabels(['{:.0f}%'.format(x*100) for x in plt.gca().get_yticks()])
    st.pyplot(fig)



app()