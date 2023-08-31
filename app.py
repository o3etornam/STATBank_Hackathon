import streamlit as st
import plotly.express as px
import pandas as pd

import plotly.graph_objects as go

st.set_page_config(layout='wide', initial_sidebar_state='expanded')
st.title(f':bar_chart: Dashboard of the distribtion of Information Technology tools and Internet Usage in Ghana')
st.markdown('<style>div.block-container{padding-top:1rem;}, *{margin:0}<\style>', unsafe_allow_html= True)

laptop = pd.read_csv('laptop.csv')
phone = pd.read_csv('smart and non smart.csv')
usedInternet = pd.read_csv('Usedlaptop.csv')

datasets = st.sidebar.selectbox('Pick a dataset to explore', ['Laptop', 'Phone', 'Internet Usage',])
link = {'Laptop': laptop, 'Phone': phone, 'Internet Usage': usedInternet}

titles = [('Laptop', 'Ownership of Laptops'), ('Phone','Type of Phone used'), ('Internet Usage', 'internet Usage in the last six months')]

for i,v in titles:
   if datasets == i:
      title = v

dataset = link[datasets]

w_variable = dataset.columns[0]

if datasets == 'Phone':
   dataset =  dataset.loc[dataset[w_variable] != 'None']

## own laptop
df = dataset.groupby([w_variable]).sum(numeric_only=True).sum(axis = 1).reset_index()
df = df.rename(columns={0: 'count'})



### Regions
region_df = dataset.groupby([w_variable,'Geographic_Area']).sum(numeric_only=True).sum(axis = 1).reset_index()
region_df = region_df.loc[region_df['Geographic_Area'] != 'Ghana',:]
region_df = region_df.rename(columns={0: 'count'})



#### ghana
ghana_df = dataset.groupby([w_variable,'Geographic_Area']).sum(numeric_only=True).sum(axis = 1).reset_index()
ghana_df = ghana_df.loc[ghana_df['Geographic_Area'] == 'Ghana',:]
ghana_df = ghana_df.rename(columns={0: 'count'})

st.sidebar.header('Dashboard `Team Datageniuses ❤️`')
region = st.sidebar.multiselect('Visualize a region', region_df['Geographic_Area'].unique())
region_sub = region_df.loc[region_df['Geographic_Area'].isin(region),:]

gh_fig = px.bar(ghana_df, x='Geographic_Area', y='count', color=w_variable, barmode='group', title=f'Grouped Bar Plot showing {title} across regions in Ghana')

if region:
    selected_region = ', '.join(region)  # Join selected regions with a comma
    sub_fig = px.bar(region_sub, x='Geographic_Area', y='count', color=w_variable, barmode='group', title=f'{title} in the {selected_region} region')
    st.plotly_chart(sub_fig, use_container_width=True)
else:
    st.plotly_chart(gh_fig, use_container_width=True)


#### sex
sex_df = dataset.groupby([w_variable,'Sex']).sum(numeric_only=True).sum(axis = 1).reset_index()
sex_df = sex_df.rename(columns={0: 'count'})

col1, col2 = st.columns((2))
with col1:
    sex_fig = px.bar(sex_df, y='Sex', x='count', color=w_variable, barmode='group', title='Ownership of Laptop Across Gender')
    st.plotly_chart(sex_fig, use_container_width=True, height=400)  # Adjust the height as needed


#### education
edu_df = dataset.groupby([w_variable,'Education']).sum(numeric_only=True).sum(axis = 1).reset_index()
edu_df = edu_df.rename(columns={0: 'count'})

with col2:
    edu_fig = px.bar(edu_df, y='Education', x='count', color=w_variable, barmode='group', title='Ownership of Laptop Across Educational Levels')
    st.plotly_chart(edu_fig, use_container_width=True, height=400)


df = dataset.groupby(['Education',w_variable,'Sex']).sum(numeric_only=True).sum(axis = 1).reset_index() 
df = df.rename(columns={0: 'count'})
yes_df = df.loc[df[w_variable] == 'Yes',:]


st.sidebar.subheader('Select a region and owbership to visualize a sankey diagram')

ownership = st.sidebar.selectbox('Visualize a education and gender by ownership', dataset[w_variable].unique())
   
sankey_ownership_df = dataset.loc[dataset[w_variable] == ownership,:]


