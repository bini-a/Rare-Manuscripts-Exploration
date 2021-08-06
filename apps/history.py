import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re
from scipy import stats
import operator
import plotly.express as px

def app():
    st.title("History")
    st.write("""See the 'Selected Collections' tab to see the Duke Presidents, Building Names, and Early Duke Names in the dataset""")
    st.header("History of Duke Presidents in the Catalog")
    # st.write("""Our first approach for finding presidents was a simple search for their last names. However, most of these occurances were unrealated to the presidents, so for our second approach we looked for both the first and last name appearing together in a card and yielded much better results, shown below.""")
    
    #---------------------------------------------------------------------------------------------------------------------------------------
    # Print graph of counts per presidential name
    last = ["York", "Craven", "Gannaway", "Wood", "Crowell", "Kilgo", "Few", "Flowers", "Edens", "Hart", "Knight", "Sanford", "Brodie", "Keohane", "Brodhead"]
    name_counts = [4, 36, 5, 5, 5, 10, 34, 15, 0, 1, 4, 17, 0, 0, 3]
    
    # # Disply bar chart of first and last name occurances
    # fig, ax = plt.subplots()
    # plt.bar(last, name_counts, color='#00539B')
    # plt.xticks(rotation = 45)
    # plt.title("Occurances of Duke Presidental Names in the Card Catalog")
    # plt.xlabel("Name")
    # plt.ylabel("# of Cards")
    # plt.show()
    # st.pyplot(fig)

