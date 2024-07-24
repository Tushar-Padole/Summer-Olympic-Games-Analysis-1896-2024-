''' Summer Olympic Games Analysis(1896-2024)'''
import pandas as pd
import numpy as np
import streamlit as st
import preprocessor,helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

df = pd.read_csv('data/all_athlete_games.csv')
region_df = pd.read_csv('data/all_regions.csv')

df = preprocessor.preprocess(df,region_df)

st.sidebar.title("Olympic Analysis")
st.sidebar.image("Olympic_flag.svg.png")
user_menu = st.sidebar.radio('Select an Option',
                 ('Medal Tally','Overall Analysis','Country-wise Analysis','Athlete-wise Analysis'))

#st.dataframe(df)

if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years,countrys = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year",years)
    selected_country = st.sidebar.selectbox("Select Country",countrys)

    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)
    
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Tally")
    elif selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " Overall Performance")
    elif selected_year != 'Overall' and selected_country == 'Overall':
        st.title("Medal Tally in " + str(selected_year) + " Olympics")
    elif selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " Performance in " + str(selected_year) + " Olympics")
    
    st.table(medal_tally)

if user_menu == 'Overall Analysis':
    edition = df['Year'].unique().shape[0] 
    cities = df['City'].unique().shape[0] 
    events = df['Event'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['Region'].unique().shape[0]

    st.title("Top Statistics")
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(edition)
    with col1:
        st.header("Hosts")
        st.title(cities)
    with col1:
        st.header("Sports")
        st.title(sports)

    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col1:
        st.header("Athletes")
        st.title(athletes)
    with col1:
        st.header("Nations")
        st.title(nations)

    nations_over_time = helper.data_over_time(df,"Region")
    #st.table(nations_over_time)
    fig = px.line(nations_over_time, x='Edition', y="Region")
    st.title("Participating Nations over the years")
    st.plotly_chart(fig)

    event_over_time = helper.data_over_time(df,"Event")
    fig = px.line(event_over_time, x='Edition', y="Event")
    st.title("Event over the years")
    st.plotly_chart(fig)

    athlete_over_time = helper.data_over_time(df,"Name")
    fig = px.line(athlete_over_time, x='Edition', y="Name")
    st.title("Athlete over the years")
    st.plotly_chart(fig)

    st.title("No. of Events over time(Every Sport)")
    fig,ax = plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year','Sport','Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport',columns='Year',values='Event',aggfunc='count').fillna(0).astype("int"),annot=True)
    st.pyplot(fig)

    st.title("Most Successful Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

    selected_sport = st.selectbox('Select of Sport',sport_list)
    x = helper.most_successful(df,selected_sport)
    st.table(x)

if user_menu == 'Country-wise Analysis':

    st.sidebar.title('Country-wise Analysis')

    country_list = df['Region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select a Country',country_list)

    country_df = helper.year_wise_medal_tally(df,selected_country)
    fig = px.line(country_df, x='Year', y="Medal")
    st.title(selected_country + " Medal tally over the years")
    st.plotly_chart(fig)

    st.title(selected_country + " excels in the following sport")
    pivot_table = helper.country_envent_heatmap(df,selected_country)
    fig,ax = plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year','Sport','Event'])
    ax = sns.heatmap(pivot_table,annot=True)
    st.pyplot(fig)

    st.title("Top 10 athletes of " + selected_country)
    top10_df = helper.most_successful_country_wise(df,selected_country)
    st.table(top10_df)

if user_menu == 'Athlete-wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name','Region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1,x2,x3,x4],['Overall Age','Gold medalist','Silver medalist','Bronze medalist'],show_hist=False,show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)






    st.title("Male VS Female Participation Over the Years")
    final = helper.male_vs_female(df)
    fig = px.line(final,x="Year",y=["Male","Female"])
    fig.update_layout(autosize=False,width=1000,height=600)
    st.plotly_chart(fig)


''' 
    x = []
    name = []
    all_sports = athlete_df['Sport'].unique().tolist()
    for sport in all_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x,name,show_hist=False,show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title("Distribution of Age WRT Sports(Gold Medalist)")
    st.plotly_chart(fig)
'''