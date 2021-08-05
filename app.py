
import streamlit as st
from multiapp import MultiApp

from apps import home, data, history, tool, explore_collections
st.set_page_config(page_title="Rubenstein Library Card Catalog", page_icon="DUL_logo_blue.jpg", layout='centered', initial_sidebar_state='auto')


app = MultiApp()

# st.markdown("""
# # Multi-Page App
# The main app running all the other apps
# """)

# Add all your application here
app.add_app("Home", home.app)
app.add_app("Data Analysis", data.app)
app.add_app("Duke History", history.app)
app.add_app("Filter and Explore", tool.app)
app.add_app("Selected Collections", explore_collections.app)




# The main app
app.run()