sankey_df = sankey_ownership_df.groupby(['Geographic_Area','Education',w_variable,'Sex']).sum(numeric_only=True).sum(axis = 1).reset_index()
sankey_df = sankey_df.rename(columns={0: 'count'})

sankey_region = st.sidebar.selectbox('Visualize a region', sankey_df['Geographic_Area'].unique())
sankey_region_df = sankey_df.loc[sankey_df['Geographic_Area'] == sankey_region,:]  
temp = sankey_region_df.groupby(['Sex']).sum(numeric_only=True).sum(axis = 1).reset_index()
temp = temp.rename(columns={0: 'count'})
total_sex = temp['count'].tolist() #female first
auto_values = total_sex + sankey_region_df['count'].tolist()



node_labels = sankey_region_df[w_variable].unique().tolist() + sankey_region_df['Sex'].unique().tolist() + sankey_region_df['Education'].unique().tolist() + sankey_region_df['Education'].unique().tolist()
sankey_fig = go.Figure(data=[go.Sankey(
    node = dict(
      pad = 15,
      thickness = 20,
      line = dict(color = "black", width = 0.5),
      label = node_labels,
      color = "blue"
    ),
    link = dict(
      source = [0,0,1,1,1,1,2,2,2,2],
      target = [1,2,3,4,5,6,7,8,9,10],
      value =  auto_values
  ))])

sankey_fig.update_layout(title_text="Distribution of Education Level Based on Laptop Ownership and Gender", font_size=10)


sunburst_df = dataset.groupby(['Geographic_Area','Education',w_variable,'Sex']).sum(numeric_only=True).sum(axis = 1).reset_index()
sunburst_df = sankey_df.rename(columns={0: 'count'})
sunburst_region_df = sunburst_df.loc[sunburst_df['Geographic_Area'] == sankey_region,:] 

fig_sunburst = px.sunburst(
    sunburst_region_df,
    path=[w_variable, 'Education', 'Sex'],
    values='count'
)


fig_sunburst.update_layout(title='Distribution of Education Level Based on Laptop Ownership and Gender')


col3 , col4 = st.columns((2))

with col3:
  st.plotly_chart(sankey_fig)

with col4:
  st.plotly_chart(fig_sunburst)


def styled_metric(title, value):
    metric_card = f"""
    <div style="border: 1px solid #e0e0e0; border-radius: 10px; padding: 15px; text-align: center; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); margin: 10px; width: %; display: inline-block;">
        <div style="font-size: 18px; font-weight: bold; margin-bottom: 5px;">{title}</div>
        <div style="font-size: 36px; font-weight: bold; color: #0077B6;">{value}</div>
    </div>
    """
    return metric_card

# Example usage
col1, col2, col3, col4, col5, col6, col7, col8, col9, col10= st.columns(10)

# Create styled metric cards
col1.markdown(styled_metric("Females", str(round(auto_values[0]/(auto_values[0] + auto_values[1]) * 100)) + '%'), unsafe_allow_html=True)
col2.markdown(styled_metric("Males", str(round(auto_values[1]/(auto_values[0] + auto_values[1]) * 100))+ '%'), unsafe_allow_html=True)
col3.markdown(styled_metric("Females & Never attended", str(round((auto_values[2]/auto_values[0]) * 100))+ '%'), unsafe_allow_html=True)
col4.markdown(styled_metric("Males & Never attended", str(round((auto_values[3]/auto_values[1]) * 100))+ '%'), unsafe_allow_html=True)
col5.markdown(styled_metric("Females & Primary", str(round((auto_values[4]/auto_values[0]) * 100))+ '%'), unsafe_allow_html=True)
col6.markdown(styled_metric("Males & Primary", str(round((auto_values[5]/auto_values[1]) * 100))+ '%'), unsafe_allow_html=True)
col7.markdown(styled_metric("Females & Secondary", str(round((auto_values[6]/auto_values[0]) * 100))+ '%'), unsafe_allow_html=True)
col8.markdown(styled_metric("Males & Secondary", str(round((auto_values[7]/auto_values[1]) * 100))+ '%'), unsafe_allow_html=True)
col9.markdown(styled_metric("Females & Tertiary", str(round((auto_values[8]/auto_values[0]) * 100))+ '%'), unsafe_allow_html=True)
col10.markdown(styled_metric("Males & Tertiary", str(round((auto_values[9]/auto_values[1]) * 100))+ '%'), unsafe_allow_html=True)

