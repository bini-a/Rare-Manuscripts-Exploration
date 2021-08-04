import streamlit as st
import pandas as pd
import numpy as np


def app():
    @st.cache
    # Load data
    def load_data():
        df = pd.read_csv("main_file_dataset.csv")
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
        df_year["Country"] = df_year.Country.fillna("Unknown")
        df_year["Continent"] = df_year.Continent.fillna("Unknown")
        

        # create country to continent dictionary
        continent_list = df_year.Continent.unique()
        dic = {}
        for i in continent_list:
            dic[i] = set()
        for ind,row in df_year.iterrows():
            dic[row.Continent].add(row.Country)
        return df,df_year,dic
    files =  load_data()
    df =files[0]
    df_year = files[1]
    dic = files[2]

    def dataset_selector():
        dataset_container = st.sidebar.beta_expander(" Configure and Explore Dataset ", True)

        with dataset_container:
            st.header("Configure the Dataset for Exploration")
            if st.checkbox("See Caveats"):
                st.info("""Configuring the dataset selects rows with available date and text. While using this tool, only the rows which are collection headers (according to 
            our algorithm) and have existing date are used.
            """)
            values = st.slider("Choose time range", min_value=1700,max_value=1950,value=(1700,1950))
            start_date,end_date = values[0],values[1]
            author_identity = st.multiselect("Select Author Identity",options = (df_year.Author_Identity.unique()),
            default =df_year.Author_Identity.unique())
            author = st.selectbox("Select Author",options = np.append(np.array("All"),sorted(df_year.Name.unique())))
            continent = st.selectbox("Select Continent",options = np.append(np.array("All"),sorted(df_year.Continent.unique())))
            if continent!="All":
                country = st.selectbox("Select Country",np.append(np.array("All"),sorted(dic[continent])))
            else:
                country = "All"
            drawer_no = st.selectbox("Drawer No",options =np.append(np.array("All"), np.arange(157,232)))
            return start_date,end_date,author_identity,author,continent,country,drawer_no

    def generate_data(start_date, end_date,author_identity,author,continent,country,drawer_no):
        time_condition =(df_year.Start>=start_date) & (df_year.Start<=end_date)

        ret = df_year[time_condition]
        ret = ret[ret.Author_Identity.isin(author_identity)]

        if continent == "All":
            continent = df_year.Continent.unique()
        else:
            continent = [continent]
        ret = ret[ret.Continent.isin(continent)]

        if country == "All":
            country = df_year.Country.unique()
        else:
            country = [country]
        ret = ret[ret.Country.isin(country)]
  
        if drawer_no == "All":
            drawer_no = df_year.Drawer_No.unique()
        else:
            drawer_no = [int(drawer_no)]
        ret = ret[ret.Drawer_No.isin(drawer_no)]

        if author =="All":
            author = df_year.Name.unique()
        else:
            author = [author]
        ret = ret[ret.Name.isin(author)]

        columns = df_year.columns.tolist()
        if st.checkbox(" Select the columns to display:",False):
    
            columns_to_show = st.multiselect("",columns,default = columns)
            if len(columns_to_show) > 0:
                selected_df = ret[columns_to_show]
                return selected_df    
        return ret

    s = dataset_selector()
    first_exp= st.beta_expander("Explore Dataset",True)
    with first_exp:

        container1 = st.beta_container()
        with container1:
            first_container_displayed_df = generate_data(s[0],s[1],s[2],s[3],s[4],s[5],s[6])
            st.dataframe(first_container_displayed_df)


     










    


# app()