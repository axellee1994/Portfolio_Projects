#!/usr/bin/env python
# coding: utf-8

# In[27]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import os


# In[5]:


files = os.listdir(r'C:\Users\Axel\Data Analysis with Python\Covid-19')
files


# In[6]:


def read_data(path, filename):
    return pd.read_csv(path + '/' + filename)


# In[11]:


path = 'C:/Users/Axel/Data Analysis with Python/Covid-19'
world_data = read_data(path,'worldometer_data.csv')
world_data


# In[13]:


world_data.head(5)


# In[16]:


day_wise = read_data(path, files[2])
day_wise


# In[17]:


full_grouped = read_data(path, files[3])
full_grouped


# In[19]:


usa_country_wise = read_data(path, files[4])
usa_country_wise


# In[20]:


province_data = read_data(path, files[1])
province_data


# In[21]:


world_data.columns


# In[28]:


columns = ['TotalCases','TotalDeaths','TotalRecovered','ActiveCases']
for i in columns:
    fig = px.treemap(world_data.iloc[0:20], values=i, path=['Country/Region'], title='Treemap representation of different countries with respect to their {}'.format(i))
    fig.show()


# In[30]:


day_wise.head()


# In[31]:


day_wise.columns


# In[33]:


px.line(day_wise,x = 'Date', y = ['Confirmed','Deaths','Recovered','Active'], title = 'COVID cases with respect to date',template='plotly_dark')


# In[35]:


world_data.head()


# In[39]:


population_test_ratio = world_data['Population'] / world_data['TotalTests'].iloc[0:20]


# In[48]:


fig = px.bar(world_data.iloc[0:20], x = 'Country/Region', y = population_test_ratio[0:20], color = 'Country/Region', title = 'Population to test done ratio',template='plotly_dark')
fig.show()


# In[41]:


world_data.columns


# In[49]:


fig = px.bar(world_data.iloc[0:20], x = 'Country/Region', y = ['Serious,Critical','TotalDeaths','TotalRecovered','ActiveCases','TotalCases'], title = 'Top 20 countries that are badly affected by COVID',template='plotly_dark')
fig.show()


# In[52]:


fig = px.bar(world_data.iloc[0:20], y='Country/Region',x='TotalCases',text = 'TotalCases', color = 'TotalCases')
fig.update_layout(template = 'plotly_dark', title_text = 'Top 20 countries of total confirmed cases')
fig.show()


# In[53]:


world_data.sort_values(by = 'TotalDeaths', ascending = False)


# In[55]:


fig = px.bar((world_data.sort_values(by = 'TotalDeaths', ascending = False).iloc[0:20]), y='Country/Region',x='TotalDeaths',text = 'TotalDeaths', color = 'TotalDeaths')
fig.update_layout(template = 'plotly_dark', title_text = 'Top 20 countries of total death cases')
fig.show()


# In[56]:


world_data.sort_values(by = 'ActiveCases', ascending = False)


# In[58]:


fig = px.bar((world_data.sort_values(by = 'ActiveCases', ascending = False).iloc[0:20]), y='Country/Region',x='ActiveCases',text = 'ActiveCases', color = 'ActiveCases')
fig.update_layout(template = 'plotly_dark', title_text = 'Top 20 countries of total active cases')
fig.show()


# In[91]:


fig = px.bar((world_data.sort_values(by = 'TotalRecovered', ascending = False).iloc[0:20]), y='Country/Region',x='TotalRecovered',text = 'TotalRecovered', color = 'TotalRecovered')
fig.update_layout(template = 'plotly_dark', title_text = 'Top 20 countries of total recovered cases')
fig.show()


# In[92]:


def plot_bar_chart(df, x, y, title):
    df = world_data.sort_values(by=x, ascending = False).iloc[0:20]
    fig = px.bar(df, x=x, y=y, color=x, text=y, title=title, template='plotly_dark')
    return fig.show()


# In[93]:


plot_bar_chart(world_data, 'TotalRecovered', 'Country/Region','Top 20 countries of total recovered cases')


# In[95]:


def stack_bar_chart(df,x,y,title):
    df = world_data.iloc[0:20]
    fig = px.bar(df, x=x,y=y,title=title, template = 'plotly_dark')
    return fig.show()


# In[97]:


stack_bar_chart(world_data, 'Country/Region', ['Serious,Critical','TotalDeaths','TotalRecovered','ActiveCases','TotalCases'], 'Top 20 countries that are badly affected by COVID')


# In[98]:


world_data.head()


# In[101]:


labels = world_data[0:15]['Country/Region'].values
cases = ['TotalCases','TotalDeaths','TotalRecovered','ActiveCases']
for i in cases:
    fig = px.pie(world_data.iloc[0:15],values=i,names = labels, hole = 0.3, title = '{} recorded with respect to WHO region of 15 worst affected countries'.format(i))
    fig.show()


# In[102]:


world_data.head()


# In[104]:


death_to_confirmed_ratio = world_data['TotalDeaths'] / world_data['TotalCases']
death_to_confirmed_ratio


# In[106]:


fig = px.bar(world_data, x='Country/Region', y=death_to_confirmed_ratio, title = 'Death to confirmed ratio of worst affected countries')
fig.show()


# In[107]:


death_to_recovered_ratio = world_data['TotalDeaths'] / world_data['TotalRecovered']
death_to_recovered_ratio


# In[108]:


fig = px.bar(world_data, x='Country/Region', y=death_to_recovered_ratio, title = 'Death to recovered ratio of worst affected countries')
fig.show()


# In[109]:


test_to_confirmed_ratio = world_data['TotalTests'] / world_data['TotalCases']
test_to_confirmed_ratio


# In[110]:


fig = px.bar(world_data, x='Country/Region', y=test_to_confirmed_ratio, title = 'Test to confirmed ratio of worst affected countries')
fig.show()


# In[111]:


serious_to_deaths_ratio = world_data['Serious,Critical'] / world_data['TotalDeaths']
serious_to_deaths_ratio


# In[113]:


fig = px.bar(world_data, x='Country/Region', y=serious_to_deaths_ratio, title = 'Serious to deaths ratio of worst affected countries')
fig.show()


# In[114]:


world_data.head()


# In[124]:


from plotly.subplots import make_subplots
import plotly.graph_objects as go


# In[117]:


full_grouped.head()


# In[132]:


def country_visualization(df,country):
    data = df[df['Country/Region'] == country]
    data2 = data.loc[:,['Date','Confirmed','Deaths','Recovered','Active']]
    fig = make_subplots(rows=1, cols=4, subplot_titles=('Confirmed', 'Active', 'Recovered', 'Deaths'))

    fig.add_trace(go.Scatter(name='Confirmed', x=data2['Date'], y=data2['Confirmed']), row=1, col=1)

    fig.add_trace(go.Scatter(name='Deaths', x=data2['Date'], y=data2['Deaths']), row=1, col=2)

    fig.add_trace(go.Scatter(name='Recovered', x=data2['Date'], y=data2['Recovered']), row=1, col=3)

    fig.add_trace(go.Scatter(name='Active', x=data2['Date'], y=data2['Active']), row=1, col=4)

    fig.update_layout(height=600, width=1000, title_text='Date vs Recorded cases of {}'.format(country), template='plotly_dark')
    fig.show()


# In[134]:


country_visualization(full_grouped,'Singapore')

