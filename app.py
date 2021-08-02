
import streamlit as st
from multiapp import MultiApp

from apps import home,spatial, data, demographics,history,tool # import your app modules here


app = MultiApp()

# st.markdown("""
# # Multi-Page App
# The main app running all the other apps
# """)

# Add all your application here
app.add_app("Home", home.app)
app.add_app("Explore Data", tool.app)
app.add_app("Data", data.app)
app.add_app("Spatial", spatial.app)
app.add_app("Demographics", demographics.app)
app.add_app("History", history.app)


# The main app
app.run()