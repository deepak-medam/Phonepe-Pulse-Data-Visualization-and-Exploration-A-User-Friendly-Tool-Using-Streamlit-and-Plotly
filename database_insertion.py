import pandas as pd
import mysql.connector
from mysql.connector import errorcode

# creates database if it doesn't exist
def create_database(host, user, password, database):
    try:
        db_connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
        )
        cursor = db_connection.cursor()

        # database creation if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
        cursor.execute(f"USE {database}")

        cursor.close()
        db_connection.close()
        print("Database created successfully.")

    except mysql.connector.Error as error:
        print("Error while creating database:", error)


# Creates table if it doesn't exist
def create_table(cursor, table_name, columns):
    try:
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})")
        print(f"Table {table_name} created successfully.")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print(f"Table {table_name} already exists.")
        else:
            print(err.msg)


# Inserts data into table uses dataframe datatypes and mapit into sql types.
def insert_data(cursor, table_name, df):
    try:
        placeholders = ', '.join(['%s'] * len(df.columns))
        for _, row in df.iterrows():
            values = tuple(row[col] for col in df.columns)
            sql = f"INSERT INTO {table_name} ({', '.join(df.columns)}) VALUES ({placeholders})"
            cursor.execute(sql, values)
        print(f"Data inserted into {table_name} successfully.")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_WARN_DATA_OUT_OF_RANGE:
            print(f"Out of range value for row: {row}")
        else:
            print(err.msg)


def main():
    # local database connection
    host = "127.0.0.1"
    user = "root"
    password = "password"
    database = "phonepe_pulse"

    # database creation
    create_database(host, user, password, database)

    # list of all files paths
    file_paths = [
        (r'D:\GDrive\2024-25\Projects\Phonepe-Pulse-Data-Visualization-and-Exploration-A-User-Friendly-Tool-Using-Streamlit-and-Plotly\aggregated_transaction.csv'),
        (r'D:\GDrive\2024-25\Projects\Phonepe-Pulse-Data-Visualization-and-Exploration-A-User-Friendly-Tool-Using-Streamlit-and-Plotly\aggregated_users.csv'),
        (r'D:\GDrive\2024-25\Projects\Phonepe-Pulse-Data-Visualization-and-Exploration-A-User-Friendly-Tool-Using-Streamlit-and-Plotly\map_transactions.csv'),
        (r'D:\GDrive\2024-25\Projects\Phonepe-Pulse-Data-Visualization-and-Exploration-A-User-Friendly-Tool-Using-Streamlit-and-Plotly\map_users.csv'),
        (r'D:\GDrive\2024-25\Projects\Phonepe-Pulse-Data-Visualization-and-Exploration-A-User-Friendly-Tool-Using-Streamlit-and-Plotly\top_transactions_pincode.csv'),
        (r'D:\GDrive\2024-25\Projects\Phonepe-Pulse-Data-Visualization-and-Exploration-A-User-Friendly-Tool-Using-Streamlit-and-Plotly\top_transactions_state.csv'),
        (r'D:\GDrive\2024-25\Projects\Phonepe-Pulse-Data-Visualization-and-Exploration-A-User-Friendly-Tool-Using-Streamlit-and-Plotly\top_user_district.csv'),
        (r'D:\GDrive\2024-25\Projects\Phonepe-Pulse-Data-Visualization-and-Exploration-A-User-Friendly-Tool-Using-Streamlit-and-Plotly\top_user_picode.csv'),
    ]

    # List of all table names
    table_names = [
        'aggregate_transactions',
        'aggregate_users',
        'map_transactions',
        'map_users',
        'top_transactions_pincode',
        'top_transactions_state',
        'top_user_district',
        'top_user_pincode'
    ]

    try:
        db_connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
        )
        cursor = db_connection.cursor()

        for file_path, table_name in zip(file_paths, table_names):
            df = pd.read_csv(file_path)
            mysql_data_types = {
                'int64': 'INT',
                'float64': 'DOUBLE',
                'object': 'VARCHAR(255)',
            }
            # dynamic mapping of columns from dataframe using dataframe column types.
            columns = ', '.join([f"{col} {mysql_data_types[str(df[col].dtype)]}" for col in df.columns])

            create_table(cursor, table_name, columns)
            insert_data(cursor, table_name, df)

    except mysql.connector.Error as error:
        print("Error while connecting to MySQL", error)

    finally:
        if db_connection.is_connected():
            cursor.close()
            db_connection.close()
            print("MySQL connection is closed.")

if __name__ == "__main__":
    main()
