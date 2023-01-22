import streamlit as st
import pandas as pd
import numpy as np
import neattext as nt 
from neattext.functions import clean_text
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
import re
import pickle
        
def app():
    if st.checkbox("How to use the tools"):
        st.write("""
        *Configure and Explore Dataset*: Use the widget on the left side of the page to filter the dataset by year, author, author identity, continent, and/or drawer number. You can also click the Quick Overview checkbox to choose which rows of the dataset you wish to see. If you want to see the full text of your selected cards, click the Read Full Text Here checkbox under the displayed dataset.
        
        *Generate Wordcloud*: Scroll down on the left side of the page to select a range of years to generate a wordcloud of common words in the related cards.
        """)
    
    @st.cache
    # Load data
    def load_data():
        # load main dataset
        df = pd.read_csv("data\main_data.csv")
        # select only collection heads, with available year
        df_year = pd.read_csv("data\data_year_avail.csv")
        # data cleaned and grouped by start year
        df_grouped = pd.read_csv("data\df_clean_grouped.csv")
        # Continent to country dictionary
        # Drawer to page number dictionary
        with open('data\continent_country.pkl', 'rb') as f:
            continent_country = pickle.load(f)
        with open('data\drawer_dict.pkl', 'rb') as f:
            drawer_dict = pickle.load(f)
        return df, df_year, df_grouped, continent_country, drawer_dict 
    df, df_year,df_grouped, continent_country, drawer_dict = load_data()

    def dataset_selector():
        dataset_container = st.sidebar.expander(" Configure and Explore Dataset ", True)
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
                country = st.selectbox("Select Country",np.append(np.array("All"),sorted(continent_country[continent])))
            else:
                country = "All"
            drawer_no = st.selectbox("Drawer No",options =np.append(np.array("All"), np.arange(157,232)))
            if drawer_no!="All":
                page_no = st.selectbox("Page No",options= np.append(np.array("All"), drawer_dict[int(drawer_no)]))
            else:
                page_no = "All"
            return start_date,end_date,author_identity,author,continent,country,drawer_no,page_no

    def generate_data(select_list):
        start_date, end_date,author_identity,author,continent,country,drawer_no,page_no = select_list
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
            ret = ret[ret.Drawer_No.isin(df_year.Drawer_No.unique())]
        else:
            ret = ret[ret.Drawer_No.isin([int(drawer_no)])]
        if drawer_no!="All":
            if page_no=="All":
                ret = ret[ret.Page_drawer.isin(drawer_dict[int(drawer_no)])]
            else:
                ret = ret[ret.Page_drawer.isin([int(page_no)])]

        if author =="All":
            author = df_year.Name.unique()
        else:
            author = [author]
        ret = ret[ret.Name.isin(author)]

        columns = df_year.columns.tolist()
        if st.checkbox("Quick Overview: Select the columns to display",True):
            columns_to_show = st.multiselect("",columns,default = columns)
            if len(columns_to_show) > 0:
                selected_df = ret[columns_to_show]
                return selected_df    
        return ret

    selector = dataset_selector()
    first_exp= st.expander("Explore Dataset",True)
    with first_exp:
        container1 = st.container()
        with container1:
            first_container_displayed_df = generate_data(selector)
            st.dataframe(first_container_displayed_df)
    
            if st.checkbox("Read Full Text Here", False):                
                st.table(first_container_displayed_df[["Name","Text", "Drawer_No","Page_drawer"]])

    # GENERATE WORD CLOUD
    wd_cld_container = st.sidebar.expander("Generate Word Cloud ", True)
    @st.cache
    def generate_wdcloud(start_date,end_date):
        condition =(df_grouped.Start>=start_date) & (df_grouped.Start<=end_date)
        clean_text = " ".join(df_grouped[condition].Clean.tolist())
        wordcloud = WordCloud(background_color="white", width=3000, height=2000, max_words=100,
        collocations=True,prefer_horizontal=1).generate(clean_text)
        return wordcloud

    second_exp = st.expander("Generated Word Cloud",True)

    with wd_cld_container:
        st.header("Choose Time Range and generate your own Word Cloud")
        if st.checkbox("See Caveats",key="2"):
            st.info("""Configuring the dataset selects rows with available date and text. While using this tool, only the rows which are collection headers (according to 
        our algorithm) and have existing date are used.
        """)
        values = st.slider("Choose time range", min_value=1700,max_value=1950,value=(1700,1950),key="3",)   

        if st.button("Generate"):
            start_date,end_date = values[0],values[1]
            with second_exp:
                gen = generate_wdcloud(start_date,end_date)
                fig= plt.figure()
                plt.imshow(gen)
                plt.title("Word Cloud for {} - {}".format(start_date,end_date),pad=20,fontsize=20)
                plt.axis("off")
                st.success('Word-Cloud Created!')
                st.pyplot(fig)











    


# app()