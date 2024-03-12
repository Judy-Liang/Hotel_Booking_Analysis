import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.express as px
import folium


def clean_df(df):
    '''
    cleaning the data, i.e. drop the columns with lots of NA values, 
    drop NA values, drop values that make no sense and etc.

    df:= the input dataframe

    output: cleaned dataframe
    '''

    df.drop('company', axis=1, inplace=True)
    df.drop('agent', axis=1, inplace=True)

    mode_value = df["country"].mode()[0]
    df["country"].fillna(value=mode_value, inplace=True)

    df.dropna(subset=['children'], inplace=True)

    # In meal column, 'Undefined' and 'SC' are the same
    df["meal"] = df["meal"].replace("Undefined", "SC")
    
    #Sort values for children
    df.sort_values('children',ascending = False)
    #drop irrational data
    df.drop(328, axis=0, inplace=True)

    df.sort_values('babies',ascending = False)
    #drop irrational data
    df.drop([46619,78656], axis=0, inplace=True)

    # the sum of children, adults and babies can not be zero
    filter = (df.children == 0) & (df.adults == 0) & (df.babies == 0)
    df = df.loc[~filter]

    return df

def preprocessing_df(df):
    '''
    Data preprocessing including dropping useless columns, transfering the combined date data
    into year, month and day, encoding categorical variables, normalizing columns
    '''

    dataset = df.copy()
    dataset.drop('adr_pp', axis=1, inplace=True)

    # Correlation
    plt.figure(figsize = (24, 12))
    corr = dataset.corr()
    sns.heatmap(corr, annot = True, linewidths = 1)
    plt.show()

    # Drop useless columns
    useless_col = ['days_in_waiting_list', 'arrival_date_year', 'assigned_room_type', 'booking_changes',
                   'reservation_status', 'country', 'days_in_waiting_list']
    dataset.drop(useless_col, axis=1, inplace=True)

    # Convert 'reservation_status_date' to datetime and extract year, month, day
    if 'reservation_status_date' in dataset.columns:
        dataset['reservation_status_date'] = pd.to_datetime(dataset['reservation_status_date'])
        dataset['year'] = dataset['reservation_status_date'].dt.year
        dataset['month'] = dataset['reservation_status_date'].dt.month
        dataset['day'] = dataset['reservation_status_date'].dt.day
        dataset.drop(['reservation_status_date', 'arrival_date_month'], axis=1, inplace=True)

    # Identifying categorical columns
    cat_cols = [col for col in dataset.columns if dataset[col].dtype == 'O']
    cat_df = dataset[cat_cols]

    mappings = {
        'hotel': {'Resort Hotel': 0, 'City Hotel': 1},
        'meal': {'BB': 0, 'FB': 1, 'HB': 2, 'SC': 3, 'Undefined': 4},
        'market_segment': {
            'Direct': 0, 'Corporate': 1, 'Online TA': 2, 'Offline TA/TO': 3,
            'Complementary': 4, 'Groups': 5, 'Undefined': 6, 'Aviation': 7
            },
        'distribution_channel': {'Direct': 0, 'Corporate': 1, 'TA/TO': 2, 'Undefined': 3, 'GDS': 4},
        'reserved_room_type': {
            'C': 0, 'A': 1, 'D': 2, 'E': 3, 'G': 4, 'F': 5, 'H': 6,
            'L': 7, 'B': 8
            },
        'deposit_type': {'No Deposit': 0, 'Refundable': 1, 'Non Refund': 3},
        'customer_type': {'Transient': 0, 'Contract': 1, 'Transient-Party': 2, 'Group': 3},
        'year': {2015: 0, 2014: 1, 2016: 2, 2017: 3}
    }
    # Apply mappings for categorical variable encoding    
    cat_df.replace(mappings, inplace=True)

    # Normalize numerical variables
    num_df = dataset.drop(columns=cat_cols + ['is_canceled'], axis=1)
    for column in ['lead_time', 'arrival_date_week_number', 'arrival_date_day_of_month', 'adr']:
        num_df[column] = np.log1p(num_df[column])

    # Handle missing values for 'adr'
    num_df['adr'] = num_df['adr'].fillna(value=num_df['adr'].mean())

    # Combine categorical and numerical dataframes
    X = pd.concat([cat_df, num_df], axis=1)
    y = df['is_canceled']

    return X, y