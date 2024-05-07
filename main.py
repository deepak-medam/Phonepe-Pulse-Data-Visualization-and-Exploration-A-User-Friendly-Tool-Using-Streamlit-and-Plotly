# Importing Libraries
import pandas as pd
import mysql.connector as sql
import streamlit as st
import plotly.express as px
import os
from streamlit_option_menu import option_menu
from PIL import Image

# Setting up page configuration
def setup_page_config():
    """
    This function sets up the Streamlit page configuration.
    """
    icon = Image.open(r"D:\GDrive\2024-25\Projects\Phonepe-Pulse-Data-Visualization-and-Exploration-A-User-Friendly-Tool-Using-Streamlit-and-Plotly\phonepe_logo.png")
    st.set_page_config(page_title="Phonepe Pulse Data Visualization",
                       page_icon=icon,
                       layout="wide",
                       initial_sidebar_state="expanded",
                       menu_items={'About': """# This dashboard app is created by *Deepak*!
                                            Data has been cloned from Phonepe Pulse Github Repo"""})

# Creating connection with MySQL workbench
def create_db_connection():
    """
    This function creates a connection with the MySQL database.
    """
    db_connection = sql.connect(host="localhost",
                                user="root",
                                password="password",
                                database="phonepe_pulse")
    return db_connection

# Creating option menu in the sidebar
def create_option_menu():
    """
    This function creates an option menu in the sidebar.
    """
    with st.sidebar:
        selected = option_menu(
            "Menu",
            options=["Home", "Charts and Insights", "Geo Map and Insights",],
            icons=["house", "graph-up-arrow", "bar-chart-line", "exclamation-circle"],
            menu_icon="menu-button-wide",
            default_index=0,
            styles={
                "nav-link": {
                    "font-size": "20px",
                    "text-align": "left",
                    "margin": "-2px",
                    "--hover-color": "#6F36AD"
                },
                "nav-link-selected": {
                    "background-color": "#C65BCF"
                }
            })
    return selected

# Home
def show_home_page():
    """
    This function displays the content for the Home page.
    """
    st.image(r"D:\GDrive\2024-25\Projects\Phonepe-Pulse-Data-Visualization-and-Exploration-A-User-Friendly-Tool-Using-Streamlit-and-Plotly\pulse.png")
    st.markdown("# :blue[Data Understaing, Visualization and Exploration]")
    col1, col2 = st.columns([3, 2], gap="medium")
    with col1:
        st.write(" ")
        st.write(" ")
        st.markdown("### :blue[Domain :] This project domain is 'Fintech'")
        st.markdown("### :blue[Overview :] This website is created to understand and visualise the phonepe pulse data and gain insights on transactions, number of users, top 10 states, districts, pincodes in transactions cout and amount and which brand has most number of users...etc. Differnt kind of charts, pies and geo maps are used to acheive the objective.")
        st.markdown("### :blue[About me :] My name is Deepak, You can visit my github page at https://github.com/deepak-medam")
    with col2:
        st.image(r"D:\GDrive\2024-25\Projects\Phonepe-Pulse-Data-Visualization-and-Exploration-A-User-Friendly-Tool-Using-Streamlit-and-Plotly\home_img.jpg")

# Top charts
def show_charts_insights(cursor):
    """
    This function displays the Top Charts section.
    
    Args:
        cursor (mysql.connector.cursor): The MySQL cursor object.
    """
    st.markdown("## :blue[Top Charts]")
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
    colum1, colum2 = st.columns([1, 1.5], gap="large")
    with colum1:
        year = st.slider("**Year**", min_value=2021, max_value=2023, value=st.session_state.get("selected_year", 2021), key="year")
        quarter = st.slider("Quarter", min_value=1, max_value=4, value=st.session_state.get("selected_quarter", 1), key="quarter")
    with colum2:
        st.info(
            """
            #### In this section we are going to see various useful insights like :
            - Top 10 State, District, Pincode based on Total number of transaction and Total amount spent using phonepe.
            - Overall ranking on a particular Year and Quarter.
            - Top 10 State, District, Pincode based on Total phonepe users and their app opening frequency.
            - Top 10 mobile brands and its percentage based on the how many people use phonepe.
            """
        )

    # Store selected values in separate session state keys
    st.session_state["selected_year"] = year
    st.session_state["selected_quarter"] = quarter

    # Topchart Transactions
    if Type == "Transactions":
        show_charts_transactions(cursor, st.session_state["selected_year"], st.session_state["selected_quarter"])

    # Topchart users
    if Type == "Users":
        show_charts_users(cursor, st.session_state["selected_year"], st.session_state["selected_quarter"])


