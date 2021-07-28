import streamlit as  st
import pandas as pd
import numpy
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
import plotly.express as px
# WordCloud 
from wordcloud import WordCloud, ImageColorGenerator
import re
from num2words import num2words
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import gender_guesser.detector as gender
import os

def app():
    st.title("Explore Dataset")
    st.write("""
    - Dataset
    - Pandas report on the dataset
    - Wordclouds
    - Topics in Card
    - Option to download csv
    - Link to IA
    """)
    "1-Dataset"
    @st.cache
    # Load data
    def load_data():
        df = pd.read_csv("all_sorted_collection.csv")
        return df
    df = load_data().head()
    # Display the dataframe
        # Select columns to display
    if st.checkbox("Show dataset with selected columns"):
        # get the list of columns
        columns = df.columns.tolist()
        st.write("#### Select the columns to display:")
        selected_cols = st.multiselect("",columns,default = columns)
        if len(selected_cols) > 0:
            selected_df = df[selected_cols]
            st.dataframe(selected_df)


    @st.cache
    # generate profile report
    def explore_profile(df):
        pr = ProfileReport(df, explorative=True)
        return pr

    # checkbox to select "explore the dataset report based on pandas profiling"
    if st.checkbox('Explore the dataset'):
        st.header('**Pandas Profiling Report**')
        st_profile_report(explore_profile(df))

    #TODO
    



# app()