#     "Better to have interactive graph with plotly"
    br =px.bar({"Names":last,"Number of Records":name_counts},x="Names",y="Number of Records")
    st.subheader("Occurances of Duke Presidental Names in the Card Catalog")
    st.plotly_chart(br,use_container_width=True)
    
    if st.checkbox("See caveats", key="1"):
        st.write("""*
        While this search method is fairly accurate, there are still some instances in which the names refer to unrelated people.
        *""")
    
    st.write("""Here we have a graph of the frequencies of each president's name in the catalog. Let's look at what these cards have to say about the Duke presidents.""")
    
    #---------------------------------------------------------------------------------------------------------------------------------------
    
    st.subheader("Qualitative Analysis of Presidents")
    
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
    
    #-----------------------------------------------------------------------------------------------------------------------------------
    
    st.header("Duke Building Names in the Catalog")
    
    st.write("""
    Here are the counts of the building names present in the collection headers' name column: 
    
    *Alspaugh: 1, Brodie: 1, Crowell: 1, Edens: 1, Kilgo: 1, Bassett: 2, Lilly: 2, Southgate: 4, Flowers: 4, Few: 4, Pegram: 5, Wilkinson: 5, Perkins: 6, Giles: 7, Baldwin: 9, Hart: 10, Sanford: 10, Craven: 10, Gray: 13, Biddle: 19, Blackwell: 36, White: 42, Allen: 46, Wilson: 49, Brown: 74*""")
    
    if st.checkbox("See caveats",key="2"):
        st.write("""*
        Many of these names are not related directly to the person or persons for which these buildings were named. However, they may suggest family ties to the university lasting for multiple generations. Check out the 'Selected Collections' tab or search in the Internet Archive to explore the contents of these cards.
        *""")
    
    st.subheader("Qualitative Analysis of Building Names")

    st.write("""
    Lilly, Pegram, Wilkinson, Gray, White, Allen, Wilson, Brown, unfortunately, do not have any hits that are directly relevant to the history of the building, but it is still interesting to see the prevalence of Duke-related names, regardless if it is the same specific individuals. Additionally, the library's history of East Campus buildings is found [here](https://library.duke.edu/rubenstein/uarchives/history/exhibits/building-names/east).
    
    Similar to the presidents, some of these names' only relevant cards are the "See Duke University Archives" cards assoicated with the person the building is named after. See [Alspaugh](https://archive.org/details/rubensteinmanuscriptcatalog_A_to_Amer/page/n644/mode/2up), [Bassett](https://archive.org/details/rubensteinmanuscriptcatalog_Bam_to_Bedh/page/n449/mode/2up), and [Baldwin](https://archive.org/details/rubensteinmanuscriptcatalog_Armi_to_Bal/page/n575/mode/2up).

    There are, however, a couple mentions of the Bassett Affair [here](https://archive.org/details/rubensteinmanuscriptcatalog_Wi._Smith_to_So/page/n639/mode/2up) and [here](https://archive.org/details/rubensteinmanuscriptcatalog_J._Brown_to_L._Butler/page/n81/mode/2up). [The Bassett Affair](https://library.duke.edu/rubenstein/uarchives/history/articles/bassett-affair) was when John Spencer Bassett added a sentence in his journal praising Booker T. Washington as one of the best southerners in the past 100 years, enraging many Southern Democrats. President Kilgo and other faculty and students supported Bassett and the Trinity Board of Trustees voted not to accept his resignation, leading to favorable publicity for the college and setting a precident for academic freedom.

    James Southgate had numerous items recorded in the catalog. Starting with [this card](https://archive.org/details/rubensteinmanuscriptcatalog_Wi._Smith_to_So/page/n602/mode/2up), there is a lot of information about James and family. Southgate's son, James Haywood was a Trinity College trustee and is discussed in his father's collections. The senior's letters are described being more of interest than Haywood's, who wrote anout the insurance business and family stress. Kilgo, apparently was a friend of J.H.

    The Giles sisters were the first women to recieve degrees from Trinity college, both undergraduate and graduate. Mary Giles' [collection](https://archive.org/details/rubensteinmanuscriptcatalog_Ger_to_Gorl/page/n279/mode/2up) includes papers concerning her and her sisters' education, international travels, and their lives after college.

    William Thomas Blackwell was the founder of the Bull Durham Tobacco Company and has many associated collections in the catalog, starting [here](https://archive.org/details/rubensteinmanuscriptcatalog_Ben_to_Blac/page/n725/mode/2up). The cards discuss his tobacco business and his financial woes. There are many money-related logs, ledgers, and journals.

    The card corresponding to Mary Duke Biddle's collection is found [here](https://archive.org/details/rubensteinmanuscriptcatalog_Ben_to_Blac/page/n481/mode/2up). It contains a variety of documents relating to various aspects of her life.

    William Robertson Perkins was a judge who was counsel to James B. Duke and a trustee of the Duke Endowment. Starting [here](https://archive.org/details/rubensteinmanuscriptcatalog_Pep_to_Pn/page/n45/mode/2up), his collection discusses his connection to the university and employment.
    """)
    
    
    st.header("Duke's Nomenclature")
    
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
    
    if st.checkbox("See caveats", key="3"):
        st.write("""*These are the counts of the occurances of a full name in the catalog (e.g., "Trinity College"). These may just be a boilerplate phrase like "See Duke University Archives" or they may provide deeper insights into the university's history. Check out the 'Selected Collections' tab to see the relevance of the results.
        *""")
    
    st.subheader("Actual Dates of Institutions:")
    st.write("""
    Brown School: 1838-1841

    Union Institution: 1841-1851

    Normal College: 1851-1859

    Trinity College: 1859-1924

    Duke University: 1924-present""")

    st.subheader("Average Associated Date in the Catalog:")
    
    st.write("""
    Brown School: N/A

    Union Institution: 1880

    Normal College: 1871

    Trinity College: 1884

    Duke University: 1917
    """)
    
    #-------------------------------------------------------------------------------------------------------------------------------
    
    brown = []
    union = ['1863-1890', '1879-1889']
    normal = ['1833-1985', '1852-1853', '1881-1919', '1846-1933', '1846-1933', '1820-1907', '1783-1940', '1840-1925', '1851-1861', '1851-1861', '1851-1861', '1870-1900', '1870-1900', '1757-1978', '1757-1978', '1852-1857', '1896-1902', '1856-1866', '1830-1850', '1853-1862', '1853-1862']
    trinity = ['1891-1913', '1901-1922', '1847-1890', '1865', '1833-1967', '1852-1853', '1924-1971', '1859', '1887-1960', '1886-1888', '1886-1888', '1842-1864', '1842-1864', '1951', '1912-1974', '1896-1899', '1905', '1806-1909', '1806-1909', '1806-1909', '1885-1976', '1885-1976', '1885-1976', '1885-1976', '1855-1885', '1855-1885', '1914-1946', '1902-1961', '1912-1976', '1861-1865', '1752-1927', '1913-1914', '1854-1869', '1893-1898', '1893-1898', '1893-1898', '1893-1898', '1893-1898', '1785-1966', '1785-1966', '1785-1966', '1816-1876', '1889-1894', '1859-1905', '1909', '1820-1869', '1820-1869', '1820-1869', '1855-1929', '1855-1929', '1783-1984', '1851-1861', '1818-1894', '1846-1942', '1846-1942', '1846-1942', '1836-1932', '1325-1408', '1892-1910', '1848-1984', '1848-1984', '1788-1952', '1767-1965', '1767-1965', '1848-1893', '1796-1891', '1884-1886', '1841-1929', '1841-1929', '1841-1929', '1841-1929', '1903', '1870', '1810-1929', '1915-1955', '1912-1955', '1797-1919', '1840-1856', '1918-1973', '1869', '1881-1935', '1935-1936', '1831-1879', '1881-1916', '1772-1899', '1772-1899', '1860-1927', '1873-1882', '1788-1797', '1788-1797', '1884-1887', '1900-1911', '1861', '1875-1887', '1875-1887', '1860-1877', '1885-1890', '1885-1890', '1885-1890', '1888-1892', '1888-1892', '1888-1892', '1875-1887', '1893-1971', '1805-1881', '1919-1973', '1890-1953', '1889-1917', '1977', '1900-1961', '1881-1959', '1889-1890', '1894-1912', '1918', '1893-1897', '1910-1935', '1864-1868', '1889-1958', '1889-1958', '1924-1952', '1767-1905', '1767-1905', '1747-1751', '1920', '1875-1912', '1837-1893', '1886-1967', '1913-1917', '1854-1940', '1855-1869', '1856-1937', '1856-1937', '1856-1871', '1884-1887', '1851-1935', '1851-1935', '1851-1935', '1851-1935', '1912-1933', '1803-1891', '1915-1954', '1915-1954', '1866-1891', '1866-1891', '1888-1975', '1748-1989', '1748-1989', '1748-1989', '1829-1901', '1829-1901', '1905-1922', '1905-1922', '1905-1922', '1774-1777', '1694', '1891-1969', '1891-1969', '1835-1961', '1835-1961', '1835-1961', '1884-1939', '1890-1948', '1842', '1856-1866', '1828-1969', '1828-1969', '1828-1969', '1879-1889', '1784-1837']
    duke = ['1973-1989', '1973-1989', '1967-1995', '1962', '1990-1995', '1923-1960', '1843-1971', '1843-1971', '1843-1971', '1843-1971', '1843-1971', '1843-1971', '1866-1969', '1987', '1987', '1987', '1814', '1977-1982', '1977-1982', '1955-1984', '1925-1968', '1925-1968', '1844', '1964-1992', '1913-1962', '1856-1950', '1901-1970', '1833-1967', '1913-1966', '1805-1952', '1805-1952', '1805-1952', '1809-1824', '1866-1868', '1799-1870', '1872-1904', '1820-1962', '1755-1967', '1755-1967', '1216', '1887-1960', '1858-1936', '1967-1984', '1967-1984', '1967-1984', '1899-1972', '1963', '1798-1813', '1840-1865', '1840-1865', '1939-1963', '1846-1933', '1846-1933', '1930-1950', '1922-1976', '1922-1976', '1894', '1868-1928', '1912-1974', '1912-1974', '1912-1974', '1912-1974', '1912-1974', '1912-1974', "1930-1950", "1930-1950", '1929', '1959-1966', '1851-1907', '1928-1986', '1854-1857', '1811-1899', '1680', '1680', '1822-1888', '1879-1922', '1884-1917', '1975-1979', '1731-1969', '1864', '1885-1976', '1885-1976', '1855-1885', '1962-1972', '1980-1985', '1821-1946', '1821-1946', '1821-1946', '1886-1978', '1862', '1936', '1914-1946', '1942-1944', '1902-1961', '1902-1961', '1981', '1924-1926', '1927-1938', '1927-1938', '1927-1938', '1927-1938', '1927-1938', '1927-1938', '1927-1938', '1927-1938', '1927-1938', '1912-1976', '1912-1976', '1946-1953', '1940-1953', '1941-1953', '1897-1910', '1847-1916', '1752-1927', '1931-1934', '1931-1934', '1881-1968', '1821-1973', '1918-1977', '1918-1977', '1785-1966', '1987', '1816-1876', '1816-1876', '1889-1894', '1927-1961', '1927-1961', '1889-1893', '1900-1982', '1846-1854', '1852-1854', '1865-1887', '1820-1869', '1820-1869', '1915', '1925-1968', '1973-1978', '1973-1978', '1973-1978', '1973-1978', '1973-1978', '1803-1883', '1920-1970', '1920-1970', '1920-1970', '1920-1970', '1979-1994', '1979-1994', '1979-1994', '1979-1994', '1979-1994', '1979-1994', '1979-1994', '1979-1994', '1979-1994', '1979-1994', '1979-1994', '1979-1994', '1979-1994', '1979-1994', '1979-1994', '1979-1994', '1979-1994', '1979-1994', '1979-1994', '1979-1994', '1979-1994', '1979-1994', '1979-1994', '1979-1994', '1979-1994', '1979-1994', '1992-1993', '1992-1993', '1992-1993', '1992-1993', '1992-1993', '1992-1993', '1992-1993', '1992-1993', '1974-1988', '1974-1988', '1974-1988', '1974-1988', '1974-1988', '1974-1988', '1974-1988', '1974-1988', '1971-1992', '1971-1992', '1971-1992', '1971-1992', '1943', '1772-1795', '1728-1984', '1896-1961', '1896-1961', '1827-1858', '1935', '1976', '1862-1902', '1837-1971', '1802', '1969', '1939', '1928-1983', '1928-1983', '1778-1783', '1765-1850', '1943-1948', '1786-1796', '1800-1981', '1800-1981', '1800-1981', '1800-1981', '1938-1939', '1727-1905', '1785-1900', '1860-1920', '1931-1942', '1905-1985', '1905-1985', '1905-1985', '1905-1985', '1967-1987', '1967-1987', '1707-1948', '1863-1909', '1914-1979', '1914-1979', '1814-1864', '1832', '1938-1996', '1938-1996', '1953-1964', '1788-1952', '1939', '1350-1995', '1930-1979', '1930-1979', "1700-1972", "1700-1972", "1700-1972", "1700-1972", "1700-1972", "1700-1972", "1700-1972", "1700-1972", '1799-1862', '1955-1980', '1927-1983', '1927-1983', '1907-1978', '1941-1942', '1971-1989', '1971-1989', '1971-1989', '1817-1844', '1913-1989', '1913-1989', '1913-1989', ' 1959-1979', '1921-1930', '1951', '1837-1874', '1958-1985', '1854-1855', '1930-1940', '1916-1928', '1967', '1759-1792', '1818-1982', '1818-1982', '1818-1982', '1842-1969', '1936-1983', '1770-1773', '1777-1783', '1727-1805', '1930-1969', '1972-1983', '1837-1841', '1839', '1819-1830', '1905-1986', '1905-1986', '1905-1986', '1905-1986', '1905-1986', '1905-1986', '1905-1986', '1905-1977', '1954-1962', '1871-1872', '1918-1986', '1780-1813', '1861-1991', '1889-1970', '1915-1955', '1940-1941', '1912-1955', '1757-1978', '1757-1978', '1858-1991', '1913-1970', '1913-1970', '1913-1970', '1837', '1997', '1997', '1901-1970', '1901-1970', '1901-1970', '1900-1927', '1755', '1983-1984', '1879-1969', '1879-1969', '1905-1949', '1947-1985', '1963-1980', '1963-1980', '1926-1947', '1940', '1848-1904', '1788-1789', '1911-1984', '1969', '1772-1899', '1797-1800', '1860-1927', '1784-1847', '1826-1895', '1834-1890', '1790-1820', '1788-1797', '1788-1797', '1764-1981', '1764-1981', '1764-1981', '1782-1821', '1860-1868', '1934-1977', '1852-1933', '1942', '1981-1985', '1972-1975', '1878-1934', '1806-1863', '1912-1913', '1917-1970', '1980', '1824-1859', '1899-1947', '1602-1677', '1923-1926', '1840-1949', '1840-1949', '1918-1975', '1956-1985', '1903', '1889-1917', '1957-1976', '1957-1963', '1900-1961', '1942-1970', '1969-1990', '1881-1959', '1881-1959', '1881-1959', '1932-1941', '1932-1941', '1903-1967', '1580-1892', '1952', '1961-1990', '1892-1921', '1972-1996', '1891-1976', '1962-1995', '1892-1959', '1861-1871', '1861-1871', '1968-1986', '1933', '1766', '1925-1938', '1887-1944', '1968-1964', '1968-1964', '1483-1974', '1934-1984', '1964-1982', '1852-1986', '1956-1976', '1956-1976', '1956-1976', '1918', '1922-1982', '1922-1982', '1891-1983', '1891-1983', '1864-1868', '1928-1995', '1928-1995', '1914', '1928-1971', '1928-1971', '1949', '1855-1907', '1776-1794', '1760-1790', '1934', '1760-1845', '1919-1962', '1941-1991', '1937-1990', '1937-1990', '1924-1952', '1926-1980', '1926-1980', '1926-1980', '1985-1992', '1985-1992', '1985-1992', '1983', '1983', '1946-1994', '1946-1994', '1946-1994', '1939-1986', '1939-1986', '1939-1986', '1939-1986', '1859-1959', '1925-1991', '1925-1991', '1925-1991', '1878-1991', '1878-1991', '1878-1991', '1933-1941', '1972-1974', '1812-1815', '1812-1815', '1886-1967', '1854-1940', '1983', '1887-1949', '1964-1965', '1916-1973', '1916-1973', '1887-1953', '1864', '1900-1976', '1900-1976', '1900-1976', '1992', '1851-1935', '1912-1933', '1931-1980', '1915-1954', '1743-1838', '1955-1984', '1904', '1937-1938', '1972-1981', '1888-1975', '1888-1975', '1888-1975', '1888-1975', '1764-1792', '1748-1989', '1748-1989', '1861-1865', '1861-1865', '1921-1953', '1914-1997', '1914-1997', '1829-1901', '1898-1954', '1898-1954', '1898-1954', '1975-1982', '1832-1837', '1596-1816', '1985-1987', '1905-1922', '1905-1922', '1851', '1814-1898', '1839-1880', '1924-1939', '1924-1939', '1971', '1971', '1918-1976', '1833-1834', '1888-1891', '1830-1880', '1843-1888', '1841-1977', '1841-1977', '1990-1992', '1779-1854', '1730-1975', '1750-1762', '1802-1883', '1828-1875', '1963-1979', '1726-1889', '1759-1828', '1879-1915', '1889-1968', '1812-1885', '1839-1961', '1954-1955', '1930-1961', '1957-1976', '1957-1976', '1957-1976', '1844-1955', '1879-1889']
    
    def start(college, dic):
        for i in range(1838, 2000):
            dic[i] = 0
        
        for date in college:
            dates = str(date).split("-")
            if int(dates[0]) >= 1838:
                dic[int(dates[0])] = dic.get(int(dates[0])) + 1
        return dic
    
    # dic1, dic2, dic3, dic4 = {}, {}, {}, {}
    # dic1 = start(union, dic1)
    # dic2 = start(normal, dic2)
    # dic3 = start(trinity, dic3)
    # dic4 = start(duke, dic4)
    
    # fig = plt.figure(figsize=(5,3))
    # plt.plot(dic4.keys(), dic4.values(), label='Duke', color='#00539B')
    # plt.plot(dic3.keys(), dic3.values(), label='Trinity', color='#FFD960')
    # plt.plot(dic2.keys(), dic2.values(), label='Normal', color='#E89923')
    # plt.plot(dic1.keys(), dic1.values(), label='Union', color='#C84E00')
    # plt.legend(loc='upper left')
    # plt.title("Mentions of Duke's Names over Time")
    # plt.xlabel("Year")
    # plt.ylabel("# of Mentions")
    # # st.pyplot(fig,use_col)
    # plt.savefig("duke_buildings.png")

    col1, col2, col3 = st.beta_columns([1,6,1])

    with col1:
        st.write("")

    with col2:
        st.image("duke_buildings.png")

    with col3:
        st.write("")
    
    if st.checkbox("See caveats", key="4"):
        st.write("""*The dates indicate the date the collection that mentions a Duke name was written. Due to inconsistancies in the cataloging dates, we were unable to pull those from the data, and are going off of the date written. For this chart, the start date is used for collections with date ranges.
        *""")
    
    st.write("""This plot shows the quantity of the dates of the collections that mention one of Duke's names, for each of the names.""") 
    
    st.header("Suggestions for Future Research")
    st.write("""
    While we were able to create a fairly comprehensive dataset containing all of the digitized cards, we were limited by our OCR software and data cleaning techniques. We have manually gone through the dataset to correct OCR errors in the authors' names; however, there are still many incomplete location or date cells, as well as some completly blank rows that the OCR did not pick up. Our first reccomendation, should another team continue this research, would be to manually correct some of the data which we were unable to correct due to time constrainsts and update our analysis which relies upon said data.
    
    An avenue of analysis that we were, unfortunately, unable to explore was sentiment analysis surrounding various groups in the catalog (e.g., the southern gentleman, slaves, southern belles). We would reccomend that future researchers analyze how these and other groups are represented and discussed in the catalog. In addition, the identification of "outdated language" in the cards would prove helpful.
    
    We were able to explore Duke's history in relation to its presidents, buildings, and early names; other topics to look into with regards to the university could be the historical ties to Methodism, the relationship with UNC, and the history of minority students (POC, women, international, etc.). Beyond the university, exploring major events such as the Civil War, slavery, and activism in North Carolina could be interesting as well.
    """)