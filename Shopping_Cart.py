
import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st

st.set_page_config(layout='wide',page_title='Shopping_Cart_EDA.py')
st.markdown("<h1 style='text-align: center; color: white;'>Shopping_Cart_EDA</h1>", unsafe_allow_html=True)
st.image('10247.jpg')

df=pd.read_csv('Shopping Cart Project.csv',index_col=0)
df['order_date']=pd.to_datetime(df['order_date'])
df['delivery_date']=pd.to_datetime(df['delivery_date'])


page=st.sidebar.radio('pages',['🏠 Home', '📊 KPI Dashboard', '📢 Marketing Report' ,'🛠️ Made by'])

if( page =='🏠 Home'):
    st.subheader("Welcome to the Home Page")
    st.subheader("data frame overview")
    st.dataframe(df)
elif( page =='📊 KPI Dashboard'):

    # 1. Total Sales Revenue: Sum of all total_price
    total_sales_revenue = df['total_price'].sum()
    # 2. Total Number of Orders: Count of unique order_id
    total_orders = df['order_id'].nunique()
    # 3. Average Order Value (AOV): Total revenue divided by the number of unique orders
    order_revenue = df.groupby('order_id')['total_price'].sum()
    average_order_value = order_revenue.mean()
    # 4. Total Units Sold: Sum of units sold (using the 'stock' column based on data inspection)
    total_units_sold = df['stock'].sum()
    # 5. Average Delivery Duration: Mean of the delivery_duration column
    average_delivery_duration = df['delivery_duration'].mean()
# --- 6. Most Popular Product Type (by Units Sold) ---
    product_units = df.groupby('product_type')['stock'].sum()
    most_popular_type = product_units.idxmax()
    most_popular_units = product_units.max()
    most_popular_percentage = (most_popular_units / total_units_sold) * 100


    col1, col2, col3 = st.columns(3)

    col1.metric("💰 Total Sales Revenue", f"${total_sales_revenue:,.2f}")

    col2.metric("🛒 Total Orders", total_orders)

    col3.metric("📦 Total Units Sold", total_units_sold)

    col4, col5,col6 = st.columns(3)

    col4.metric("📏 Avg Order Value (AOV)", f"${average_order_value:,.2f}")

    col5.metric("⏱ Avg Delivery Duration (days)", f"{average_delivery_duration:.1f}")

    col6.metric("🔥 Most Popular Product %",f"{most_popular_percentage:.2f}%")

    st.header('   ')
    st.header('   ')


    st.header('📈 revenue trend over time')
    sorted_df=df.sort_values(by='order_date')
    revenue_over_time=sorted_df.groupby('order_date')['total_price'].sum().reset_index()
    st.plotly_chart(px.line(data_frame=revenue_over_time,x='order_date',y='total_price'))



    st.header('top states with the highest revenue')
    st.plotly_chart(px.bar(data_frame=df,x='state',y='total_price',labels={'state': 'State ', 'total_price': 'Revenue'}))

elif(page=='📢 Marketing Report'):


    start = pd.to_datetime(st.sidebar.date_input('Start date',min_value=df['order_date'].min(),max_value=df['order_date'].max(),value=df['order_date'].min()))

    end = pd.to_datetime(st.sidebar.date_input('End date',min_value=df['order_date'].min(),max_value=df['order_date'].max(),value=df['order_date'].max()))

    filtered_df = df[(df['order_date'] >= start) & (df['order_date'] <= end)]



    state_filter=st.sidebar.selectbox('select state',df.state.unique())
    filtered_df=df[df['state']==state_filter]

    st.dataframe(filtered_df)


    st.header(f'📈 revenue trend from {start} to {end} in {state_filter}')
    sorted_df=filtered_df.sort_values(by='order_date')
    revenue_over_time=sorted_df.groupby('order_date')['total_price'].sum().reset_index()
    st.plotly_chart(px.line(data_frame=revenue_over_time,x='order_date',y='total_price'))

elif (page=='🛠️ Made by'):
    st.markdown(
        """
        <div style='text-align: center; margin-top: 50px; color: gray; font-size: 16px;'>
            Made with ❤️ by <strong>Mohamed Shabaan </strong>
        </div>
        """,
    unsafe_allow_html=True
)



