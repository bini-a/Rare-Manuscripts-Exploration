import streamlit as st
import pandas as pd
import numpy as np

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
    dataset_container = st.sidebar.beta_expander("# Configure a dataset", True)
    with dataset_container:
        values = st.slider("Choose time range", min_value=1700,max_value=1950,value=(1700,1950))
        start_date,end_date = values[0],values[1]
        author_identity = st.multiselect("Select Author Identity",options = df_year.Author_Identity.unique(),
        default =df_year.Author_Identity.unique())
        continent = st.selectbox("Select Continent",options = np.append(np.array("All"),df_year.Continent.unique()))
        country = st.selectbox("Select Country",options = np.append(np.array("All"),df_year.Country.unique()))

        return start_date,end_date,author_identity,country,continent

def generate_data(start_date, end_date,author_identity,country,continent):
    time_condition =(df_year.Start>=start_date) & (df_year.Start<=end_date)

    ret = df_year[time_condition]
    ret = ret[ret.Author_Identity.isin(author_identity)]
    if continent == "All":
        continent = df_year.Continent.unique()
    else:
        continent = [continent]
    if country == "All":
        country = df.Country.unique()
    else:
        country = [country]
    ret = ret[ret.Continent.isin(continent)]
    ret = ret[ret.Country.isin(country)]
    return ret

s = dataset_selector()
df = generate_data(s[0],s[1],s[2],s[3],s[4])
st.dataframe(df)




        # n_samples = st.number_input(
        #     "Number of samples",
        #     min_value=50,
        #     max_value=1000,
        #     step=10,
        #     value=300,
        # )

        # train_noise = st.slider(
        #     "Set the noise (train data)",
        #     min_value=0.01,
        #     max_value=0.2,
        #     step=0.005,
        #     value=0.06,
        # )
        # test_noise = st.slider(
        #     "Set the noise (test data)",
        #     min_value=0.01,
        #     max_value=1.0,
        #     step=0.005,
        #     value=train_noise,
        # )

        # if dataset == "blobs":
        #     n_classes = st.number_input("centers", 2, 5, 2, 1)
        # else:
        #     n_classes = None