import json
import os
import pandas as pd


def aggregate_transactions(dir_path):
    df_data = {'State': [], 'Year': [], 'Quarter': [], 'Transaction_Type': [], 'Transaction_Count': [], 'Transaction_Amount': []}
    for state in os.listdir(dir_path):
        state_path = os.path.join(dir_path, state)
        if not os.path.isdir(state_path):
            continue
        
        for year in os.listdir(state_path):
            year_path = os.path.join(state_path, year)
            if not os.path.isdir(year_path):
                continue
            
            for quarter_file in os.listdir(year_path):
                if quarter_file.endswith('.json'):
                    quarter_path = os.path.join(year_path, quarter_file)
                    with open(quarter_path, 'r') as f:
                        quarter_data = json.load(f)
                        quarter_num = int(quarter_file.strip('.json'))
                        for transaction in quarter_data['data']['transactionData']:
                            name = transaction['name']
                            count = transaction['paymentInstruments'][0]['count']
                            amount = transaction['paymentInstruments'][0]['amount']
                            df_data['State'].append(state)
                            df_data['Year'].append(year)
                            df_data['Quarter'].append(quarter_num)
                            df_data['Transaction_Type'].append(name)
                            df_data['Transaction_Count'].append(count)
                            df_data['Transaction_Amount'].append(amount)

    return pd.DataFrame(df_data)


def aggregate_users(dir_path):
    df_data = {'State': [], 'Year': [], 'Quarter': [], 'Registered_users':[], 'App_opens':[], 'Brand': [], 'User_Count': [], 'Percentage': []}

    for state in os.listdir(dir_path):
        state_path = os.path.join(dir_path, state)
        if not os.path.isdir(state_path):
            continue

        for year in os.listdir(state_path):
            year_path = os.path.join(state_path, year)
            if not os.path.isdir(year_path):
                continue

            for quarter_file in os.listdir(year_path):
                if quarter_file.endswith('.json'):
                    quarter_path = os.path.join(year_path, quarter_file)
                    with open(quarter_path, 'r') as f:
                        quarter_data = json.load(f)
                        quarter_num = int(quarter_file.strip('.json'))
                        registered_users = quarter_data['data']['aggregated']['registeredUsers']
                        app_opens = quarter_data['data']['aggregated']['appOpens']
                        try:      
                            users_data = quarter_data['data'].get('usersByDevice')  # Use .get() to safely get the value
                            if users_data is None:
                                continue
                            for user in users_data:
                                brand = user['brand']
                                count = user['count']
                                percentage = user['percentage']
                                df_data['State'].append(state)
                                df_data['Year'].append(year)
                                df_data['Quarter'].append(quarter_num)
                                df_data['Registered_users'].append(registered_users)
                                df_data['App_opens'].append(app_opens)
                                df_data['Brand'].append(brand)
                                df_data['User_Count'].append(count)
                                df_data['Percentage'].append(percentage)
                        except KeyError:
                            pass

    return pd.DataFrame(df_data)


def map_transactions(dir_path):
    df_data = {'State': [], 'Year': [], 'Quarter': [], 'District': [], 'Transaction_Count': [], 'Transaction_Amount': []}
    for state in os.listdir(dir_path):
        state_path = os.path.join(dir_path, state)
        if not os.path.isdir(state_path):
            continue

        for year in os.listdir(state_path):
            year_path = os.path.join(state_path, year)
            if not os.path.isdir(year_path):
                continue

            for quarter_file in os.listdir(year_path):
                if quarter_file.endswith('.json'):
                    quarter_path = os.path.join(year_path, quarter_file)
                    with open(quarter_path, 'r') as f:
                        quarter_data = json.load(f)
                        quarter_num = int(quarter_file.strip('.json'))
                        for hover_data in quarter_data['data']['hoverDataList']:
                            district = hover_data['name']
                            count = hover_data['metric'][0]['count']
                            amount = hover_data['metric'][0]['amount']
                            df_data['State'].append(state)
                            df_data['Year'].append(year)
                            df_data['Quarter'].append(quarter_num)
                            df_data['District'].append(district)
                            df_data['Transaction_Count'].append(count)
                            df_data['Transaction_Amount'].append(amount)

    return pd.DataFrame(df_data)


