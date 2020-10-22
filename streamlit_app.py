
import streamlit as st
import pandas as pd
import altair as alt
import json

@st.cache
def get_covid_data():
  with open('repeated_data.json') as json_f:
    repeated_json = json.load(json_f)
    return alt.Data(values=repeated_json["features"])

@st.cache
def get_world_data():
  with open('world_data.json') as json_f:
    world_json = json.load(json_f)
    return alt.Data(values=world_json["features"])

repeated_data = get_covid_data()
world_data = get_world_data()

my_selector = alt.selection_multi(fields = ["properties.location"])

chart = alt.Chart(repeated_data,title = "Percentage of Elderly and GDP for each Country").mark_circle().encode(
    x = alt.X("properties.gdp_per_capita:Q", title='GDP per Capita'),
    y=alt.Y("properties.aged_65_older:Q", title='Percentage of Elderly'),
    color=alt.condition(my_selector, alt.Color("properties.Continent:N",title = "Continent"), alt.value('lightgray')),
    size=alt.Size("properties.population:Q",scale=alt.Scale(domain=(-400000000, 1850000000)),legend=None),
    tooltip=alt.Tooltip('properties.location:N',title = "Country")
    
).add_selection(
    my_selector
).properties(
    width=300,
    height=200
)


one_country = alt.Chart(repeated_data).mark_geoshape().encode(
    color= alt.condition(
        my_selector, alt.Color("properties.Continent:N"),  alt.value('gray')
    ),
    tooltip=alt.Tooltip('properties.location:N',title = "Country")
).properties(
    width=375,
    height=200
).add_selection(
    my_selector
)

world = alt.Chart(world_data).mark_geoshape().encode(
    color=alt.value('lightgray'),
    tooltip=alt.Tooltip('properties.location:N', title = "Country")
).properties( 
    width=375,
    height=200
)


boundaries = alt.Chart(world_data, title='World Map').mark_geoshape(
    stroke='white',
    strokeWidth=1,
    fill=None
)


fear = alt.Chart(repeated_data, title='Twitter Fear over Time').mark_bar().encode(
    x=alt.X('properties.week:O',title= "Week"),
    y=alt.Y('mean(properties.fear_percentage):Q', title = "Fear Index"),
    color= alt.value("gray")
).transform_filter(
    my_selector
).properties(
    width = 700,
    height = 150
)

cases = alt.Chart(repeated_data, title='Covid Infections over Time').mark_bar().encode(
    x=alt.X('properties.week:O', title = "Week"),
    y=alt.Y('mean(properties.new_cases_per_million):Q',title="New Cases per Million"),
    color = alt.value('darkred')
).transform_filter(
    my_selector
).properties(
    width = 700,
    height = 150
)

deaths = alt.Chart(repeated_data, title='Covid Deaths over Time').mark_bar().encode(
    x=alt.X('properties.week:O', title = "Week"),
    y=alt.Y('mean(properties.new_deaths_per_million):Q',title="New Deaths per Million"),
    color = alt.value('darkblue')
).transform_filter(
    my_selector
).properties(
    width = 700,
    height = 150
)

st.write((chart | world + one_country  + boundaries) & fear & cases  & deaths)

expander = st.beta_expander("Instructions")
expander.write("This visualization app allows you to view how the public sentiment of fear changed in 15 countries as a result of the novel Coronavirus. By clicking a country on either of the top two graphs, you can view how the Fear Index varied in comparison to new Covid cases and deaths. \n\n By holding shift and pressing multiple countries you can view Covid fear and Covid statistics on an aggregated level.")
expander = st.beta_expander("What is the Fear Index")
expander.write("The Fear Index is the percentage of Covid-related tweets that contain keywords related to fear. These keywords include conjugations of multiple synonyms such as scared, afraid and nervous. \n\n To collect the Tweets, we utilize the publically available Harvard 'Coronavirus Tweet Ids' dataset.")
