import streamlit as st
import pandas as pd
import plotly.express as px
from urllib.request import urlopen
import json

def app():
    st.title("Spatial Info")
    st.write(""" 
    - US states
    - NC states
    - Foreign Countries...
    """)
    
    st.subheader("USA Spatial Frequency of Card Catalog Manuscripts")

    fig = px.choropleth(locations=['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'], locationmode="USA-states", color=[153, 0, 1, 16, 11, 3, 76, 5, 43, 17, 371, 1, 0, 25, 21, 13, 3, 53, 71, 11, 218, 169, 12, 3, 63, 33, 0, 3, 0, 22, 17, 6, 302, 1188, 1, 63, 3, 2, 193, 19, 299, 0, 81, 22, 4, 13, 1631, 5, 48, 3, 1], scope="usa", color_continuous_scale="YlGnBu", labels={'color':'Count'})
    st.plotly_chart(fig,use_container_width=True)
    
    st.subheader("NC County Spatial Frequency of Card Catalog Manuscripts")
    
    st.subheader("International Frequency of Card Catalog Manuscripts")
    
    df = pd.read_csv("world.csv")
    
    fig = px.choropleth(df, locations='iso', color='count', hover_name="hover_name", color_continuous_scale=px.colors.sequential.Plasma)
    st.plotly_chart(fig,use_container_width=True)