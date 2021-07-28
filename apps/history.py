import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re
from scipy import stats
import operator

def app():
    st.title("History")
    st.subheader("History of Duke Presidents in the Catalog")
    
    #---------------------------------------------------------------------------------------------------------------------------------------
    # Print graph of counts per presidential name
    last = ["York", "Craven", "Gannaway", "Wood", "Crowell", "Kilgo", "Few", "Flowers", "Edens", "Hart", "Knight", "Sanford", "Brodie", "Keohane", "Brodhead"]
    name_counts = [4, 36, 5, 5, 5, 10, 34, 15, 0, 1, 4, 17, 0, 0, 3]

    # Disply bar chart of first and last name occurances
    fig, ax = plt.subplots()
    plt.bar(last, name_counts, color='#00539B')
    plt.xticks(rotation = 45)
    plt.title("Occurances of Duke Presidental Names in the Card Catalog")
    plt.xlabel("Name")
    plt.ylabel("# of Cards")
    plt.show()
    st.pyplot(fig)
    
    st.write("""Here we have a graph of the frequencies of each president's name in the catalog. Let's look at what these cards have to say about the Duke presidents.""")
    
    #---------------------------------------------------------------------------------------------------------------------------------------
    
    st.write("""   
    Presidents Brodie, Keohane, and Edens were not mentioned in the card catalog. Hart did not have any relevant mentions
    
    On two cards, a Richard Brodhead is mentioned, but not the one who was president of Duke. Upon further inspection, this man was a [U.S. Democratic Senator from Pennsylvania](https://en.wikipedia.org/wiki/Richard_Brodhead). The cards upon which he is mentioned can be viewed [here](https://archive.org/details/rubensteinmanuscriptcatalog_P_to_Peo/page/44/mode/2up) and [here](https://archive.org/details/rubensteinmanuscriptcatalog_Pep_to_Pn/page/n393/mode/2up).

    President Douglas Knight is mentioned as having [correspondence with Herbert Clarence Bradshaw](https://archive.org/details/rubensteinmanuscriptcatalog_R._Boyd_to_I._Brown/page/n125/mode/2up), being the recipient of a [letter from a Mr. Matton](https://archive.org/details/rubensteinmanuscriptcatalog_Mani_to_Maw/page/3/mode/2up) and [letters from William Murray Werber](https://archive.org/details/rubensteinmanuscriptcatalog_Ware_to_H._White/page/n567/mode/2up). The first two mention religion and all involve letters.

    For President York, one [card](https://archive.org/details/rubensteinmanuscriptcatalog_X_to_Z/page/n83/mode/2up) simply prompts a look to the Duke University Archives. York is mentioned here as [correspondent to Tod Robinson Caldwell](https://archive.org/details/rubensteinmanuscriptcatalog_M._Butler_to_Caq/page/n202/mode/2up). 
    [This collection](https://archive.org/details/rubensteinmanuscriptcatalog_Durh_to_Els/page/n586/mode/2up) mentions early foundations of Duke Univesity and President Craven.
    Here is [York's son's collection](https://archive.org/details/rubensteinmanuscriptcatalog_X_to_Z/page/n89/mode/2up).

    Four cards mention William Gannaway Brownlow, former Governor of Tennesee and one is a prompt to [see the archives](https://archive.org/details/rubensteinmanuscriptcatalog_Fro_to_Geq/page/n322/mode/2up).

    Like many of the other presidents, Wood has a [card](https://archive.org/details/rubensteinmanuscriptcatalog_S._Williams_to_Wood/page/n717/mode/2up) prompting a check of the archives.
    Marquis Wood also has two collections of [papers](https://archive.org/details/rubensteinmanuscriptcatalog_Meth_to_Mh/page/59/mode/2up) associated with the Methodist Episcopal [Church](https://archive.org/details/rubensteinmanuscriptcatalog_Meth_to_Mh/page/n344/mode/2up).
    In William Clark Doub's [collection](https://archive.org/details/rubensteinmanuscriptcatalog_Del_to_Dov/page/19/mode/2up), Wood's manuscript on the introduction of Methodism into the Yadkin Valley is mentioned.

    We, of course, have the entry under Crowell's name to [See Duke University Archives](https://archive.org/details/rubensteinmanuscriptcatalog_Cre_to_I._Davis/page/n119/mode/2up).
    This [card](https://archive.org/details/rubensteinmanuscriptcatalog_A_to_Amer/page/n127/mode/2up) mentions a quarrel between Crowell and his faculty.
    [This](https://archive.org/details/rubensteinmanuscriptcatalog_Mus_to_Nn/page/n105/mode/2up) and [this](https://archive.org/details/rubensteinmanuscriptcatalog_Gri_to_Hand/page/n131/mode/2up) mention letters to and from John Crowell.
    [Here](https://archive.org/details/rubensteinmanuscriptcatalog_V_to_Ward/page/n85/mode/2up) Crowell is part of a list of unpublished sketches of well-known North Carolinians.

    Here we have the boilerplate John Kilgo [card](https://archive.org/details/rubensteinmanuscriptcatalog_K_to_Kira/page/n489/mode/2up).

    Kilgo is listed as a correspondent in the Hemphill Family [Collection](https://archive.org/details/rubensteinmanuscriptcatalog_Harw_to_Hem/page/23/mode/2up).
    Kilgo appears to have been involved in the Methodist Episcopal Church [here](https://archive.org/details/rubensteinmanuscriptcatalog_Meth_to_Mh/page/n503/mode/2up) and [here](https://archive.org/details/rubensteinmanuscriptcatalog_Mi_to_Mord/page/n686/mode/2up).
    Correspondence with President Kilgo is mentioned [here](https://archive.org/details/rubensteinmanuscriptcatalog_Ton_to_Tz/page/n668/mode/2up) and [here](https://archive.org/details/rubensteinmanuscriptcatalog_Wi._Smith_to_So/page/n642/mode/2up) in relation to the Southgates.
    Kilgo seems to be something of a controversial and outspoken character, as [here](https://archive.org/details/rubensteinmanuscriptcatalog_J._Brown_to_L._Butler/page/n675/mode/2up) and [here](https://archive.org/details/rubensteinmanuscriptcatalog_Ton_to_Tz/page/81/mode/2up) he is spoken of positively and [here](https://archive.org/details/rubensteinmanuscriptcatalog_A_to_Amer/page/n157/mode/2up) and [here](https://archive.org/details/rubensteinmanuscriptcatalog_Wi._Smith_to_So/page/n639/mode/2up) he is said to be involved in a court case.

    In addition to the requisite Flowers [card](https://archive.org/details/rubensteinmanuscriptcatalog_Fif_to_Frn/page/n276/mode/2up) we have correspondence between Flowers and others [here](https://archive.org/details/rubensteinmanuscriptcatalog_Conl_to_Crd/page/n265/mode/2up), [here](https://archive.org/details/rubensteinmanuscriptcatalog_Gre_to_Grh/page/n605/mode/2up), [here](https://archive.org/details/rubensteinmanuscriptcatalog_No_to_Oz/page/151/mode/2up), [here](https://archive.org/details/rubensteinmanuscriptcatalog_Wi._Smith_to_So/page/n632/mode/2up), [here](https://archive.org/details/rubensteinmanuscriptcatalog_Wi._Smith_to_So/page/n638/mode/2up), and [here](https://archive.org/details/rubensteinmanuscriptcatalog_J._Thomas_to_Tom/page/n73/mode/2up).
    President Flowers is praised [here](https://archive.org/details/rubensteinmanuscriptcatalog_Ton_to_Tz/page/81/mode/2up) along with some other notable Dukies and had gifted some items related to the Methodist Church [here](https://archive.org/details/rubensteinmanuscriptcatalog_Meth_to_Mh/page/n17/mode/2up).
    He is also in a [photograph](https://archive.org/details/rubensteinmanuscriptcatalog_Lowr_to_Mack/page/n115/mode/2up) that is cataloged and is said to have written a biography of [Edwin W. Fuller](https://archive.org/details/rubensteinmanuscriptcatalog_Fro_to_Geq/page/n95/mode/2up).

    As Terry Sanford was a US Senator and NC Governor as well as a President of Duke, there appear to be many cards mentioning him. Cards mentioning correspondence with Sanford can be found [here](https://archive.org/details/rubensteinmanuscriptcatalog_R._Boyd_to_I._Brown/page/n126/mode/2up), [here](https://archive.org/details/rubensteinmanuscriptcatalog_Claw_to_Com/page/n498/mode/2up), [here](https://archive.org/details/rubensteinmanuscriptcatalog_Claw_to_Com/page/n506/mode/2up), [here](https://archive.org/details/rubensteinmanuscriptcatalog_Hold_to_Huba/page/n149/mode/2up), [here](https://archive.org/details/rubensteinmanuscriptcatalog_J._Thomas_to_Tom/page/80/mode/2up), and [here](https://archive.org/details/rubensteinmanuscriptcatalog_Ton_to_Tz/page/n177/mode/2up).
    [This](https://archive.org/details/rubensteinmanuscriptcatalog_Wi._Smith_to_So/page/n580/mode/2up) talks about the Southern Rural Poverty Project, directed by members of the Sanford Institute of Public Policy.
    [Here](https://archive.org/details/rubensteinmanuscriptcatalog_Claw_to_Com/page/n519/mode/2up) and [here](https://archive.org/details/rubensteinmanuscriptcatalog_Hane_to_Harv/page/n9/mode/2up) are collections that catalog items that talk about Sanford.
    [Here] and on subsequent pages we have a restricted collection relating to manuscripts created by Terry Sanford, related to his time as Governor and Duke President. And [here](https://archive.org/details/rubensteinmanuscriptcatalog_San_to_Sem/page/n73/mode/2up) there are documents related to his time as a US Senator.

    Few is mentioned as a professor [here](https://archive.org/details/rubensteinmanuscriptcatalog_J._Brown_to_L._Butler/page/1873/mode/2up).
    He is included in collections with other important Duke figures [here](https://archive.org/details/rubensteinmanuscriptcatalog_Ben_to_Blac/page/n481/mode/2up), [here](https://archive.org/details/rubensteinmanuscriptcatalog_Dow_to_Durg/page/n255/mode/2up), [here](https://archive.org/details/rubensteinmanuscriptcatalog_Fif_to_Frn/page/n292/mode/2up), [here](https://archive.org/details/rubensteinmanuscriptcatalog_Harw_to_Hem/page/21/mode/2up), [here](https://archive.org/details/rubensteinmanuscriptcatalog_Pep_to_Pn/page/n47/mode/2up), and [here](https://archive.org/details/rubensteinmanuscriptcatalog_Wi._Smith_to_So/page/n641/mode/2up).
    Correspondece with William Few is mentioned [here](https://archive.org/details/rubensteinmanuscriptcatalog_Lanp_to_Ler/page/n223/mode/2up), [here](https://archive.org/details/rubensteinmanuscriptcatalog_P_to_Peo/page/39/mode/2up), and [here](https://archive.org/details/rubensteinmanuscriptcatalog_V_to_Ward/page/n403/mode/2up).
    Few's son, Lynne Few, appears [here](https://archive.org/details/rubensteinmanuscriptcatalog_Ger_to_Gorl/page/n536/mode/2up).
    He also has a [collection](https://archive.org/details/rubensteinmanuscriptcatalog_Elt_to_Fie/page/n625/mode/2up) of papers related to war and money.
    Ella Howerton Parks remembers Few as the ["prince of all hat doffers."](https://archive.org/details/rubensteinmanuscriptcatalog_P_to_Peo/page/n295/mode/2up).
    [This collection](https://archive.org/details/rubensteinmanuscriptcatalog_V_to_Ward/page/n649/mode/2up) talks about a treatise Few signed related to the relations between the northern and southern colonies.

    President Craven's great grandson has a rather extensive [collection](https://archive.org/details/rubensteinmanuscriptcatalog_Conl_to_Crd/page/n689/mode/2up) and his grandson is mentioned [here](https://archive.org/details/rubensteinmanuscriptcatalog_Conl_to_Crd/page/n677/mode/2up).
    Braxton Craven is cataloged in the 1850 census of Randolph County [here](https://archive.org/details/rubensteinmanuscriptcatalog_Armi_to_Bal/page/n486/mode/2up) along with many transactions under his name. Another money-related [card](https://archive.org/details/rubensteinmanuscriptcatalog_Con_to_Conk/page/n403/mode/2up) mentions a statement for what Trinity College owed a company.
    Correspondences involving Craven are cataloged [here](https://archive.org/details/rubensteinmanuscriptcatalog_Durh_to_Els/page/n586/mode/2up), [here](https://archive.org/details/rubensteinmanuscriptcatalog_Harw_to_Hem/page/n34/mode/2up), and [here](https://archive.org/details/rubensteinmanuscriptcatalog_Harw_to_Hem/page/n88/mode/2up).
    Craven is mentioned, but not in much detail [here](https://archive.org/details/rubensteinmanuscriptcatalog_Elt_to_Fie/page/n469/mode/2up), [here](https://archive.org/details/rubensteinmanuscriptcatalog_Gri_to_Hand/page/n128/mode/2up), [here](https://archive.org/details/rubensteinmanuscriptcatalog_Harw_to_Hem/page/167/mode/2up), [here](https://archive.org/details/rubensteinmanuscriptcatalog_J._Johnson_to_Jz/page/n676/mode/2up), [here](https://archive.org/details/rubensteinmanuscriptcatalog_Lanp_to_Ler/page/27/mode/2up), and [here](https://archive.org/details/rubensteinmanuscriptcatalog_I._White_to_R._Williams/page/n408/mode/2up).
    """)
    
    st.subheader("Duke Building Names in the Catalog")
    
    st.write("""
    Here are the counts of the building names present in the collection headers' name column: 
    
    Alspaugh: 1, Brodie: 1, Crowell: 1, Edens: 1, Kilgo: 1, Bassett: 2, Lilly: 2, Southgate: 4, Flowers: 4, Few: 4, Pegram: 5, Wilkinson: 5, Perkins: 6, Giles: 7, Baldwin: 9, Hart: 10, Sanford: 10, Craven: 10, Gray: 13, Biddle: 19, Blackwell: 36, White: 42, Allen: 46, Wilson: 49, Brown: 74


    Lilly, Pegram, Wilkinson, Gray, White, Allen, Wilson, Brown, unfortunately, do not have any hits that are directly relevant to the history of the building, but it is still interesting to see the prevalence of Duke-related names, regardless if it is the same specific individuals. Additionally, the library's history of East Campus buildings is found [here](https://library.duke.edu/rubenstein/uarchives/history/exhibits/building-names/east).
    
    Similar to the presidents, some of these names' only relevant cards are the "See Duke University Archives" cards assoicated with the person the building is named after. See [Alspaugh](https://archive.org/details/rubensteinmanuscriptcatalog_A_to_Amer/page/n644/mode/2up), [Bassett](https://archive.org/details/rubensteinmanuscriptcatalog_Bam_to_Bedh/page/n449/mode/2up), and [Baldwin](https://archive.org/details/rubensteinmanuscriptcatalog_Armi_to_Bal/page/n575/mode/2up).

    There are, however, a couple mentions of the Bassett Affair [here](https://archive.org/details/rubensteinmanuscriptcatalog_Wi._Smith_to_So/page/n639/mode/2up) and [here](https://archive.org/details/rubensteinmanuscriptcatalog_J._Brown_to_L._Butler/page/n81/mode/2up). [The Bassett Affair](https://library.duke.edu/rubenstein/uarchives/history/articles/bassett-affair) was when John Spencer Bassett added a sentence in his journal praising Booker T. Washington as one of the best southerners in the past 100 years, enraging many Southern Democrats. President Kilgo and other faculty and students supported Bassett and the Trinity Board of Trustees voted not to accept his resignation, leading to favorable publicity for the college and setting a precident for academic freedom.

    James Southgate had numerous items recorded in the catalog. Starting with [this card](https://archive.org/details/rubensteinmanuscriptcatalog_Wi._Smith_to_So/page/n602/mode/2up), there is a lot of information about James and family. Southgate's son, James Haywood was a Trinity College trustee and is discussed in his father's collections. The senior's letters are described being more of interest than Haywood's, who wrote anout the insurance business and family stress. Kilgo, apparently was a friend of J.H.

    The Giles sisters were the first women to recieve degrees from Trinity college, both undergraduate and graduate. Mary Giles' [collection](https://archive.org/details/rubensteinmanuscriptcatalog_Ger_to_Gorl/page/n279/mode/2up) includes papers concerning her and her sisters' education, international travels, and their lives after college.

    William Thomas Blackwell was the founder of the Bull Durham Tobacco Company and has many associated collections in the catalog, starting [here](https://archive.org/details/rubensteinmanuscriptcatalog_Ben_to_Blac/page/n725/mode/2up). The cards discuss his tobacco business and his financial woes. There are many money-related logs, ledgers, and journals.

    The card corresponding to Mary Duke Biddle's collection is found [here](https://archive.org/details/rubensteinmanuscriptcatalog_Ben_to_Blac/page/n481/mode/2up). It contains a variety of documents relating to various aspects of her life.

    William Robertson Perkins was a judge who was counsel to James B. Duke and a trustee of the Duke Endowment. Starting [here](https://archive.org/details/rubensteinmanuscriptcatalog_Pep_to_Pn/page/n45/mode/2up), his collection discusses his connection to the university and employment.
    """)
    
    
    st.subheader("Duke's Nomenclature")
    
    counts = [0, 2, 21, 169, 523]
    names = ["Brown School", "Union Institute", "Normal College", "Trinity College", "Duke University"]
    
    # Create bar chart of Duke name frequencies
    fig, ax = plt.subplots()
    plt.bar(names, counts, color='#00539B')
    plt.xticks(rotation = 45)
    plt.title("Occurances of Duke's Names in the Catalog")
    plt.xlabel("Name")
    plt.ylabel("# of Cards")
    plt.show()
    st.pyplot(fig)
    
    st.write("""
    Actual Dates of Institutions:
    
    Brown School: 1838-1841

    Union Institution: 1841-1851

    Normal College: 1851-1859

    Trinity College: 1859-1924

    Duke University: 1924-present

    Average Associated Date in the Catalog:
    
    Brown School: N/A

    Union Institution: 1880

    Normal College: 1871

    Trinity College: 1884

    Duke University: 1917
    """)