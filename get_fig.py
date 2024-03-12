import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.express as px
import folium


def hotel_type_fig(df):
    '''
    Bar plot that shows the number of each type of hotel booking.

    df:= cleaned dataframe
    '''
    hotel_counts = df['hotel'].value_counts()

    # Create the bar plot with the counts
    fig = px.bar(hotel_counts, 
                 x=hotel_counts.index, 
                 y=hotel_counts.values, 
                 labels={'x': 'Hotel Type', 'y': 'Number of Guests'}, 
                 template='plotly_dark', 
                 title='Number of Guests for Each Hotel Type')
    fig.show()

    return

def guest_distribution_pie(df):
    '''
    Show origin country distribution of the guests.
    '''

    # Filter out canceled bookings and then count occurrences of each country
    country_counts = df.loc[df['is_canceled'] == 0, 'country'].value_counts().rename_axis('country').reset_index(name='No of guests')

    fig = px.pie(country_counts,
                 values='No of guests',
                 names='country',
                 title='Home Country of Guests',
                 template='seaborn')

    fig.update_traces(textposition='inside', textinfo='percent+label')

    fig.show()

    return country_counts

def guest_distribution_map(country_counts):
    '''
    Show the country distribution in a heat map of the world map.
    '''

    basemap = folium.Map()
    guests_map = px.choropleth(country_counts, locations = country_counts['country'],
                            color = country_counts['No of guests'], hover_name = country_counts['country'])
    guests_map.show()

    return

def room_price_per_night(df):
    '''
    Find out the price of each room type and hotel type per night (ADR).
    '''

    data = df[df['is_canceled'] == 0]
    data = data.sort_values('reserved_room_type')
    fig = px.box(data_frame = data, x = 'reserved_room_type', y = 'adr', color = 'hotel', template = 'plotly_dark',
        labels={'reserved_room_type': 'Reserved Room Type', 'adr': 'Average Daily Rate'}, title = 'Room price per night')
    fig.show()

    return

def room_price_per_night_pp(df):
    '''
    The room price per person (include adults and children, babies are not included)
    of different room type and hotel type.

    df:= dataframe after previous editting

    output: 
    data_resort: data of resort hotel booking that checked-in
    data_city: data of city hotel booking that checked-in
    data: the whole data of hotel booking that checked-in
    '''

    data = df.copy()

    # Filter for checked-in bookings for both hotel types
    data_resort = data[(data['hotel'] == 'Resort Hotel') & (data['is_canceled'] == 0)].copy()
    data_city = data[(data['hotel'] == 'City Hotel') & (data['is_canceled'] == 0)].copy()

    # Compute the ADR per person for both datasets
    for dataset in [data_resort, data_city, data]:
        dataset['adr_pp'] = dataset['adr'] / (dataset['adults'] + dataset['children']).replace({0: 1})

    data = data[data['is_canceled'] == 0]

    room_price_pp = data[['hotel', 'reserved_room_type', 'adr_pp']].sort_values('reserved_room_type')
    
    fig = px.box(data_frame=room_price_pp, x='reserved_room_type', y='adr_pp', color='hotel', template='plotly_dark',
                 labels={'reserved_room_type': 'Reserved Room Type', 'adr_pp': 'Average Daily Rate Per Person'},
                 title='Room Price per Night per Person')
    fig.show()

    # Return the processed dataframes
    return data_resort, data_city, data

def price_over_year(data_resort, data_city):
    '''
    Compute the average room price of each month over the year of 
    each room type and hotel type.
    '''
    # Group by month and calculate average price, then reset index
    resort_prices = data_resort.groupby('arrival_date_month')['adr'].mean().reset_index(name='price_for_resort')
    city_prices = data_city.groupby('arrival_date_month')['adr'].mean().reset_index(name='price_for_city')

    # Merge dataframes on the month column
    combined_prices = pd.merge(resort_prices, city_prices, on='arrival_date_month', how='outer')

    # correct ordering of months
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    combined_prices['arrival_date_month'] = pd.Categorical(combined_prices['arrival_date_month'], categories=month_order, ordered=True)
    combined_prices.sort_values('arrival_date_month', inplace=True)

    # plot
    fig = px.line(combined_prices, x='arrival_date_month', y=['price_for_resort', 'price_for_city'],
                  labels={'variable': 'Hotel Type', 'value': 'Average Price', 'arrival_date_month': 'Month'},
                  title='Average Room Price per Night Over the Months')
    fig.update_layout(template='plotly_dark', xaxis_title='Month', yaxis_title='Average Price (€)')
    fig.show()

    return


def busiest_month(data_resort, data_city):
    '''
    Compute the average number of hotel guests per month.
    '''
    # Calculate monthly guests for both hotel types
    resort_guests_monthly = data_resort.groupby('arrival_date_month', as_index=False)['hotel'].count()
    city_guests_monthly = data_city.groupby('arrival_date_month', as_index=False)['hotel'].count()

    # Rename columns for clarity
    resort_guests_monthly.rename(columns={'hotel': 'guests'}, inplace=True)
    resort_guests_monthly['hotel'] = 'Resort Hotel'
    
    city_guests_monthly.rename(columns={'hotel': 'guests'}, inplace=True)
    city_guests_monthly['hotel'] = 'City Hotel'

    combined_data = pd.concat([resort_guests_monthly, city_guests_monthly], axis=0)
    
    # Convert 'arrival_date_month' to datetime to order months correctly
    months_order = {month: i for i, month in enumerate(['January', 'February', 'March', 'April', 'May', 'June', 
                                                        'July', 'August', 'September', 'October', 'November', 'December'])}
    combined_data['month_num'] = combined_data['arrival_date_month'].map(months_order)
    combined_data.sort_values('month_num', inplace=True)
    
    # Plot
    fig = px.line(combined_data, x='arrival_date_month', y='guests', color='hotel',
                  labels={'arrival_date_month': 'Month', 'guests': 'Number of Guests'},
                  title='Average Number of Hotel Guests Per Month')
    fig.update_layout(template='plotly_dark', xaxis_title='Month', yaxis_title='Average Number of Guests', legend_title='Hotel Type')

    fig.show()

    return

