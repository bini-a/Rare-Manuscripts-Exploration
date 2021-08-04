
import streamlit as st
from multiapp import MultiApp

from apps import home, data, history, tool


app = MultiApp()

# st.markdown("""
# # Multi-Page App
# The main app running all the other apps
# """)

# Add all your application here
app.add_app("Home", home.app)
# app.add_app("Explore Duke History", history_tool.app)
app.add_app("Data Analysis", data.app)
# app.add_app("Spatial", spatial.app)
# app.add_app("Demographics", demographics.app)
app.add_app("Duke History", history.app)
app.add_app("Filter and Explore Dataset", tool.app)



# The main app
app.run()