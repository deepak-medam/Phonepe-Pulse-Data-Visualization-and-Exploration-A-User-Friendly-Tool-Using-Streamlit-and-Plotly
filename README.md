# Phonepe-Pulse-Data-Visualization-and-Exploration-A-User-Friendly-Tool-Using-Streamlit-and-Plotly

## This project is developed in 6 stages:
1. **Data Extraction**: In this step I collected the data from phonepe pulse github using scripting
2. **Data Transformation**: In this step I transformed the raw json data to json files with useful information and then to csv files
3. **Database Insertion**: In this step I wrote a python script to use the csv files and insert the data to different tables using mysql which helps in faster retreival of data.
4. **Dashboard Creation**: Using streamlit I created a simple dashboard to show the results
5. **Data Retreival**: I used plotly for various graphs and charts to display the different insights.
6. **Deployement**: After thorough tesing I deployed my streamlit app.

## Main libraries
* pip install mysql-connector-python
* pip install plotly streamlit