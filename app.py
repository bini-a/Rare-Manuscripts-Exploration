
import streamlit as st
from multiapp import MultiApp
from pathlib import Path
from apps import home, analysis, history, explore_tool, explore_collections
# loc = Path(__file__).parents[1] / 'rlapp/data/img/DUL_logo_blue.jpg'
# st.write(loc)
# home_dir = Path(__file__).parents[1] 
st.set_page_config(page_title="Rubenstein Library Card Catalog", page_icon= "data/img/DUL_logo_blue.jpg",
                   layout='wide', initial_sidebar_state='auto')


app = MultiApp()
# home_dir = Path(__file__).parents[1] / 'data/main_data.csv'


# app.add_app("Home", home.app)
app.add_app("Filter and Explore", explore_tool.app)
# app.add_app("Selected Collections", explore_collections.app)
app.add_app("Data Analysis", analysis.app)
# app.add_app("Duke History", history.app)

# The main app
app.run()
