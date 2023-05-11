#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd


# In[2]:


import seaborn as sns
import matplotlib.pyplot as plt


# In[3]:


uber_15 = pd.read_csv('C:/Users/Axel/Data Analysis with Python/Uber Analysis/uber-raw-data-janjune-15.csv', encoding='utf-8')


# In[4]:


uber_15.head(2)


# In[5]:


uber_15.shape


# In[6]:


uber_15.duplicated().sum()


# In[7]:


uber_15.drop_duplicates(inplace = True)


# In[8]:


uber_15.shape


# In[9]:


uber_15.dtypes


# In[10]:


uber_15['Pickup_date'] = pd.to_datetime(uber_15['Pickup_date'],format = '%Y-%m-%d %H:%M:%S')


# In[11]:


uber_15['Pickup_date'].dtype


# In[12]:


uber_15['Pickup_date']


# In[13]:


uber_15['month'] = uber_15['Pickup_date'].dt.month


# In[14]:


uber_15['month'].value_counts().plot(kind = 'bar')


# In[15]:


uber_15['weekday'] = uber_15['Pickup_date'].dt.day_name()
uber_15['day'] = uber_15['Pickup_date'].dt.day
uber_15['hour'] = uber_15['Pickup_date'].dt.hour
uber_15['month'] = uber_15['Pickup_date'].dt.month
uber_15['minute'] = uber_15['Pickup_date'].dt.minute


# In[16]:


uber_15.head(2)


# In[17]:


temp = uber_15.groupby((['month','weekday']),as_index = False).size()
temp.head()


# In[18]:


type(uber_15.groupby(['month','weekday']).size())


# In[19]:


temp['month'].unique()


# In[20]:


dict_month = {1:'Jan',2:'Feb',3:'March',4:'April',5:'May',6:'June'}


# In[21]:


temp['month'] = temp['month'].map(dict_month)


# In[22]:


temp


# In[23]:


plt.figure(figsize = (12,8))
sns.barplot(x='month',y='size',hue ='weekday', data=temp)


# In[24]:


uber_15.groupby(['weekday','hour']).count()


# In[25]:


summary = uber_15.groupby((['weekday','hour']),as_index = False).size()
summary


# In[26]:


plt.figure(figsize =(12,8))
sns.pointplot(x='hour',y='size',hue='weekday',data = summary)


# In[27]:


uber_15.head(2)


# In[28]:


uber_foil =pd.read_csv(r'C:\Users\Axel\Data Analysis with Python\Uber Analysis\Uber-Jan-Feb-FOIL.csv')
uber_foil


# In[29]:


import chart_studio
import plotly


# In[30]:


pip install chart_studio


# In[31]:


import chart_studio.plotly as py


# In[32]:


import plotly.graph_objs as go
import plotly.express as px


# In[33]:


from plotly.offline import download_plotlyjs, plot, iplot, init_notebook_mode
init_notebook_mode(connected=True)


# In[34]:


px.box(x='dispatching_base_number', y='active_vehicles', data_frame =uber_foil)


# In[35]:


px.violin(x='dispatching_base_number', y='active_vehicles', data_frame =uber_foil)


# In[36]:


import os


# In[37]:


os.listdr(r'C:\Users\Axel\Data Analysis with Python\Uber Analysis')


# In[42]:


import os

files = os.listdir(r'C:\Users\Axel\Data Analysis with Python\Uber Analysis')[-7:]
files


# In[43]:


files.remove('uber-raw-data-janjune-15.csv')


# In[44]:


files


# In[45]:


path = 'C:\\Users\\Axel\\Data Analysis with Python\\Uber Analysis'


final = pd.DataFrame()
for file in files:
    current_df = pd.read_csv(path + '/' + file, encoding ='utf8')
    final = pd.concat([current_df,final])


# In[46]:


final.shape


# In[47]:


final.head()


# In[48]:


final.duplicated().sum()


# In[49]:


final.drop_duplicates(inplace = True)


# In[50]:


final.shape


# In[51]:


rush_uber = final.groupby((['Lat','Lon']),as_index = False).size()
rush_uber


# In[52]:


get_ipython().system('pip install folium')


# In[53]:


import folium 


# In[54]:


basemap = folium.Map()
basemap


# In[55]:


from folium.plugins import HeatMap


# In[56]:


HeatMap(rush_uber).add_to(basemap)
HeatMap


# In[57]:


basemap


# In[58]:


final.tail(5)


# In[64]:


final['Date/Time'] = pd.to_datetime(final['Date/Time'], format='%m/%d/%Y %H:%M:%S')


# In[65]:


final['weekday'] = final['Date/Time'].dt.day
final['hour'] = final['Date/Time'].dt.hour 


# In[67]:


final.head(3)


# In[68]:


final.groupby(['weekday','hour']).size().unstack()


# In[69]:


pivot = final.groupby(['weekday','hour']).size().unstack()


# In[70]:


pivot


# In[71]:


pivot.style.background_gradient()


# In[73]:


def gen_pivot_table(df,col1,col2):
    pivot = df.groupby([col1,col2]).size().unstack()
    return pivot.style.background_gradient()


# In[75]:


gen_pivot_table(final,'weekday','hour')


# In[81]:


img_path = 'gen_pivot_table.png'
pivot_table.to_image().save(img_path)

