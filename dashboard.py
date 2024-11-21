import streamlit as st
import pandas as pd

st.header("2024 AHI 507 Streamlit Example")
st.subheader("We are going to go through a couple different examples of loading and visualization information into this dashboard")

st.text("""In this streamlit dashboard, we are going to focus on some recently released school learning modalities data from the NCES, for the years of 2021.""")

# ## https://healthdata.gov/National/School-Learning-Modalities-2020-2021/a8v3-a3m3/about_data
df = pd.read_csv("https://healthdata.gov/resource/a8v3-a3m3.csv?$limit=50000") ## first 1k 

## data cleaning 
df['week_recoded'] = pd.to_datetime(df['week'])
df['zip_code'] = df['zip_code'].astype(str)

df['week'].value_counts()

## box to show how many rows and columns of data we have: 
col1, col2, col3 = st.columns(3)
col1.metric("Columns", df.shape[1]) 
col2.metric("Rows", len(df))
col3.metric("Number of unique districts/schools:", df['district_name'].nunique())

## exposing first 1k of NCES 20-21 data
st.dataframe(df)



table = pd.pivot_table(df, values='student_count', index=['week'],
                       columns=['learning_modality'], aggfunc="sum")

table = table.reset_index()
table.columns

## line chart by week 
st.bar_chart(
    table,
    x="week",
    y="Hybrid",
)

st.bar_chart(
    table,
    x="week",
    y="In Person",
)

st.bar_chart(
    table,
    x="week",
    y="Remote",
)

# Description
st.markdown("### Insights")
st.write("The bar chart below shows the distribution of learning modalities across schools.")

# Visualization (Bar Chart Example)
import matplotlib.pyplot as plt
modality_counts = df['learning_modality'].value_counts()
fig, ax = plt.subplots()
modality_counts.plot(kind='bar', ax=ax)
ax.set_title('Distribution of Learning Modalities')
st.pyplot(fig)

# Description
st.markdown("### Filter Data by District")
st.write("Use the dropdown menu below to select a specific district. Once selected, the table will display only the data for that district.")

# Add interactive dropdown to filter by district
district = st.selectbox('Select a District', df['district_name'].unique())
filtered_df = df[df['district_name'] == district]

# Display filtered data
st.dataframe(filtered_df)
