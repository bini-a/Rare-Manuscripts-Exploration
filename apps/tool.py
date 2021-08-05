import streamlit as st
import pandas as pd
import numpy as np
import neattext as nt 
from neattext.functions import clean_text
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
import re




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
        df_year.Start = pd.to_numeric(df_year.Start,downcast='integer')  
        df_year.End = pd.to_numeric(df_year.End,downcast='integer')
        df_year['End'] = df_year['End'].astype(float).astype('Int64')

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
    # create drawer to page no dict
    x =(list(zip(df_year.Drawer_No,df_year.Page_drawer)))
    dc = {}
    for i in df_year.Drawer_No.unique():
        dc[i]=list()
    for a,b in x:
        dc[a].append(b)

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
            if drawer_no!="All":
                page_no = st.selectbox("Page No",options= np.append(np.array("All"), dc[int(drawer_no)]))
            else:
                page_no = "All"
            return start_date,end_date,author_identity,author,continent,country,drawer_no,page_no

    def generate_data(start_date, end_date,author_identity,author,continent,country,drawer_no,page_no):
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
                ret = ret[ret.Page_drawer.isin(dc[int(drawer_no)])]
            else:
                ret = ret[ret.Page_drawer.isin([int(page_no)])]

        if author =="All":
            author = df_year.Name.unique()
        else:
            author = [author]
        ret = ret[ret.Name.isin(author)]

        columns = df_year.columns.tolist()
        if st.checkbox("Quick Overview: Select the columns to display",False):
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
            first_container_displayed_df = generate_data(s[0],s[1],s[2],s[3],s[4],s[5],s[6],s[7])
            st.dataframe(first_container_displayed_df)
    
            if st.checkbox("Read Full Text Here", False):
                # st.write(first_container_displayed_df[["Name","Text","Link","Drawer_No","Page_drawer"]].to_html(escape = False),
                #  unsafe_allow_html = True)

                st.table(first_container_displayed_df[["Name","Text","Drawer_No","Page_drawer"]])
            # st.write(first_container_displayed_df.to_html(escape = False), unsafe_allow_html = True)

    # GENERATE WORD CLOUD
    wd_cld_container = st.sidebar.beta_expander("Generate Word Cloud ", True)

    @st.cache
    def create_stopwords():
        change_dict = {"variou":"various","thoma":"thomas","thomass":"thomas","united state":"united states","variouss":"various"}

        my_stopword =["haven't", 'it', 'its', 'further', 'can', 'did', "she's", 'such', 've', 'that', 'at', 'where', 'all', 'they', 'don', 'hasn', 're', 'm', 'ours', 'am', 'this', 'needn', 'while', 'again', 'as', 'from', 'once', 'any', 'aren', 'wasn', "shouldn't", 'other', 'be', 'below', 'then', 'very', "couldn't", 'having', 'if', 'herself', 'through', "you'd", 'who', 'had', 'haven', 'after', 'yours', 'whom', 'hers', 'more', "isn't", 'her', "aren't", "don't", "hadn't", 'how', 'his', 'why', 'to', "you've", 'same', 'she', 'themselves', 'an', 'their', 'because', "didn't", 'll', 'd', 'than', "you'll", "you're", 'ain', 'when', 'couldn', 'been', 'there', 'by', 'myself', 'during', 'about', 'both', 'i', 'with', 'just', 'being', 'the', 'ourselves', 'so', 'have', 'we', "shan't", 'me', 'those', 's', 'wouldn', "needn't", 'what', 'itself', "that'll", 'on', 'you', 'between', 'most', 'yourselves', 'off', 'himself', "it's", 'our', 'is', 'no', 'under', "won't", 'over', 'too', 'hadn', 'of', 'were', 'was', 'few', "wouldn't", "mightn't", 'now', "hasn't", 'does', 'doing', 'each', 'own', "should've", 'he', 'above', 'will', "wasn't", 'mightn', 'in', 'not', "mustn't", 'which', 'only', 'your', 'him', 'these', 'against', 'until', 'isn', "doesn't", 't', 'into', 'for', 'mustn', 'some', 'my', 'o', 'doesn', 'ma', 'but', 'has', 'before', 'down', 'theirs', 'out', 'nor', 'or', 'shan', 'up', 'didn', 'a', 'weren', "weren't", 'do', 'them', 'are', 'here', 'and', 'y', 'shouldn', 'yourself', 'won', 'should']
        my_stopword.extend(['i', 'me', 'my', 'myself', 'we', 'our', 'ours', "itemse",'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this',
        'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 
        'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't", 'papers', 'letters', 'items', 'letter', 'collection', 'family', 'co', 'also', 'added', 'see', 'sketch', 'one', 'two', 'ten', 'pp', 'book', 'section', 'ndhyme', 'many', 'item', 'next', 'dec', 'jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'december', 'january', 'febraury', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'vol', 'volume', 'addition', 'sept', 'include', 'included',
        'crd', 'eee', 'card', 'new', 'contain', 'boards', 'cm', 'tion', 'including', 'company', 'vols', 'ing', 'three', 'first', 'papers', 'letters', 'paper', 'letter', 'collection', 'collections', 'items', 'record', 'records', 'contains', 'list', 'letter', 'collection', 'family', 'co', 'also', 'added', 'see', 'sketch', 'one', 'two', 'ten', 'pp', 'book', 'section', 'ndhyme', 'many', 'item', 'next', 'december', 'january', 'febraury', 'march', 'april', 'may', 'report', 'mention', 'concerning', 'several', 
        'guide', 'made', 'june', 'july', 'august', 'september', 'october', 'november', 'vol', 'volume', 'addition', 'sept', 'please', 'ask'])
        return my_stopword,change_dict
    my_stopword,change_dict = create_stopwords()

    @st.cache
    def clean(full):
        # remove punctuation
        full_no_punc = re.sub(r"\.|!", "",full)
        
        # Select only those longer than 1
        full_no_punc = " ".join([i for i in full_no_punc.split() if len(i)>1])

        # Tokenize
        text_tokens = nt.TextFrame(full_no_punc).word_tokens()

        # Change to lower case and select only alphanumeric
        pre_process = [i.lower() for i in text_tokens if i.isalpha()]

        # Remove Stop Words,# remove_single_characters
        token_no_stopword = [word for word in pre_process if word not in my_stopword]
    # 
        filtered_sentence = (" ").join(token_no_stopword)
        return filtered_sentence

    @st.cache
    def get_year_df(df_year):
        df_set_year = df_year.groupby(["Start"])["Text"].apply(" ".join).reset_index()
        df_set_year["Clean"] = df_set_year["Text"].apply(clean)
        return df_set_year
    df_set_year = get_year_df(df_year)
    @st.cache
    def wordcd(clean_sent):
        wordcloud = WordCloud(background_color="white", width=3000, height=2000, max_words=100,
        collocations=True,prefer_horizontal=1).generate(clean_sent)
        return wordcloud
    @st.cache
    def gen_wdcloud_condition(start_date,end_date):
        condition =(df_set_year.Start>=start_date) & (df_set_year.Start<=end_date)
        filt_condition = " ".join(df_set_year[condition].Clean.tolist())
        return wordcd(filt_condition)
    second_exp = st.beta_expander("Generated Word Cloud",True)

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
                gen = gen_wdcloud_condition(1700,1800)
                fig= plt.figure()
                plt.imshow(gen)
                plt.title("Word Cloud for {} - {}".format(start_date,end_date),pad=20,fontsize=20)
                plt.axis("off")
                st.success('Word-Cloud Created!')
                st.pyplot(fig)











    


# app()