def stay_distribution(data):
    '''
    Conpute the days of stay for each type of hotel.
    '''

    data['total_night'] = data['stays_in_weekend_nights'] + data['stays_in_week_nights']

    stay = data.groupby(['total_night', 'hotel']).agg('count').reset_index()
    stay = stay.iloc[:, :3]
    stay = stay.rename(columns={'is_canceled':'Number of stays'})

    fig = px.bar(data_frame = stay, x = 'total_night', y = 'Number of stays', color = 'hotel', barmode = 'group',
        template = 'plotly_dark')
    fig.show()

    return

def market_segment_pie(df):
    '''
    Show the market segement of number of hotel booking.
    '''
    segments = df['market_segment'].value_counts()

    fig = px.pie(segments,
                values=segments.values,
                names=segments.index,
                title="Bookings per market segment",
                template="seaborn")
    fig.update_traces(rotation=-90, textinfo="percent+label")
    fig.show()

    return

def market_segment_barplot(df):
    '''
    Show room price per night per person (ADR_pp) for different 
    market segmentation and different type of rooms.
    '''

    new_data = df
    new_data['adr_pp'] = new_data['adr']/ (new_data['adults'] + new_data['children'])
    new_data = new_data.sort_values('reserved_room_type')
    # price per night (ADR) and person based on booking and room.

    plt.figure(figsize=(12, 8))
    sns.barplot(x='market_segment',
                y='adr_pp',
                hue='reserved_room_type',
                data=new_data,
                errorbar='sd',
                err_kws={'linewidth': 1},
                capsize=0.1)
    plt.title('ADR by market segment and room type', fontsize=16)
    plt.xlabel('Market segment', fontsize=16)
    plt.xticks(rotation=45)
    plt.ylabel('ADR per person', fontsize=16)
    plt.legend(loc='upper left')
    plt.show()

    return

def airline_data(df):
    '''
    Show the hotel booking data for aviation, including columns
    'is_canceled', 'adults', 'lead time', 'adr_pp'
    '''
    Airline_data = df.loc[df["market_segment"]== "Aviation"][["is_canceled", "adults", "lead_time", "adr_pp"]].describe()

    Non_Airline_data = df.loc[df["market_segment"]!= "Aviation"][["is_canceled", "adults", "lead_time", "adr_pp"]].describe()

    return Airline_data, Non_Airline_data

def lead_time(df):
    '''
    Show the relationship between lead time and cancellation.
    '''
    fig = px.histogram(df, x='lead_time', color='is_canceled',
                   barmode='stack', nbins=50,
                   title='Relationship between Lead Time and Cancellation',
                   labels={'lead_time': 'Lead Time', 'count': 'Count'}, template = 'plotly_dark')
    fig.update_traces(marker_line_width=1, marker_line_color='black')
    fig.show()
    
    return

def deposite_type(df):
    '''
    Show the relationship between cancenlation and deposit type.
    '''
    fig = px.histogram(df, x='deposit_type', color='is_canceled',
                   barmode='group', text_auto=True,
                   title='Relationship between Deposit Type and Cancellation',
                   template = 'plotly_dark')

    fig.update_layout(xaxis_title='Deposit Type', yaxis_title='Count')

    fig.show()

    return

def previous_cancel(df):
    '''
    Show the scatter plot of previous cancelation and is_canceled status
    '''
    fig = px.scatter(df, x='previous_cancellations', y='is_canceled',
                 title='Scatter Plot of Previous Cancellations and Cancellation Status',
                 labels={'previous_cancellations': 'Previous Cancellations', 'is_canceled': 'Is Canceled (0 or 1)'},
                 template = 'plotly_dark')

    fig.update_yaxes(tickvals=[0, 1])

    fig.show()

    return

def highest_num_cancel(df):
    '''
    Compute the cancelation per month based on different hotel type.
    '''
    # Calculate bookings and cancellations per month for each hotel type
    bookings_per_month = df.groupby(['hotel', 'arrival_date_month'])['hotel'].count().rename('Bookings')
    cancellations_per_month = df.groupby(['hotel', 'arrival_date_month'])['is_canceled'].sum().rename('Cancellations')

    # Combine the two series
    cancel_data = pd.concat([bookings_per_month, cancellations_per_month], axis=1).reset_index()
    cancel_data['Cancelation Rate'] = (cancel_data['Cancellations'] / cancel_data['Bookings']) * 100

    # Sort data by month in correct chronological order
    months_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                    'July', 'August', 'September', 'October', 'November', 'December']
    cancel_data['arrival_date_month'] = pd.Categorical(cancel_data['arrival_date_month'], categories=months_order, ordered=True)
    cancel_data.sort_values(['hotel', 'arrival_date_month'], inplace=True)

    # Visualization
    plt.figure(figsize=(12, 8))
    sns.barplot(x='arrival_date_month', y='Cancelation Rate', hue='hotel', data=cancel_data)
    plt.title('Cancellation Rate per Month by Hotel Type')
    plt.xlabel('Month')
    plt.xticks(rotation=45)
    plt.ylabel('Cancellation Rate (%)')
    plt.legend(title='Hotel Type', loc='upper right')
    plt.tight_layout()
    plt.show()    
    return



