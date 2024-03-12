import pandas as pd
from statsmodels.tsa.seasonal import STL
import matplotlib.pyplot as plt

def STL_analysis(df):
    '''
    Aggregate the data to create a daily time series of bookings and then 
    proceed with the STL decomposition and visualization of the components.
    '''
    df['arrival_date'] = pd.to_datetime(df['arrival_date_year'].astype(str) + '-' +
                                    df['arrival_date_month'] + '-' +
                                    df['arrival_date_day_of_month'].astype(str))

    # Aggregate data to find the total number of bookings per day
    daily_bookings = df.groupby('arrival_date')['hotel'].count()

    # Perform STL Decomposition
    stl = STL(daily_bookings, seasonal=13)
    result = stl.fit()

    # Visualize the Decomposition
    fig, axes = plt.subplots(4, 1, figsize=(10, 8), sharex=True)
    plt.subplots_adjust(hspace=0.5)

    # Original Data
    axes[0].plot(daily_bookings, label='Original Series')
    axes[0].set_title('Original Series')
    axes[0].legend()

    # Trend Component
    axes[1].plot(result.trend, label='Trend Component')
    axes[1].set_title('Trend Component')
    axes[1].legend()

    # Seasonal Component
    axes[2].plot(result.seasonal, label='Seasonal Component')
    axes[2].set_title('Seasonal Component')
    axes[2].legend()

    # Residual Component
    axes[3].plot(result.resid, label='Residual Component')
    axes[3].set_title('Residual Component')
    axes[3].legend()

    plt.tight_layout()
    plt.show()

    return