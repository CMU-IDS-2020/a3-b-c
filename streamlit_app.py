import streamlit as st
import numpy as np
import pandas as pd
import time
import altair as alt
import json

@st.cache
def Your_Covid_Data():
  with open('repeated_data.json') as json_f:
    repeated_json = json.load(json_f)
    return alt.Data(values=repeated_json["features"])

@st.cache
def Your_World_Data():
  with open('world_data.json') as json_f:
    world_json = json.load(json_f)
    return alt.Data(values=world_json["features"])

st.title("How Data-Driven are our Covid fears?")

expander = st.beta_expander("Instructions")
expander.write("This visualization app allows you to view how the public sentiment of fear has changed in 15 countries as a result of the novel Coronavirus. By clicking a country on either of the two graphs below, you can view how the Fear Index varied in comparison to new Covid cases and deaths. \n\n By holding shift and pressing multiple countries you can view how Covid fear and Covid statistics vary among different countries. To learn more about Interesting Trends, the Fear Index and Variable Selection, please view the descriptions below. The graphs start at week 11 of the year 2020, which corresponds to the data March 9, 2020.")

repeated_data = Your_Covid_Data()
world_data = Your_World_Data()


my_selector = alt.selection_multi(fields = ["properties.location"],init = [{"properties.location": "United States"},{"properties.location": "India"}])

chart = alt.Chart(repeated_data,title = "Percentage of Elderly and GDP for each Country").mark_circle().encode(
    x = alt.X("properties.gdp_per_capita:Q", title='GDP per Capita'),
    y=alt.Y("properties.aged_65_older:Q", title='Percentage of Elderly'),
    # color=alt.condition(my_selector, alt.Color("properties.Continent:N",title = "Continent"), alt.value('lightgray')),
    color=alt.condition(my_selector, alt.Color("properties.location:N",title = "Countries"), alt.value('lightgray')),
    opacity = alt.condition(my_selector, alt.value(1.0), alt.value(0.15)),
    size=alt.Size("properties.population:Q",scale=alt.Scale(domain=(-400000000, 1850000000)), legend=None),
    tooltip=alt.Tooltip('properties.location:N',title = "Country")
    
).add_selection(
    my_selector
).properties(
    width=300,
    height=200
)


one_country = alt.Chart(repeated_data).mark_geoshape().encode(
    color= alt.condition(
        # my_selector, alt.Color("properties.Continent:N"), alt.value('gray')
        my_selector, alt.Color("properties.location:N",title = "Countries",scale=alt.Scale(scheme='tableau20'),legend = alt.Legend(orient="top",columns=5, labelOpacity=0.8, columnPadding=67,clipHeight=12)), alt.value('gray')
    ),
    opacity = alt.condition(my_selector, alt.value(1.0), alt.value(0.15)),
    tooltip=alt.Tooltip('properties.location:N',title = "Country")
).properties(
    width=375,
    height=200
).add_selection(
    my_selector
)

world = alt.Chart(world_data).mark_geoshape().encode(
    color=alt.value('lightgray'),
    tooltip=alt.Tooltip('properties.location:N',title = "Country")
).properties( 
    width=375,
    height=200
)


boundaries = alt.Chart(world_data, title='World Map').mark_geoshape(
    stroke='white',
    strokeWidth=1,
    fill=None
)


fear = alt.Chart(repeated_data, title='Twitter Fear over Time').mark_line().encode(
    x=alt.X('properties.week:O',title= "Week"),
    y=alt.Y('properties.fear_percentage:Q',title = "Fear Index"),
    color= alt.Color("properties.location:N", legend = alt.Legend())
    # y=alt.Y('mean(properties.fear_percentage):Q',title = "Fear Index"),
    # color= alt.value("gray")
).transform_filter(
    my_selector
).properties(
    width = 700,
    height = 150
)

cases = alt.Chart(repeated_data, title='Covid Infections over Time').mark_line().encode(
    x=alt.X('properties.week:O', title = "Week"),
    y=alt.Y('properties.new_cases_per_million:Q',title="New Cases per Million"),
    color= alt.Color("properties.location:N")
).transform_filter(
    my_selector
).properties(
    width = 700,
    height = 150
)

deaths = alt.Chart(repeated_data, title='Covid Deaths over Time').mark_line().encode(
    x=alt.X('properties.week:O', title = "Week"),
    y=alt.Y('properties.new_deaths_per_million:Q',title="New Deaths per Million"),
    color= alt.Color("properties.location:N")
).transform_filter(
    my_selector
).properties(
    width = 700,
    height = 150
)


st.write((chart | world + one_country  + boundaries) & fear & cases  & deaths)

expander = st.beta_expander("Interesting Trends")
expander.write("Have a look at how the Fear Index precedes the number of infections in first world countries. In most of these countries, the fear index halves by the time Covid cases hit their peak. Do we just become bored when the pandemic is most deadly? \n\nNotice how the death rate is very low in UAE compared to in Ireland; perhaps the lower percentage of elderly could explain this. \n\n Have a look at Covid infections and deaths in third world countries. Could a lack of testing explain the low cases and deaths even when fear is high? \n\n Maybe look at how similar the fear and Covid trends are within countries of the same continent, maybe shared cultural and geographical aspects could be the reason?")

expander = st.beta_expander("What is the Fear Index")
expander.write("The Fear Index is the percentage of Covid-related tweets that contain keywords related to fear. These keywords include conjugations of synonyms of 'fear' such as 'scared', 'afraid' and 'nervous'. \n\n To collect the Tweets, we utilize the publically available Harvard 'Coronavirus Tweet Ids' dataset.")

expander = st.beta_expander("Variable Selection")
expander.write("The variables GDP per Capita and percentage of population above 65 were chosen because our intuition would tell us that our Covid fears should increase as these variables increase. This is because Covid is more dangerous when hospital beds cannot be afforded or when it affects a member of the elderly.")
