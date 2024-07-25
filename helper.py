import numpy as np

def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=['Team','NOC','Year','Season','City','Sport','Event','Medal'])
    medal_tally = medal_tally.groupby('Region').sum()[['Bronze','Gold','Silver']].sort_values('Gold',ascending=False).reset_index()
    medal_tally = medal_tally.groupby('Region').sum()[['Bronze','Gold','Silver']].sort_values('Gold',ascending=False).reset_index()
    medal_tally['total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
    
    return medal_tally

def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0,'Overall')

    countrys = np.unique(df['Region'].dropna().values).tolist()
    countrys.sort()
    countrys.insert(0,'Overall')

    return years,countrys

def fetch_medal_tally(df,year,country):
    medal_df = df.drop_duplicates(subset=['Team','NOC','Year','Season','City','Sport','Event','Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        temp_df = medal_df[medal_df['Region'] == country]
        flag = 1
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == year]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == year) & (medal_df['Region'] == country)]
        
    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('Region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()       
    
    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']
    
    return x

def data_over_time(df,col):
    temp_data_over_time = df.drop_duplicates(['Year',col])['Year'].value_counts().reset_index().sort_values('Year')
    temp_data_over_time.rename(columns={'count':'Edition','Year':col},inplace=True)
    return temp_data_over_time   

def most_successful(df, sport):
    temp_df = df.dropna(subset=['Medal'])
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]
        
    # Ensure 'Name' columns in both dataframes are of the same type (string)
    temp_df['Name'] = temp_df['Name'].astype(str)
    df['Name'] = df['Name'].astype(str)
    
    x = temp_df['Name'].value_counts().reset_index().head(10)
    x.columns = ['Name', 'count']
    
    # Merge with the original dataframe
    merged_df = x.merge(df, on='Name', how='left')[['Name', 'count', 'Sport', 'Region']].drop_duplicates('Name')
    merged_df.rename(columns={'count': 'Medal'}, inplace=True)
    return merged_df

def year_wise_medal_tally(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team','NOC','Year','City','Sport','Event','Medal'],inplace=True)

    new_df = temp_df[temp_df['Region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index() 
    return final_df 

def country_envent_heatmap(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team','NOC','Year','City','Sport','Event','Medal'],inplace=True)

    new_df = temp_df[temp_df['Region'] == country]
    pivot_table = new_df.pivot_table(index='Sport',columns='Year',values='Medal',aggfunc='count').fillna(0)
    return pivot_table

def most_successful_country_wise(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['Region'] == country]

    temp_df['Name'] = temp_df['Name'].astype(str)
    df['Name'] = df['Name'].astype(str)

    x = temp_df['Name'].value_counts().reset_index().head(10)
    x.columns = ['Name', 'count']
    
    merged_df = x.merge(df, on='Name', how='left')[['Name', 'count', 'Sport']].drop_duplicates('Name')
    merged_df.rename(columns={'count': 'Medal'}, inplace=True)
    return merged_df
    
def male_vs_female(df):
    athlete_df = df.drop_duplicates(subset=['Name','Region'])

    male = athlete_df[athlete_df['Gender'] == 'Male'].groupby('Year').count()['Name'].reset_index()
    female = athlete_df[athlete_df['Gender'] == 'Female'].groupby('Year').count()['Name'].reset_index()

    final = male.merge(female,on='Year',how='left')
    final.rename(columns={'Name_x':'Male','Name_y':'Female'},inplace=True)

    final.fillna(0,inplace=True)

    return final
