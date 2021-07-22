import streamlit as  st
import pandas as pd
import numpy
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report

pd.set_option('display.max_colwidth', None)
pd.set_option("display.max_row", None)


# st.set_option('deprecation.showPyplotGlobalUse', False)
st.title("Rubenstein Library Catalog")

@st.cache  # 👈 Added this
def myfunc():
    df = pd.read_csv("all_sorted_collection.csv")
    return df
df = myfunc()
st.write(df)

@st.cache
def explore_profile(df):
    pr = ProfileReport(df, explorative=True)
    return pr
if st.button('Explore the dataset'):
    pr = explore_profile(df)
    st.header('**Pandas Profiling Report**')
    st_profile_report(pr)


st.title("Visualizations")
df_year = df[((df.End>=1512))|((df.Start<1512 )& (df.End<1512))]
df_year=df_year[df_year.Start>1700]
# st.line_chart(df)
fig1= plt.figure(1,figsize=(15,5))
@st.cache
def hist_vis(fig):
    sns.histplot(df_year["Start"],stat="probability")
    plt.title("Records vs Time")
    plt.xlabel("Year")
    plt.ylabel("Percentage")
    plt.gca().set_yticklabels(['{:.0f}%'.format(x*100) for x in plt.gca().get_yticks()]);
    
hist_vis(fig1)
st.pyplot(fig1)

import plotly.express as px
fig3= px.histogram(df_year, x="Start",width=800, height = 400,histnorm='percent',nbins=36)
# fig3.layout.yaxis.tickformat = ',.0%'

st.plotly_chart(fig3)



fig2= plt.figure(2,figsize=(15,5))



# WordCloud 
from wordcloud import WordCloud, ImageColorGenerator
import re
from num2words import num2words
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
def black_color_func(word, font_size, position,orientation,random_state=None, **kwargs):
    return("hsl(0,100%, 1%)")
stop_words = stopwords.words('english')
stop_words.extend(['dec', 'jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov',"include","included","crd","eee","card","new","contain",
"boards","cm","tion","including","company","vols","ing","three","first","papers","letters","paper","letter","collection","collections",
"items","record","records","contains","list","letter","collection","family","co","also","added","see","sketch","one","two","ten", "pp","book","section","ndhyme","many","item","next",
"december","january","febraury","march","april","may","report","mention","concerning","several","guide","made","june","july","august","september","october","november","vol","volume","addition","sept","please","ask"])
change_dict = {"variou":"various","thoma":"thomas","thomass":"thomas","united state":"united states"}

@st.cache
def filtered_sentence():
    full = " ".join([str(t) for t in df.Text])
    # remove punctuation
    full_no_punc = re.sub(r"\.|!", "",full)
    full_no_punc = " ".join([i for i in full_no_punc.split() if len(i)>2])

    # Tokenize
    text_tokens = word_tokenize(full_no_punc)

    # # Change to lower case and select only alphanumeric
    pre_process = [i.lower() for i in text_tokens if i.isalnum() and len(i)>2]

    # Remove Stop Words,# remove_single_characters
    token_no_stopword = [word for word in pre_process if word not in stop_words and len(word)>2]


    filtered_sentence = (" ").join(token_no_stopword)

    for i in change_dict:
        filtered_sentence =filtered_sentence.replace(i,change_dict[i])
    return filtered_sentence

@st.cache()
def wordcd(fig,cfunc = None):
            wordcloud = WordCloud(color_func = cfunc, 
            stopwords=stop_words,background_color="white", width=3000, height=2000, max_words=50,
            collocations=True,prefer_horizontal=1).generate(filtered_sentence())
            plt.imshow(wordcloud)
            plt.title("Word Cloud for full text",pad=20,fontsize=20)
            plt.axis("off")

wordcd(fig2)
st.pyplot(fig2)


import gender_guesser.detector as gender

st.title("Gender Distribution | Distribution over time")
st.title("Spatial Disribution")
st.title("Topics ")
st.subheader("Duke University/Presidents")
st.subheader("Race Related Collections")
st.subheader("Civil War")
st.subheader("Main Events")
st.write("Wilmington race riot, Charleston Earthquake")
st.subheader("Collections with outdated language")







