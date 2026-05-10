import streamlit as st
import pandas as pd
import plotly.express as px
st.markdown("""
<style>

/* Sidebar only */
section[data-testid="stSidebar"] {
    font-family: "Times New Roman", serif;
    font-size: 12px;
}

/* Sidebar widget labels ONLY */
section[data-testid="stSidebar"] label {
    font-family: "Times New Roman", serif !important;
    font-size: 12px !important;
    color: red !important;
}

/* Sidebar dropdown / multiselect text */
section[data-testid="stSidebar"] div[data-baseweb="select"] {
    font-family: "Times New Roman", serif !important;
    font-size: 12px !important;
}

</style>
""", unsafe_allow_html=True)
st.set_page_config(page_title='Airline Losses Dashboard')
st.markdown(
    '<div class="custom-header">🛰 Interactive Losses for Airline due to Iran-USA War Dashboard</div>',
    unsafe_allow_html=True
)
df = pd.read_csv('airline_losses.csv')

st.sidebar.header('Filter Data')

country_filter = st.sidebar.multiselect(
    'Select Country',
    options=df['country'].unique(),
    default=df['country'].unique()
)

airline_filter = st.sidebar.multiselect(
    'Select Airline',
    options=df['airline'].unique(),
    default=df['airline'].unique()
)

filtered_df = df[
    (df['country'].isin(country_filter)) &
    (df['airline'].isin(airline_filter))
]
col1, col2 = st.columns(2)

with col1:
    total_losses = filtered_df['estimated_loss_usd'].sum()
    st.metric('Total Loss', f'{total_losses:.2f}')

with col2:
    average_losses = filtered_df['estimated_loss_usd'].mean()
    st.metric('Average Loss', f'{average_losses:.2f}')
tab1, tab2 = st.tabs(['✈ Loss by Airline', '🌍 Loss by Country'])

with tab1:
    st.subheader('Loss by Airline')

    airline_data = filtered_df.groupby('airline')['estimated_loss_usd'].sum().reset_index()
    airline_data.columns = ['airline', 'Total Loss']

    fig1 = px.bar(
        airline_data,
        x='airline',
        y='Total Loss',
        color='airline',
        text='Total Loss'
    )

    st.plotly_chart(fig1)

with tab2:
    st.subheader('Loss by Country')

    country_data = filtered_df.groupby('country')['estimated_loss_usd'].sum().reset_index()
    country_data.columns = ['country', 'Total Loss']

    fig2 = px.pie(
        country_data,
        names='country',
        values='Total Loss',
        title='Losses per region'
    )

    st.plotly_chart(fig2)
st.markdown(f'''
#### Country Selected: {country_filter}
#### Airline Selected: {airline_filter}
''')

