import streamlit as  st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud, ImageColorGenerator
import re
from num2words import num2words
import gender_guesser.detector as gender
import base64
import streamlit.components.v1 as components
import neattext as nt 
from neattext.functions import clean_text
import streamlit as st



def app():
    st.markdown(""" <style> .font {
    font-size:50px ; font-family: 'Garamond Bold'; color: #005587;} 
    </style> """, unsafe_allow_html=True)
    st.markdown('<p class="font">Card Catalog Data</p>', unsafe_allow_html=True)
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
    #         st.dataframe(selected_df)
    # @st.cache
    # def load_profile():
    #     pr = df.profile_report()
    #     return pr

    # if st.checkbox("Show Pandas Profiling Report on Dataset"):
    #     st.title("Pandas Profiling in Streamlit")
    #     pr = load_profile()
    #     st_profile_report(pr)

    
    # Download Csv option
    def get_table_download_link(df):
        """Generates a link allowing the data in a given panda dataframe to be downloaded
        in:  dataframe
        out: href string
        """
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
        href =  f'<a href="data:file/csv;base64,{b64}" download="main_entry_dataset.csv"> Download the full Dataset file</a>'
        return href

    st.markdown(get_table_download_link(df), unsafe_allow_html=True)
    
    st.write("""
    The original pdf files for all the card entries included in this datasets 
    are uploaded to [Duke Library's Collection in Internet Archive](https://archive.org/details/rubensteinmanuscriptcatalog). They are searchable by text content and metadata.
     """)
    st.header("Topic Modeling")
    st.write("""
    The card catalogues involve several topics. In our attempt to do topic modeling,
    we found that our five topics model  work well to have a general overview of the cards.
    """)
    st.markdown("<h5 style='text-align: center;'>Five - Topics Model</h5>", unsafe_allow_html=True)


    st.image("topic.png")
    # st.markdown("<p style='color: blue;'>Church & Duke</p>" "p""
   
    # "<p style='color: orange;'>Foreign Affairs</p>" unsafe_allow_html=True)
    # "<p style='color: green;'>Domestic Politics</p>", unsafe_allow_html=True)
    # "<p style='color: red;'>Civil war</p>", unsafe_allow_html=True)
    # "<p style='color: purple;'>Business</p>", unsafe_allow_html=True)


    st.markdown("""
    The topics are <font color="blue">Church & Duke</font> , <font color="orange">Foreign Affairs</font>,
    <font color="green">Domestic Politics</font>
    ,
    <font color="red">Civil war </font>
    and 
    <font color="purple">Business </font>in the order of the image above.
    Topic 1 mainly deals with foreign affairs with countries such as  England, Vietnam and India being mentioned. 
    Topic 2 focuses on US politics, congress and presidents.
    On the left bottom with red coloring, we have topic 3 which is talking about the army, civil war, battle.
    This modeling gives us a brief overview of what kind of topics to explore in the dataset. 
    Futher visualizations like word-clouds add insight to the most discussed topics in the card catalogues.
    """,unsafe_allow_html=True)
       # Topic 0 -  Church & Duke   
    # Topic 1 -  Foreign Affairs  
    # Topic 2 -  Domestic Politics   
    # Topic 3  - Civil war  
    # Topic 4  - Business
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
    def wordcd(clean_sent):
            wordcloud = WordCloud(background_color="white", width=3000, height=2000, max_words=100,
            collocations=True,prefer_horizontal=1).generate(clean_sent)
            return wordcloud
    
    st.header("Word Cloud Visualization")
    st.write("These are word-cloud visualizations generated after removing stop-words and common functional words from the dataset")
    # fig= plt.figure(figsize=(15,5))
    # plt.imshow(wordcd(filtered_sentence))
    # plt.title("Word Cloud for full text",pad=20,fontsize=20)
    # plt.axis("off")
    # st.pyplot(fig)
    # plt.savefig("wdcloud-full.png")
    st.image("wdcloud-full.png")

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
        

    col1, col2, col3 = st.columns(3)
    with col1:
        # gen = gen_wdcloud_condition(1700,1800)
        # fig= plt.figure()
        # plt.imshow(gen)
        # plt.title("Word Cloud for {}".format("1700-1800"),pad=20,fontsize=20)
        # plt.axis("off")
        # plt.savefig("wdcld-1.png")
        # st.pyplot(fig)
        st.image("wdcld-1.png")
    with col2:
        # gen = gen_wdcloud_condition(1800,1900)
        # fig= plt.figure()
        # plt.imshow(gen)
        # plt.title("Word Cloud for {}".format("1800-1900"),pad=20,fontsize=20)
        # plt.axis("off")        
        # plt.savefig("wdcld-2.png")
        # st.pyplot(fig)
        st.image("wdcld-2.png")

    with col3:
        # gen = gen_wdcloud_condition(1861,1865)
        # fig= plt.figure()
        # plt.imshow(gen)
        # plt.title("Word Cloud for {}".format("1861-1865 Civil War Period"),pad=20,fontsize=20)
        # plt.axis("off")
        # plt.savefig("wdcld-3.png")
        # st.pyplot(fig)
        st.image("wdcld-3.png",)
    if st.checkbox("See caveats"):
        st.write("""*The three word clouds generated are based on the entries which 
        have dates (and our algorithm was able to pick up).
        *""")

    # Demographics

    st.header("Demographics")
    st.markdown("""\
        These demographics were computed using the Python Gender Guesser package. This analysis helps to evaluate the identities of the people that past librarians deemed important
        enough to catalog the work of. The intention of this analysis is to explore the extent of gender discrepancies in the card catalog to further study the history of 
        the library's treatment of minority groups.

        The authors of collections in the file are typically either a person or an organization. We are evaluating the gender typically associated with only the *people*. The Gender Guesser package classifies genders as one of 6 groups. Male and female result from names that are traditionally associated with one of those genders.
        Mostly male and mostly female result from names that are less cut and dry in regards to the gender they are associated with. Androgynous, means that a name is not traditionally strongly associated with either gender and unknown means that the package was unable to classify a name into any of the other categories. 
        These tended to be non-person organizations or places that would not have a gender and thus were dropped for the visualizations of the results.
        """)
    st.image("gender.png")
    st.markdown("""
    As shown in the above bar chart, the names of the authors present in the library's card collection are overwhelmingly male. This comes as no suprise to anyone who has looked through the cards. Something else of note is the strong presence of binarily gendered names i.e., there are very few "mostly male" or "mostly female" names (and seldom an androgynous one), most are one or the other. Perhaps this
    is indicative of the kinds of names that were given during the time period represented in the cards.
    """)
    
    df_gender = df[(df.Author_Identity=="Male")| (df.Author_Identity=="Female")]

    @st.cache(allow_output_mutation=True)
    def load_gender_pie():
        fig = px.pie(df_gender, names='Author_Identity',title="Gender Distribution")
        return fig
    fig = load_gender_pie()
    fig.update_layout(title_x=0.5)

    st.plotly_chart(fig)
    if st.checkbox("See caveats",key="2"):
        st.write("""*
        For the above pie chart, we combined "mostly male" names with "male" names and "mostly female" names with female names to more easily visualize the gender frequencies. Androgynous names were dropped for the pie chart's sake, due to the fact they compose only about 0.02% of the names. 
        *""")

    st.markdown("""
    The chart shows that about nine out of ten of the collection authors present in the main entry file were, in fact, male. This confirms our specualtions that men were more often than women represented in the catalog. In addition, this supports the theory that the "head of the household," likely the husband, would be elevated to the "author" of collections that entail multiple individuals, possibly hiding the presence of women in the collections. From this we can hypothesize other reasons for the discepency, but further research should be done into the history of archival records at Duke. Further research could also be done into the common events described in the manuscripts cataloged in the files (e.g., were there many Civil War male soldier accounts
     that took presidence over a wife's account of staying home and caring for her children?)
    """)
    st.header("Time Distribution")

    @st.cache
    def load_year_fig():


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
        fg = px.histogram(df_year,x="Start")
        fg.update_layout(title_text="Number of Records vs Time", title_x=0.5)
        return fg
    fg = load_year_fig()
    st.plotly_chart(fg)
    st.markdown("""
    The visualization below shows that most of the card entries are from the 19th century.
    """)

    if st.checkbox("See caveats",key="3"):
        st.write("""*
        For this visualization, only collection head entries are used. The year
        column from the dataset (even after manual cleaning) has human errors. In order to avoid such errors,
        this visualization only takes into account entries which are written after 1700.
        *""")


    # opitional start and end time simultaneous visualization
    # fg = px.histogram(df_year,x=["Start","End"])
    # fg.update_layout(title_text="Number of Records vs Time (Start and End Date)", title_x=0.5)
    # st.plotly_chart(fg)

    st.header("Spatial Distribution")

    st.write("""
    Many of the collections cataloged in the library contain a metadata field of the location of where the items in that collection come from. 
    Using the Python SpaCy package, we attempted to extract these locations. Using those which we could glean from the data, we created spatial heat maps of cards from the United States and North Carolina counties and computed the international card counts using the GeoPandas and matplotlib packages.
    """)
        
    st.subheader("USA Spatial Frequency of Card Catalog Manuscripts")

