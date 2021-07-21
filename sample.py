import streamlit as  st
import pandas as pd

st.title("Rubenstien Library Catalog")
df = pd.read_csv("https://github.com/bini-a/Data--Rubenstein-Library-Card-Catalog/blob/main/all_sorted_collection.csv")
print(df.head())