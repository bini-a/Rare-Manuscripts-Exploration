import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re
from scipy import stats
import operator

def app():
    st.title("History")
    st.write("""
    History of Duke Presidents in the Catalog
    """)
    
    # Print graph of counts per presidential name
    last = ["York", "Craven", "Gannaway", "Wood", "Crowell", "Kilgo", "Few", "Flowers", "Edens", "Hart", "Knight", "Sanford", "Brodie", "Keohane", "Brodhead"]
    name_counts = [4, 36, 5, 5, 5, 10, 34, 15, 0, 1, 4, 17, 0, 0, 3]

    # Disply bar chart of first and last name occurances
    plt.bar(last, name_counts, color='#00539B')
    plt.xticks(rotation = 45)
    plt.title("Occurances of Duke Presidental Names in the Card Catalog")
    plt.xlabel("Name")
    plt.ylabel("# of Cards")
    plt.show()

    # Print regression of mentions vs time in office
    terms = [4, 37, 2, 1, 7, 16, 30, 7, 11, 3, 6, 16, 8, 11, 13]
    # Linear regression code adapted from https://www.w3schools.com/python/python_ml_linear_regression.asp
    slope, intercept, r, p, std_err = stats.linregress(terms, name_counts)
    def myfunc(x):
      return slope * x + intercept
    mymodel = list(map(myfunc, terms))

    # Plot labeled points, regression line
    plt.scatter(terms, name_counts, color='#00539B')
    for i in range(len(terms)):
        plt.annotate(last[i], (terms[i] - 1, name_counts[i] + 1), fontsize=7)
    plt.plot(terms, mymodel, color='#00539B')
    plt.title("Card Catalog Presidential Mentions versus Time in Office")
    plt.xlabel("Years in Office")
    plt.ylabel("# of Cards")
    plt.show()
    
    st.write("""
    Duke Building Names in the Catalog
    """)
    
    st.write("""
    Duke's Nomenclature
    """)