import streamlit as st
import pandas as pd
import numpy as np
import pickle
def app():
    @st.cache
    # Load data
    def load_data():
        # load main data
        df = pd.read_csv("data\main_data.csv")
        # load collection info data
        with open('data\collection_dict.pkl', 'rb') as f:
            collection = pickle.load(f)
        return df, collection
    df , collection = load_data()


    def get_df_key_index(key, dic):
        if key == "All":
            return df.iloc[sum(dic.values(), [])]
        ind = dic[key]
        return df.iloc[ind, :]

    def dataset_selector():
        dataset_container = st.sidebar.expander(
            """Explore Collections Related to Duke's History & Notable Events""", True)
        choice = ["Duke University Presidents",
                  "Duke University Early Names", "Duke Buildings", "Charleston Earthquake", "Wilmington Race Riot of 1898", "Civil War"]
        with dataset_container:
            check = st.radio("Explore", choice)
            if check == choice[0]:
                duke_pres = st.selectbox("Select Duke University President ", np.append(
                    np.array("All"), sorted(list(collection["president_indices"].keys()))))
                return duke_pres, 0
            elif check == choice[1]:
                duke_uni = st.selectbox("Select Duke University's Early Names ",
                                        np.append(np.array("All"), sorted(list(collection["name_indices"].keys()))))
                return duke_uni, 1
            elif check == choice[2]:
                build = st.selectbox("Select Duke University's Building Name ",
                                     np.append(np.array("All"), sorted(list(collection["buildings"].keys()))))
                return build, 2

            elif check == choice[2]:
                return None, "Charleston"
            elif check == choice[3]:
                return None, "Wilmington"
            return None, "Civil War"

    def generate_data(selected_identity, explore_topic):
        if (explore_topic == 0):
            exp_df = get_df_key_index(selected_identity, collection["president_indices"])
        elif (explore_topic == 1):
            exp_df = get_df_key_index(selected_identity,collection["name_indices"])
        elif (explore_topic == 2):
            exp_df = get_df_key_index(selected_identity, collection["buildings"])
        elif explore_topic == "Charleston":
            return df.iloc[collection["charleston"], :]
        elif explore_topic == "Wilmington":
            return df.iloc[collection["wilmington"], :]
        elif explore_topic == "Civil War":
            return df.iloc[collection["civil_war"], :]
        return exp_df

    def short_link(df):
        def make_clickable(url, text):
            return f'<a target="_blank" href="{url}">{text}</a>'
        df = df[["Name", "Text", "Link", "Drawer_No", "Page_drawer"]]
        df["Link"] = df["Link"].apply(make_clickable, args=('Link',))
        df.rename(columns={"Drawer_No": "Drawer",
                  "Page_drawer": "Page"}, inplace=True)
        return df

    selected_identity, explore_topic = dataset_selector()

    second_exp = st.expander("Explore Selected Colletions", True)
    with second_exp:
        container2 = st.container()
        with container2:
            second_container_displayed_df = generate_data(
                selected_identity, explore_topic)
            second_container_displayed_df = short_link(
                second_container_displayed_df)
            st.write(second_container_displayed_df.to_html(
                escape=False), unsafe_allow_html=True)