def map_users(dir_path):
    df_data = {'State': [], 'Year': [], 'Quarter': [], 'District': [], 'Registered_users': []}
    for state in os.listdir(dir_path):
        state_path = os.path.join(dir_path, state)
        if not os.path.isdir(state_path):
            continue

        for year in os.listdir(state_path):
            year_path = os.path.join(state_path, year)
            if not os.path.isdir(year_path):
                continue

            for quarter_file in os.listdir(year_path):
                if quarter_file.endswith('.json'):
                    quarter_path = os.path.join(year_path, quarter_file)
                    with open(quarter_path, 'r') as f:
                        quarter_data = json.load(f)
                        quarter_num = int(quarter_file.strip('.json'))
                        for district, data in quarter_data['data']['hoverData'].items():
                            registered_users = data['registeredUsers']
                            df_data['State'].append(state)
                            df_data['Year'].append(year)
                            df_data['Quarter'].append(quarter_num)
                            df_data['District'].append(district)
                            df_data['Registered_users'].append(registered_users)

    return pd.DataFrame(df_data)


def top_transactions_state(dir_path):
    df_data = {'State': [], 'Year': [], 'Quarter': [], 'District': [], 'Transaction_count': [], 'Transaction_amount': []}
    for state in os.listdir(dir_path):
        state_path = os.path.join(dir_path, state)
        if not os.path.isdir(state_path):
            continue
        
        for year in os.listdir(state_path):
            year_path = os.path.join(state_path, year)
            if not os.path.isdir(year_path):
                continue
            
            for quarter_file in os.listdir(year_path):
                if quarter_file.endswith('.json'):
                    quarter_path = os.path.join(year_path, quarter_file)
                    with open(quarter_path, 'r') as f:
                        quarter_data = json.load(f)
                        quarter_num = int(quarter_file.strip('.json'))
                        for district_data in quarter_data['data']['districts']:
                            district = district_data['entityName']
                            district_count = district_data['metric']['count']
                            district_amount = district_data['metric']['amount']
                            df_data['State'].append(state)
                            df_data['Year'].append(year)
                            df_data['Quarter'].append(quarter_num)
                            df_data['District'].append(district)
                            df_data['Transaction_count'].append(district_count)
                            df_data['Transaction_amount'].append(district_amount)

    return pd.DataFrame(df_data)


def top_transactions_pincode(dir_path):
    df_data = {'State': [], 'Year': [], 'Quarter': [], 'Pincode': [], 'Transaction_count': [], 'Transaction_amount': []}
    for state in os.listdir(dir_path):
        state_path = os.path.join(dir_path, state)
        if not os.path.isdir(state_path):
            continue
        
        for year in os.listdir(state_path):
            year_path = os.path.join(state_path, year)
            if not os.path.isdir(year_path):
                continue
            
            for quarter_file in os.listdir(year_path):
                if quarter_file.endswith('.json'):
                    quarter_path = os.path.join(year_path, quarter_file)
                    with open(quarter_path, 'r') as f:
                        quarter_data = json.load(f)
                        quarter_num = int(quarter_file.strip('.json'))
                        for pincode_data in quarter_data['data']['pincodes']:
                            pincode = pincode_data['entityName']
                            pincode_count = pincode_data['metric']['count']
                            pincode_amount = pincode_data['metric']['amount']
                            df_data['State'].append(state)
                            df_data['Year'].append(year)
                            df_data['Quarter'].append(quarter_num)
                            df_data['Pincode'].append(pincode)
                            df_data['Transaction_count'].append(pincode_count)
                            df_data['Transaction_amount'].append(pincode_amount)

    return pd.DataFrame(df_data)


def top_user_district(dir_path):
    df_data = {'State': [], 'Year': [], 'Quarter': [], 'District': [], 'Registered_users': []}
    for state in os.listdir(dir_path):
        state_path = os.path.join(dir_path, state)
        if not os.path.isdir(state_path):
            continue
        
        for year in os.listdir(state_path):
            year_path = os.path.join(state_path, year)
            if not os.path.isdir(year_path):
                continue
            
            for quarter_file in os.listdir(year_path):
                if quarter_file.endswith('.json'):
                    quarter_path = os.path.join(year_path, quarter_file)
                    with open(quarter_path, 'r') as f:
                        quarter_data = json.load(f)
                        quarter_num = int(quarter_file.strip('.json'))
                        for district_data in quarter_data['data']['districts']:
                            district = district_data['name']
                            registered_user = district_data['registeredUsers']
                            df_data['State'].append(state)
                            df_data['Year'].append(year)
                            df_data['Quarter'].append(quarter_num)
                            df_data['District'].append(district)
                            df_data['Registered_users'].append(registered_user)

    return pd.DataFrame(df_data)