def show_charts_transactions(cursor, year, quarter):
    """
    This function displays the Top Charts for Transactions.
    
    Args:
        cursor (mysql.connector.cursor): The MySQL cursor object.
        year (int): The year for which data needs to be displayed.
        quarter (int): The quarter for which data needs to be displayed.
    """
    col1, col2, col3 = st.columns([1, 1, 1], gap="small")

    with col1:
        st.markdown("### :blue[State]")
        cursor.execute(f"select State, sum(Transaction_Count) as Total_Transactions_Count, sum(Transaction_Amount) as Total from aggregate_transactions where year = {year} and quarter = {quarter} group by State order by Total desc limit 10")
        df = pd.DataFrame(cursor.fetchall(), columns=['State', 'Transactions_Count', 'Total_Amount'])
        fig = px.pie(df, values='Total_Amount',
                     names='State',
                     title='Top 10',
                     color_discrete_sequence=px.colors.sequential.Agsunset,
                     hover_data=['Transactions_Count'],
                     labels={'Transactions_Count': 'Transactions_Count'})

        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### :blue[District]")
        cursor.execute(f"select District , sum(Transaction_Count) as Total_Count, sum(Transaction_Amount) as Total from map_transactions where year = {year} and quarter = {quarter} group by District order by Total desc limit 10")
        df = pd.DataFrame(cursor.fetchall(), columns=['District', 'Transactions_Count', 'Total_Amount'])

        fig = px.pie(df, values='Total_Amount',
                     names='District',
                     title='Top 10',
                     color_discrete_sequence=px.colors.sequential.Agsunset,
                     hover_data=['Transactions_Count'],
                     labels={'Transactions_Count': 'Transactions_Count'})

        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)

    with col3:
        st.markdown("### :blue[Pincode]")
        cursor.execute(f"select Pincode, sum(Transaction_Count) as Total_Transactions_Count, sum(Transaction_Amount) as Total from top_transactions_pincode where Year = {year} and Quarter = {quarter} group by Pincode order by Total desc limit 10")
        df = pd.DataFrame(cursor.fetchall(), columns=['Pincode', 'Transactions_Count', 'Total_Amount'])
        fig = px.pie(df, values='Total_Amount',
                     names='Pincode',
                     title='Top 10',
                     color_discrete_sequence=px.colors.sequential.Agsunset,
                     hover_data=['Transactions_Count'],
                     labels={'Transactions_Count': 'Transactions_Count'})

        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)

def show_charts_users(cursor, year, quarter):
    """
    This function displays the Top Charts for Users.
    
    Args:
        cursor (mysql.connector.cursor): The MySQL cursor object.
        year (int): The year for which data needs to be displayed.
        quarter (int): The quarter for which data needs to be displayed.
    """
    col1, col2, col3, col4 = st.columns([2, 2, 2, 2], gap="small")

    with col1:
        st.markdown("### :blue[Brands]")
        cursor.execute(f"select Brand, sum(User_Count) as Total_Count, avg(Percentage)*100 as Avg_Percentage, sum(app_opens) as Total_Appopens from aggregate_users where Year = {year} and Quarter = {quarter} group by Brand order by Total_Count desc limit 10")
        df = pd.DataFrame(cursor.fetchall(), columns=['Brand', 'Total_Users', 'Avg_Percentage', 'Total_Appopens'])
        fig = px.bar(df,
                     title='Top 10',
                     x="Total_Users",
                     y="Brand",
                     orientation='h',
                     color='Avg_Percentage',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### :blue[District]")
        cursor.execute(f"select District, sum(Registered_users) as Total_Users from map_users where Year = {year} and Quarter = {quarter} group by District order by Total_Users desc limit 10")
        df = pd.DataFrame(cursor.fetchall(), columns=['District', 'Total_Users'])
        df.Total_Users = df.Total_Users.astype(float)
        fig = px.bar(df,
                     title='Top 10',
                     x="Total_Users",
                     y="District",
                     orientation='h',
                     color='Total_Users',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig, use_container_width=True)

    with col3:
        st.markdown("### :blue[Pincode]")
        cursor.execute(f"select Pincode, sum(Registered_Users) as Total_Users from top_user_pincode where Year = {year} and Quarter = {quarter} group by Pincode order by Total_Users desc limit 10")
        df = pd.DataFrame(cursor.fetchall(), columns=['Pincode', 'Total_Users'])
        fig = px.pie(df,
                     values='Total_Users',
                     names='Pincode',
                     title='Top 10',
                     color_discrete_sequence=px.colors.sequential.Agsunset,
                     hover_data=['Total_Users'])
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        st.markdown("### :blue[State]")
        cursor.execute(f"select state, sum(Registered_users) as Total_Users, sum(App_opens) as Total_Appopens from aggregate_users where Year = {year} and Quarter = {quarter} group by State order by Total_Users desc limit 10")
        df = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Users', 'Total_Appopens'])
        fig = px.pie(df, values='Total_Users',
                     names='State',
                     title='Top 10',
                     color_discrete_sequence=px.colors.sequential.Agsunset,
                     hover_data=['Total_Appopens'],
                     labels={'Total_Appopens': 'Total_Appopens'})

        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)