#     fig = px.choropleth(locations=['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'], locationmode="USA-states", color=[153, 0, 1, 16, 11, 3, 76, 5, 43, 17, 371, 1, 0, 25, 21, 13, 3, 53, 71, 11, 218, 169, 12, 3, 63, 33, 0, 3, 0, 22, 17, 6, 302, 1188, 1, 63, 3, 2, 193, 19, 299, 0, 81, 22, 4, 13, 1631, 5, 48, 3, 1], scope="usa", hover_name=['Alabama','Alaska','Arizona','Arkansas','California','Colorado','Connecticut','Delaware','District of Columbia','Florida','Georgia','Hawaii','Idaho','Illinois','Indiana','Iowa','Kansas','Kentucky','Louisiana','Maine','Maryland','Massachusetts','Michigan','Minnesota','Mississippi','Missouri','Montana','Nebraska','Nevada','New Hampshire','New Jersey','New Mexico','New York','North Carolina','North Dakota','Ohio','Oklahoma','Oregon','Pennsylvania','Rhode Island','South Carolina','South Dakota','Tennessee','Texas','Utah','Vermont','Virginia','Washington','West Virginia','Wisconsin','Wyoming',], color_continuous_scale="YlGnBu", labels={'color':'Count', 'locations':'State Abrev.'})
#     st.plotly_chart(fig,use_container_width=True)

