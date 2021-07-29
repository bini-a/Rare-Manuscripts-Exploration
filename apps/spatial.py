import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px
import plotly.graph_objects as go

def app():
    st.title("Spatial Info")
    st.write(""" 
    - US states
    - NC states
    - Foreign Countries...
    """)
    
    st.subheader("USA Spatial Frequency of Card Catalog Manuscripts")

    fig = px.choropleth(locations=['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'], locationmode="USA-states", color=[153, 0, 1, 16, 11, 3, 76, 5, 43, 17, 371, 1, 0, 25, 21, 13, 3, 53, 71, 11, 218, 169, 12, 3, 63, 33, 0, 3, 0, 22, 17, 6, 302, 1188, 1, 63, 3, 2, 193, 19, 299, 0, 81, 22, 4, 13, 1631, 5, 48, 3, 1], scope="usa", hover_name=['Alabama','Alaska','Arizona','Arkansas','California','Colorado','Connecticut','Delaware','District of Columbia','Florida','Georgia','Hawaii','Idaho','Illinois','Indiana','Iowa','Kansas','Kentucky','Louisiana','Maine','Maryland','Massachusetts','Michigan','Minnesota','Mississippi','Missouri','Montana','Nebraska','Nevada','New Hampshire','New Jersey','New Mexico','New York','North Carolina','North Dakota','Ohio','Oklahoma','Oregon','Pennsylvania','Rhode Island','South Carolina','South Dakota','Tennessee','Texas','Utah','Vermont','Virginia','Washington','West Virginia','Wisconsin','Wyoming',], color_continuous_scale="YlGnBu", labels={'color':'Count', 'locations':'State Abrev.'})
    st.plotly_chart(fig,use_container_width=True)

    st.header("Alternative display")
    lc =['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
    txt =['Alabama','Alaska','Arizona','Arkansas','California','Colorado','Connecticut','Delaware','District of Columbia','Florida','Georgia','Hawaii','Idaho','Illinois','Indiana','Iowa','Kansas','Kentucky','Louisiana','Maine','Maryland','Massachusetts','Michigan','Minnesota','Mississippi','Missouri','Montana','Nebraska','Nevada','New Hampshire','New Jersey','New Mexico','New York','North Carolina','North Dakota','Ohio','Oklahoma','Oregon','Pennsylvania','Rhode Island','South Carolina','South Dakota','Tennessee','Texas','Utah','Vermont','Virginia','Washington','West Virginia','Wisconsin','Wyoming']
    fig = px.choropleth(locations=['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'], locationmode="USA-states", color=[153, 0, 1, 16, 11, 3, 76, 5, 43, 17, 371, 1, 0, 25, 21, 13, 3, 53, 71, 11, 218, 169, 12, 3, 63, 33, 0, 3, 0, 22, 17, 6, 302, 1188, 1, 63, 3, 2, 193, 19, 299, 0, 81, 22, 4, 13, 1631, 5, 48, 3, 1], scope="usa", hover_name=['Alabama','Alaska','Arizona','Arkansas','California','Colorado','Connecticut','Delaware','District of Columbia','Florida','Georgia','Hawaii','Idaho','Illinois','Indiana','Iowa','Kansas','Kentucky','Louisiana','Maine','Maryland','Massachusetts','Michigan','Minnesota','Mississippi','Missouri','Montana','Nebraska','Nevada','New Hampshire','New Jersey','New Mexico','New York','North Carolina','North Dakota','Ohio','Oklahoma','Oregon','Pennsylvania','Rhode Island','South Carolina','South Dakota','Tennessee','Texas','Utah','Vermont','Virginia','Washington','West Virginia','Wisconsin','Wyoming',], color_continuous_scale="YlGnBu", labels={'color':'Count', 'locations':'State Abrev.'})
    fg = go.Figure(data=fig)

    fg.add_scattergeo(locations=lc,    ###codes for states,
    locationmode='USA-states',
    text=lc,
    mode='text')
    st.plotly_chart(fg,use_container_width=True)

   
    
    st.subheader("International Frequency of Card Catalog Manuscripts")
    
    df = pd.read_csv("world.csv")
    
    fig = px.choropleth(df, locations='iso', color='count', hover_name="hover_name", color_continuous_scale=px.colors.sequential.Plasma)
    st.plotly_chart(fig,use_container_width=True)
    
    
    colors = ['#C84E00', '#E89923', '#FFD960', '#A1B70D', '#339898', '#993399']

    fig = go.Figure(data=[go.Pie(labels=['Europe', 'Asia', 'North America', 'South America', 'Africa', 'Oceania'], values=[197, 70, 20, 16, 12, 3])])
    fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                  marker=dict(colors=colors, line=dict(color='#000000', width=2)))
    st.plotly_chart(fig,use_container_width=True)
    
        

    
    st.subheader("NC County Spatial Frequency of Card Catalog Manuscripts")
    
    # nc = gpd.read_file('nc.csv')
    
    # fig = px.choropleth(nc,
    #            geojson=nc.geometry,
    #            locations=nc.index,
    #            color="Count",
    #            projection="mercator")
    # fig.update_geos(fitbounds="locations", visible=False)
    # st.plotly_chart(fig, use_container_width=True)