# Explore data
def show_geomap_data(cursor, year, quarter):
    """
    This function displays the Explore Data section.
    
    Args:
        cursor (mysql.connector.cursor): The MySQL cursor object.
        year (int): The year for which data needs to be displayed.
        quarter (int): The quarter for which data needs to be displayed.
    """
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
    col1, col2 = st.columns(2)

    year = st.sidebar.slider("**Year**", min_value=2021, max_value=2023, value=st.session_state.get("selected_year", 2021), key="year")
    quarter = st.sidebar.slider("Quarter", min_value=1, max_value=4, value=st.session_state.get("selected_quarter", 1), key="quarter")
    
    # Store selected values in separate session state keys
    st.session_state["selected_year"] = year
    st.session_state["selected_quarter"] = quarter

    # Geo map transactions
    if Type == "Transactions":
        show_geomap_data_transactions(cursor, year, quarter, col1, col2)

    # Geomap users
    if Type == "Users":
        show_geomap_data_users(cursor, year, quarter)

def show_geomap_data_transactions(cursor, year, quarter, col1, col2):
    """
    This function displays the Explore Data section for Transactions.
    
    Args:
        cursor (mysql.connector.cursor): The MySQL cursor object.
        year (int): The year for which data needs to be displayed.
        quarter (int): The quarter for which data needs to be displayed.
        col1 (st.columns): The first column in the Streamlit layout.
        col2 (st.columns): The second column in the Streamlit layout.
    """
    # geo map total transaction amount
    with col1:
        st.markdown("## :violet[Overall State Data - Transactions Amount]")
        cursor.execute(f"select State, sum(Transaction_Count) as Total_Transactions, sum(Transaction_Amount) as Total_amount from map_transactions where Year = {year} and Quarter = {quarter} group by State order by State")
        df1 = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Transactions', 'Total_amount'])
        df2 = pd.read_csv(r'D:\GDrive\2024-25\Projects\Phonepe-Pulse-Data-Visualization-and-Exploration-A-User-Friendly-Tool-Using-Streamlit-and-Plotly\state_names.csv')
        df1.State = df2

        fig = px.choropleth(df1, geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                             featureidkey='properties.ST_NM',
                             locations='State',
                             color='Total_amount',
                             color_continuous_scale='sunset')

        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig, use_container_width=True)

    # Geo map transaction count
    with col2:
        st.markdown("## :violet[Overall State Data - Transactions Count]")
        cursor.execute(f"select State, sum(Transaction_Count) as Total_Transactions, sum(Transaction_Amount) as Total_amount from map_transactions where Year = {year} and Quarter = {quarter} group by State order by State")
        df1 = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Transactions', 'Total_amount'])
        df2 = pd.read_csv(r'D:\GDrive\2024-25\Projects\Phonepe-Pulse-Data-Visualization-and-Exploration-A-User-Friendly-Tool-Using-Streamlit-and-Plotly\state_names.csv')
        df1.Total_Transactions = df1.Total_Transactions.apply(lambda x: int(x) if x < 2**63 else x)  # Handle large integers
        df1.State = df2

        fig = px.choropleth(df1, geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                             featureidkey='properties.ST_NM',
                             locations='State',
                             color='Total_Transactions',
                             color_continuous_scale='sunset')

        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig, use_container_width=True)

    # Bar chart top payement type
    st.markdown("## :violet[Top Payment Type]")
    cursor.execute(f"select Transaction_Type, sum(Transaction_Count) as Total_Transactions, sum(Transaction_Amount) as Total_amount from aggregate_transactions where Year = {year} and Quarter = {quarter} group by Transaction_Type order by Transaction_Type")
    df = pd.DataFrame(cursor.fetchall(), columns=['Transaction_type', 'Total_Transactions', 'Total_amount'])

    fig = px.bar(df,
                 title='Transaction Types vs Total_Transactions',
                 x="Transaction_type",
                 y="Total_Transactions",
                 orientation='v',
                 color='Total_amount',
                 color_continuous_scale=px.colors.sequential.Agsunset)
    st.plotly_chart(fig, use_container_width=False)

    # ar chat total transactions state
    st.markdown("# ")
    st.markdown("# ")
    st.markdown("# ")
    st.markdown("## :violet[Select any State to explore more]")
    selected_state = st.selectbox("",
                                  ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh', 'assam', 'bihar',
                                   'chandigarh', 'chhattisgarh', 'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat', 'haryana',
                                   'himachal-pradesh', 'jammu-&-kashmir', 'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep',
                                   'madhya-pradesh', 'maharashtra', 'manipur', 'meghalaya', 'mizoram',
                                   'nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim',
                                   'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh', 'uttarakhand', 'west-bengal'), index=30)

    cursor.execute(f"select State, District,Year,Quarter, sum(Transaction_Count) as Total_Transactions, sum(Transaction_Amount) as Total_amount from map_transactions where Year = {year} and Quarter = {quarter} and State = '{selected_state}' group by State, District,Year,Quarter order by State,District")

    df1 = pd.DataFrame(cursor.fetchall(), columns=['State', 'District', 'Year', 'Quarter',
                                                   'Total_Transactions', 'Total_amount'])
    fig = px.bar(df1,
                 title=selected_state,
                 x="District",
                 y="Total_Transactions",
                 orientation='v',
                 color='Total_amount',
                 color_continuous_scale=px.colors.sequential.Agsunset)
    st.plotly_chart(fig, use_container_width=True)