#     st.header("Alternative display")
    lc =['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
    txt =['Alabama','Alaska','Arizona','Arkansas','California','Colorado','Connecticut','Delaware','District of Columbia','Florida','Georgia','Hawaii','Idaho','Illinois','Indiana','Iowa','Kansas','Kentucky','Louisiana','Maine','Maryland','Massachusetts','Michigan','Minnesota','Mississippi','Missouri','Montana','Nebraska','Nevada','New Hampshire','New Jersey','New Mexico','New York','North Carolina','North Dakota','Ohio','Oklahoma','Oregon','Pennsylvania','Rhode Island','South Carolina','South Dakota','Tennessee','Texas','Utah','Vermont','Virginia','Washington','West Virginia','Wisconsin','Wyoming']
    fig = px.choropleth(locations=['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'],
     locationmode="USA-states",
     color=[153, 0, 1, 16, 11, 3, 76, 5, 43, 17, 371, 1, 0, 25, 21, 13, 3, 53, 71, 11, 218, 169, 12, 3, 63, 33, 0, 3, 0, 22, 17, 6, 302, 1188, 1, 63, 3, 2, 193, 19, 299, 0, 81, 22, 4, 13, 1631, 5, 48, 3, 1],
     scope="usa", 
     hover_name=['Alabama','Alaska','Arizona','Arkansas','California','Colorado','Connecticut','Delaware','District of Columbia','Florida','Georgia','Hawaii','Idaho','Illinois','Indiana','Iowa','Kansas','Kentucky','Louisiana','Maine','Maryland','Massachusetts','Michigan','Minnesota','Mississippi','Missouri','Montana','Nebraska','Nevada','New Hampshire','New Jersey','New Mexico','New York','North Carolina','North Dakota','Ohio','Oklahoma','Oregon','Pennsylvania','Rhode Island','South Carolina','South Dakota','Tennessee','Texas','Utah','Vermont','Virginia','Washington','West Virginia','Wisconsin','Wyoming',], 
     color_continuous_scale="YlGnBu", 
     labels={'color':'Count', 'locations':'State Abrev.'})
    fg = go.Figure(data=fig)
    fg.update_layout(     autosize=False,
        margin = dict(
                l=0,
                r=0,
                b=0,
                t=0,
                pad=4,
                autoexpand=True
            ),
            width=1800,
        #     height=400,
        )


    fg.add_scattergeo(locations=lc,    ###codes for states,
    locationmode='USA-states',
    text=lc,
    mode='text')
    fig.update_layout(
    title={
           'xanchor':'center',
           'yanchor':'top',
           'x':0.5})
    st.plotly_chart(fg,use_container_width=True)
    st.write("""
    Based on the heat map, we can see that the states with the most hits are Virginia and North Carolina. New York, South Carolina, and Georgia are also pretty common. Outside of the continental US, Hawaii and Puerto Rico have one hit each.There are some odd outliers here e.g., why is North Carolina not the most represented state? 
    Perhaps NC originating cards were labeled with county instead of state, let's check it out.
    """)
    if st.checkbox("See caveats",key="4"):
        st.write("""*
        While the maps and charts in this notebook may not be entirely accurate to the true contents of the catalog, due to OCR errors compounding through the data pipeline, they serve to give a general idea of the geographic demographics of
            the manuscript collections cataloged in the Rubenstein Library Card Catalog.              
            For the US states heatmap, Washington had around 200 hits; however, it counted the name "Washington," Washington DC, and several counties called Washington incorrectly, so the value of 5 was manually added. Alaska does not have any cards, so it was omitted from the map. 
        *""")

    st.subheader("NC County Spatial Frequency of Card Catalog Manuscripts")
    
    st.image("nc_map.png")
    st.markdown("""
    When we add up all the county collection counts up, we get 551 cards cataloging collections that are specifically from North Carolina counties. 
    There are a lot of cards from Durham County because the Rubenstein Library is located
     in it — as well as Washington County, along with the counties that border Durham. After checking for overlap, most of the cards with a county also have North Carolina or an abbreviation of the state. So, the question still remains around why there are so many more cards from Virginia. According to our word cloud, the civil war is a very common topic in the catalog, and as much of this was fought in Virginia, perhaps that could explain why there are so many cards from the non-NC state.
    """)
        
    st.subheader("International Frequency of Card Catalog Manuscripts")
    st.write("""
    We've seen where the cards in the United States hail from, but what about the rest of the world?
     Let's see how many cards we have from other countries.
    """)
    @st.cache 
    def load_world_map():
        world = pd.read_csv("world.csv")
        fig = px.choropleth(world, locations='iso', color='count', hover_name="hover_name", color_continuous_scale=px.colors.sequential.Plasma)
        return fig 
    fig = load_world_map()
    st.plotly_chart(fig,use_container_width=True)
    st.markdown("### Non-US Countries in the Card Catalog")
    
    colors = ['#C84E00', '#E89923', '#FFD960', '#A1B70D', '#339898', '#993399']
    @st.cache
    def international_pie():
        fig = go.Figure(data=[go.Pie(labels=['Europe', 'Asia', 'North America', 'South America', 'Africa', 'Oceania'], values=[197, 70, 20, 16, 12, 3])])
        fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                  marker=dict(colors=colors, line=dict(color='#000000', width=2)))
        return fig
    fig = international_pie()
    st.plotly_chart(fig,use_container_width=True)
    st.markdown("The above visualizations compare the quantities of international card collection between and within continents. We have cards hailing from every continent, save Antarctica! ")

    # @st.cache()
    # def continent
    europe = {'Austria': 3, 'Belgium': 1, 'Denmark': 4, 'England': 63, 'France': 47, 'Germany': 30, 'Greece': 3, 'Ireland': 5, 
    'Italy': 3, 'Malta': 2, 'Poland': 4, 'San Marino': 1,'Spain': 22, 'Sweden': 2, 'Switzerland': 5, 'Wales': 2}

    asia = {'China': 5, 'India': 25, 'Indonesia': 1, 'Iran': 1, 'Israel': 3, 'Japan': 9, 'Jordan': 13, 'Lebanon': 2,
            'Philippines': 3, 'Syria': 1, 'Thailand': 1, 'Turkey': 3, 'Vietnam': 3}

    north_america = {'Canada': 1, 'Cuba': 4, 'Grenada': 2, 'Guatemala': 1, 'Jamaica': 4, 'Mexico': 8}

    south_america = {'Brazil': 8, 'Chile': 1, 'Colombia': 1, 'Peru': 5, 'Suriname': 1}

    africa = {'Egypt': 3, 'Liberia': 1, 'Madagascar': 1, 'Morocco': 1, 'South Africa': 5, 'Tunisia': 1}

    oceania = {'Australia': 1,'Fiji': 1,'New Zealand': 1}
    def plot(con, i):
        plt.xlabel("Country")
        plt.ylabel("Count")
        plt.xticks(rotation = 45)
        plt.bar(con.keys(), con.values(), color='#00539B')
        plt.title(titles[i])
        return fig
    titles = ["Europe", "Asia", "North America", "South America", "Africa", "Oceania"]
    e,asia_c = st.columns(2)
    n_a,s_a = st.columns(2)
    a, o = st.columns(2)
    with e:
        # fig = plt.figure()
        # plot(europe, 0)
        # fig.savefig("europe.png")
        st.image("europe.png")
    with asia_c:
        # fig = plt.figure()
        # plot(asia, 1)
        # fig.savefig("asia.png")
        st.image("asia.png")
    with n_a:
        # fig = plt.figure()
        # plot(north_america, 2)
        # fig.savefig("north_america.png")
        st.image("north_america.png")
    with s_a:
        # fig = plt.figure()
        # plot(south_america, 3)
        # fig.savefig("south_america.png")
        st.image("south_america.png")
    with a:
        # fig = plt.figure()
        # plot(asia, 4)
        # fig.savefig("africa.png")
        st.image("africa.png")
    with o:
        # fig = plt.figure()
        # plot(asia, 5)
        # fig.savefig("oceania.png")
        st.image("oceania.png")
     







    # st.subheader("Generate Wordcloud")
    # values = st.slider("Choose time range to generate your own word-cloud", min_value=1700,max_value=1950,value=(1700,1800))
    # wd_title = f"{int(values[0])}-{int(values[1])}"
    # fig2= plt.figure(figsize=(15,5))
    # generate = gen_wdcloud_condition(values[0],values[1])
    # plt.imshow(generate)
    # plt.title("Word Cloud for {}".format(wd_title),pad=20,fontsize=20)
    # plt.axis("off")
    # st.pyplot(fig2)
    


    # @st.cache(allow_output_mutation=True)
    # def generate_report(df):
    #     return ProfileReport(df, explorative=True,minimal=True)
    # if st.checkbox('Show Profiling Report on Dataset'):
    #     # output = generate_report(df).to_file('output.html', silent=False)
    #     # st.markdown("output.html",unsafe_allow_html=True)
    #     HtmlFile = open("output.html", 'r', encoding='utf-8')
    #     source_code = HtmlFile.read() 
    #     # print(source_code)
    #     components.iframe("../output.html")


        # st_profile_report(generate_report(df))











    

# app()