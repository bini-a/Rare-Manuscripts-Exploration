
import streamlit as st
from multiapp import MultiApp

from apps import home, analysis, history, explore_tool, explore_collections
st.set_page_config(page_title="Rubenstein Library Card Catalog", page_icon="data\img\DUL_logo_blue.jpg",
                   layout='wide', initial_sidebar_state='auto')


app = MultiApp()


app.add_app("Home", home.app)
app.add_app("Filter and Explore", explore_tool.app)
app.add_app("Selected Collections", explore_collections.app)
app.add_app("Data Analysis", analysis.app)
app.add_app("Duke History", history.app)

# The main app
app.run()