def show_geomap_data_users(cursor, year, quarter):
    """
    This function displays the Explore Data section for Users.
    
    Args:
        cursor (mysql.connector.cursor): The MySQL cursor object.
        year (int): The year for which data needs to be displayed.
        quarter (int): The quarter for which data needs to be displayed.
    """
    # app opens total state data
    st.markdown("## :violet[Overall State Data - User App opening frequency]")
    cursor.execute(f"select State, sum(Registered_users) as Total_Users, sum(App_opens) as Total_Appopens from aggregate_users where Year = {year} and Quarter = {quarter} group by State order by State")
    df1 = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Users', 'Total_Appopens'])
    df2 = pd.read_csv(r'D:\GDrive\2024-25\Projects\Phonepe-Pulse-Data-Visualization-and-Exploration-A-User-Friendly-Tool-Using-Streamlit-and-Plotly\state_names.csv')
    df1.Total_Appopens = df1.Total_Appopens.astype(float)
    df1.State = df2

    fig = px.choropleth(df1, geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                         featureidkey='properties.ST_NM',
                         locations='State',
                         color='Total_Appopens',
                         color_continuous_scale='sunset')

    fig.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig, use_container_width=True)

    # bar chat total user district
    st.markdown("## :violet[Select any State to explore more]")
    selected_state = st.selectbox("",
                                  ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh', 'assam', 'bihar',
                                   'chandigarh', 'chhattisgarh', 'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat', 'haryana',
                                   'himachal-pradesh', 'jammu-&-kashmir', 'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep',
                                   'madhya-pradesh', 'maharashtra', 'manipur', 'meghalaya', 'mizoram',
                                   'nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim',
                                   'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh', 'uttarakhand', 'west-bengal'), index=30)

    cursor.execute(f"select State,Year,Quarter,District,sum(Registered_users) as Total_Users from map_users where Year = {year} and Quarter = {quarter} and State = '{selected_state}' group by State, District,Year,Quarter order by State,District")

    df = pd.DataFrame(cursor.fetchall(), columns=['State', 'year', 'quarter', 'District', 'Total_Users'])
    df.Total_Users = df.Total_Users.astype(int)

    fig = px.bar(df,
                 title=selected_state,
                 x="District",
                 y="Total_Users",
                 orientation='v',
                 color='Total_Users',
                 color_continuous_scale=px.colors.sequential.Agsunset)
    st.plotly_chart(fig, use_container_width=True, aspect_ratio=1.2)

def main():
    """
    This is the main function that runs the Streamlit app.
    """
    setup_page_config()
    db_connection = create_db_connection()
    cursor = db_connection.cursor(buffered=True)
    selected = create_option_menu()

    if selected == "Home":
        show_home_page()
    elif selected == "Charts and Insights":
        show_charts_insights(cursor)
    elif selected == "Geo Map and Insights":
        year = st.session_state.get("year", 2021)
        quarter = st.session_state.get("quarter", 1)
        show_geomap_data(cursor, year, quarter)

if __name__ == "__main__":
    main()