import streamlit as  st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas_profiling
from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
import plotly.express as px
# WordCloud 
from wordcloud import WordCloud, ImageColorGenerator
import re
import nltk
from num2words import num2words
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import gender_guesser.detector as gender
import base64
import streamlit.components.v1 as components
# nltk.download('punkt')
def app():
    st.title("Explore Dataset")
    # st.write("""
    # - Dataset
    # - Pandas report on the dataset
    # - Wordclouds
    # - Topics in Card
    # - Option to download csv
    # - Link to IA
    # """)
    "1. Dataset"

    @st.cache
    # Load data
    def load_data():
        df = pd.read_csv("main_file_dataset.csv")
        return df
    df = load_data()
    # Display the dataframe, Select columns to display
    if st.checkbox("Show Dataset"):
        # get the list of columns
        columns = df.columns.tolist()
        st.write("#### Select the columns to display:")
        selected_cols = st.multiselect("",columns,default = columns)
        if len(selected_cols) > 0:
            selected_df = df[selected_cols]
            st.dataframe(selected_df)
    # components.html("apps\report=.html")

    @st.cache
    # generate profile report
    def explore_profile(df):
        pr = ProfileReport(df, explorative=True)
        return pr   
    pr = explore_profile(df)
    # checkbox to select "explore the dataset report based on pandas profiling"
    if st.checkbox('Show Profiling Report on Dataset'):
        st.header('**Pandas Profiling Report**')
        st_profile_report(pr)
    

    # Download Csv option
    def get_table_download_link(df):
        """Generates a link allowing the data in a given panda dataframe to be downloaded
        in:  dataframe
        out: href string
        """
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
        href =  f'<a href="data:file/csv;base64,{b64}" download="myfilename.csv"> Download the full Dataset file</a>'
        return href

    st.markdown(get_table_download_link(df), unsafe_allow_html=True)

    # WordCloud
    stop_words = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this',
     'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 
     'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't", 'papers', 'letters', 'items', 'letter', 'collection', 'family', 'co', 'also', 'added', 'see', 'sketch', 'one', 'two', 'ten', 'pp', 'book', 'section', 'ndhyme', 'many', 'item', 'next', 'dec', 'jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'december', 'january', 'febraury', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'vol', 'volume', 'addition', 'sept', 'include', 'included',
     'crd', 'eee', 'card', 'new', 'contain', 'boards', 'cm', 'tion', 'including', 'company', 'vols', 'ing', 'three', 'first', 'papers', 'letters', 'paper', 'letter', 'collection', 'collections', 'items', 'record', 'records', 'contains', 'list', 'letter', 'collection', 'family', 'co', 'also', 'added', 'see', 'sketch', 'one', 'two', 'ten', 'pp', 'book', 'section', 'ndhyme', 'many', 'item', 'next', 'december', 'january', 'febraury', 'march', 'april', 'may', 'report', 'mention', 'concerning', 'several', 'guide', 'made', 'june', 'july', 'august', 'september', 'october', 'november', 'vol', 'volume', 'addition', 'sept', 'please', 'ask']

    change_dict = {"variou":"various","thoma":"thomas","thomass":"thomas","united state":"united states","variouss":"various"}
    
    @st.cache
    def get_text(df):
        """return clean full text from dataframe"""
        full = " ".join([str(t) for t in df.Text])
        # remove punctuation
        full_no_punc = re.sub(r"\.|!", "",full)
        full_no_punc = " ".join([i for i in full_no_punc.split() if len(i)>2])

        # Tokenize
        text_tokens = word_tokenize(full_no_punc)

        # Change to lower case and select only alphanumeric and tokens longer than two characters
        pre_process = [i.lower() for i in text_tokens if i.isalnum() and len(i)>2]

        # remove_single_characters
        token_no_stopword = [word for word in pre_process if len(word)>2]

        filtered_sentence = (" ").join(token_no_stopword)
        for i in change_dict:
            filtered_sentence =filtered_sentence.replace(i,change_dict[i])
        return filtered_sentence
    filtered_sentence = get_text(df)
    @st.cache
    def wordcd(clean_sent,cfunc = None):
            wordcloud = WordCloud(color_func = cfunc, 
            stopwords=stop_words,background_color="white", width=3000, height=2000, max_words=50,
            collocations=True,prefer_horizontal=1).generate(clean_sent)
            return wordcloud
    
    st.header("Word Cloud Visualization")
    st.write("These are word-cloud visualizations generated after removing stop-words and common functional words from the dataset")
    fig= plt.figure(figsize=(15,5))
    plt.imshow(wordcd(filtered_sentence))
    plt.title("Word Cloud for full text",pad=20,fontsize=20)
    plt.axis("off")
    st.pyplot(fig)
    def clean(full):
        # remove punctuation
        full_no_punc = re.sub(r"\.|!", "",full)
        
        # Select only those longer than 1
        full_no_punc = " ".join([i for i in full_no_punc.split() if len(i)>1])

        # Tokenize
        text_tokens = word_tokenize(full_no_punc)

        # Change to lower case and select only alphanumeric
        pre_process = [i.lower() for i in text_tokens if i.isalpha()]

        # Remove Stop Words,# remove_single_characters
        token_no_stopword = [word for word in pre_process if word not in stop_words]
    # 
        filtered_sentence = (" ").join(token_no_stopword)
        return filtered_sentence

    @st.cache
    def get_year_df(df):
        # Start date precedes end date
        df_year = df[df.Start<df.End]
        # Select records with start year of 1700
        df_year = df_year[(df_year.Start>1700) & (df_year.End>1700) ]
        # New dataframe with cleaned column
        df_set_year = df_year.groupby(["Start"])["Text"].apply(" ".join).reset_index()
        df_set_year["Clean"] = df_set_year["Text"].apply(clean)
        return df_set_year
    df_set_year = get_year_df(df)
    
    @st.cache(allow_output_mutation=True)
    def gen_wdcloud_condition(start_date,end_date):
        condition =(df_set_year.Start>=start_date) & (df_set_year.Start<=end_date)
        filt_condition = " ".join(df_set_year[condition].Clean.tolist())
        return wordcd(filt_condition)
        

    col1, col2, col3 = st.beta_columns(3)
    with col1:
        gen = gen_wdcloud_condition(1700,1800)
        fig= plt.figure()
        plt.imshow(gen)
        plt.title("Word Cloud for {}".format("1700-1800"),pad=20,fontsize=20)
        plt.axis("off")
        st.pyplot(fig)
    with col2:
        gen = gen_wdcloud_condition(1800,1900)
        fig= plt.figure()
        plt.imshow(gen)
        plt.title("Word Cloud for {}".format("1800-1900"),pad=20,fontsize=20)
        plt.axis("off")
        st.pyplot(fig)
    with col3:
        gen = gen_wdcloud_condition(1861,1865)
        fig= plt.figure()
        plt.imshow(gen)
        plt.title("Word Cloud for {}".format("1861-1865 Civil War Period"),pad=20,fontsize=20)
        plt.axis("off")
        st.pyplot(fig)

    st.subheader("Generate Wordcloud")
    values = st.slider("Choose time range to generate your own word-cloud", min_value=1700,max_value=1950,value=(1700,1800))
    wd_title = f"{int(values[0])}-{int(values[1])}"
    fig2= plt.figure(figsize=(15,5))
    generate = gen_wdcloud_condition(values[0],values[1])
    plt.imshow(generate)
    plt.title("Word Cloud for {}".format(wd_title),pad=20,fontsize=20)
    plt.axis("off")
    st.pyplot(fig2)


    st.header("Internet Archive")
    st.write("""
    The image files for all the card entries are uploaded to Internet Archive. It can be searched by text contents...
     """)
    st.write("Follow this link to Internet archive [link](https://archive.org/details/rubensteinmanuscriptcatalog)")
    st.header("Topic Modeling")
    st.write("""
    After trying multiple models, we found a five topic model which works well. As you can see this is five topic model: 
    Topic 0 -  Church & Duke,
    Topic 1 -  Foreign Affairs,
    Topic 2 -  Domestic Politics,
    Topic 3  - Civil war,
    Topic 4  - Business.

    On the left bottom with red coloring, we have topic 3 which is talking about the army, civil war, battle.
    Topic 1 is about foreign affairs with England, Vietnam and India being mentioned. 
    Topic 2 is about us politics, congress and presidents. This modeling gives a brief overview of what kind of topics to explore 
    in the dataset.
    """)

    st.image("topic.png")










    

app()