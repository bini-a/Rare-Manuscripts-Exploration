import streamlit as st
import pandas as pd
import numpy as np

def app():
    @st.cache
    # Load data
    def load_data():
        df = pd.read_csv("main_file_dataset.csv")
        return df
    df = load_data()

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

    def dataset_selector():
        dataset_container = st.sidebar.beta_expander("""Configure a dataset""", True,)
        with dataset_container:
            values = st.slider("Choose time range", min_value=1700,max_value=1950,value=(1700,1950))
            start_date,end_date = values[0],values[1]
            author_identity = st.multiselect("Select Author Identity",options = df_year.Author_Identity.unique(),
            default =df_year.Author_Identity.unique())
            continent = st.selectbox("Select Continent",options = np.append(np.array("All"),df_year.Continent.unique()))
            country = st.selectbox("Select Country",options = np.append(np.array("All"),df_year.Country.unique()))
            drawer_no = st.selectbox("Drawer No",options =np.append(np.array("All"), np.arange(157,232)))

            return start_date,end_date,author_identity,country,continent,drawer_no
    # TODO country list for each continent
    def generate_data(start_date, end_date,author_identity,country,continent,drawer_no):
        time_condition =(df_year.Start>=start_date) & (df_year.Start<=end_date)

        ret = df_year[time_condition]
        ret = ret[ret.Author_Identity.isin(author_identity)]
        if continent == "All":
            continent = df_year.Continent.unique()
        else:
            continent = [continent]
        if country == "All":
            country = df_year.Country.unique()
        else:
            country = [country]
        if drawer_no == "All":
            drawer_no = df_year.Drawer_No.unique()
        else:
            drawer_no = [int(drawer_no)]
        ret = ret[ret.Continent.isin(continent)]
        ret = ret[ret.Country.isin(country)]
        ret = ret[ret.Drawer_No.isin(drawer_no)]
    
        return ret

    s = dataset_selector()
    df = generate_data(s[0],s[1],s[2],s[3],s[4],s[5])
    st.dataframe(df)
    def history_explorer():
        dataset_container = st.sidebar.beta_expander("""Explore Collections Related to Duke's History""", True,)
        with dataset_container:
            duke_pres = st.selectbox("Select Duke University President ", ["President 1","President 2"])
            duke_uni = st.multiselect("Select Duke University's Early Names ", ["Name 1","Name 2"])
            duke_buil = st.multiselect("Select Duke University's Buildings in the collection ", ["Bldg 1","Bldg 2"])
        return duke_pres
    if st.checkbox("Explore Duke History (To be Finished)"):
        duke_pre = history_explorer()
        dis = st.beta_container()
        with dis:
            st.write("Display the Duke History Dataframe here")
            st.write(df_year.head())
            if duke_pre=="President 1":
                st.write("You chose Presiden 1")
            elif duke_pre=="President 2":
                st.write("You chose President 2")
