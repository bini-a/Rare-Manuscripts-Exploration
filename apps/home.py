import streamlit as st

def app():
    st.title("Home")
    st.write("""
    ## Duke Rubenstein Library Main Entry Card Catalog
    
    This site was created by the Duke University Data+ 2021 Rubenstein Library Card Catalog Team. Working with the digitized cards from the David M. Rubenstein Rare Book and Manuscript Library's physical card catalogs, our team explored the files as a way to further the library's initiative of finding and describing historically marginalized voices in their collections. The card catalog is a static resource, and has not been updated since before the cards were digitized.
    
    We have created a structured dataset out of these digitized cards, sorted by collection of items within the catalog. Using natural language processing and some manual editing, we pulled out important metadata such as author, date written, and location and have added links in the dataset to the corresponding card in the Internet Archives site for further exploration. This dataset will be uploaded to the Duke Research Data Repository to allow access for those who wish to dig deeper into the files.
    
    With the dataset we created, we have analysed what and who is present in these cards. Feel free to click through the tabs to see the visualizations and research we have done using this data, or use the dataset to answer your own questions. There is copious rich information present in the files, and our Data+ project is just the tip of the iceberg. We hope that future researchers will continue to disect the card files and continue to gain insights into Duke's history.
    """)
    if st.checkbox("How to use the tabs from the navigation menu?"):
        st.write("""
    - Data Analysis Tab: View or download our dataset, read our analysis of demographics, time and spatial distribution.  
    - Duke History Tab : Read about Duke Presidents, Duke Building Names & Duke's Early names mentioned in the dataset.   
    - Explore Tab : Explore the dataset interactively by selecting time range, author name, country of origin, and drawer number.  
    - Selected Collection Tab: Explore hand-picked collections from the dataset in topics such as History of Slavery, Charleston Earthquake, Wilmington Race Riot of 1898 and Duke University Presidents.
    """)