def top_user_pincode(dir_path):
    df_data = {'State': [], 'Year': [], 'Quarter': [], 'Pincode': [], 'Registered_users': []}
    
    for state in os.listdir(dir_path):
        state_path = os.path.join(dir_path, state)
        if not os.path.isdir(state_path):
            continue
        
        for year in os.listdir(state_path):
            year_path = os.path.join(state_path, year)
            if not os.path.isdir(year_path):
                continue
            
            for quarter_file in os.listdir(year_path):
                if quarter_file.endswith('.json'):
                    quarter_path = os.path.join(year_path, quarter_file)
                    with open(quarter_path, 'r') as f:
                        quarter_data = json.load(f)
                        quarter_num = int(quarter_file.strip('.json'))
                        
                        # Process pincode data
                        for pincode_data in quarter_data['data']['pincodes']:
                            pincode = pincode_data['name']
                            registered_user = pincode_data['registeredUsers']
                            df_data['State'].append(state)
                            df_data['Year'].append(year)
                            df_data['Quarter'].append(quarter_num)
                            df_data['Pincode'].append(pincode)
                            df_data['Registered_users'].append(registered_user)

    return pd.DataFrame(df_data)


# Data paths for all different data directories
path_to_aggregate_transaction_data = r"D:\GDrive\2024-25\Projects\Phonepe-Pulse-Data-Visualization-and-Exploration-A-User-Friendly-Tool-Using-Streamlit-and-Plotly\data\aggregated\transaction\country\india\state"
path_to_aggregate_user_data = r"D:\GDrive\2024-25\Projects\Phonepe-Pulse-Data-Visualization-and-Exploration-A-User-Friendly-Tool-Using-Streamlit-and-Plotly\data\aggregated\user\country\india\state"
path_to_map_transaction_data = r"D:\GDrive\2024-25\Projects\Phonepe-Pulse-Data-Visualization-and-Exploration-A-User-Friendly-Tool-Using-Streamlit-and-Plotly\data\map\transaction\hover\country\india\state"
path_to_user_map_data = r"D:\GDrive\2024-25\Projects\Phonepe-Pulse-Data-Visualization-and-Exploration-A-User-Friendly-Tool-Using-Streamlit-and-Plotly\data\map\user\hover\country\india\state"
path_to_top_transaction_data = r"D:\GDrive\2024-25\Projects\Phonepe-Pulse-Data-Visualization-and-Exploration-A-User-Friendly-Tool-Using-Streamlit-and-Plotly\data\top\transaction\country\india\state"
path_to_top_user_data = r"D:\GDrive\2024-25\Projects\Phonepe-Pulse-Data-Visualization-and-Exploration-A-User-Friendly-Tool-Using-Streamlit-and-Plotly\data\top\user\country\india\state"

# Creating data frames from data extraction functions.
aggregated_transaction_df = aggregate_transactions(path_to_aggregate_transaction_data)
aggregated_users_df = aggregate_users(path_to_aggregate_user_data)
map_transactions_df = map_transactions(path_to_map_transaction_data)
map_users_df = map_users(path_to_user_map_data)
top_transactions_state_df = top_transactions_state(path_to_top_transaction_data)
top_transactions_pincode_df = top_transactions_pincode(path_to_top_transaction_data)
top_user_district_df = top_user_district(path_to_top_user_data)
top_user_pincode_df = top_user_pincode(path_to_top_user_data)

aggregated_transaction_df.info()
aggregated_users_df.info()
map_transactions_df.info()
map_users_df.info()
top_transactions_state_df.info()
top_transactions_pincode_df.info()
top_user_district_df.info()
top_user_pincode_df.info()


# # Converting data frames to csv files
# aggregated_transaction_df.to_csv('aggregated_transaction.csv',index=False)
# aggregated_users_df.to_csv('aggregated_users.csv',index=False)
# map_transactions_df.to_csv('map_transactions.csv',index=False)
# map_users_df.to_csv('map_users.csv',index=False)
# top_transactions_state_df.to_csv('top_transactions_state.csv', index=False)
# top_transactions_pincode_df.to_csv('top_transactions_pincode.csv', index=False)
# top_user_district_df.to_csv('top_user_district.csv', index=False)
# top_user_pincode_df.to_csv('top_user_picode.csv', index=False)