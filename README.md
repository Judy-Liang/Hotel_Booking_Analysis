# Hotel_Booking_Analysis

# Abstract
Our project focuses on data analysis and visualization to derive meaningful insights into hotel booking dynamics. Our approach includes an in-depth analysis of trends, seasonal patterns, and the impact of various factors on customers' booking decisions and cancellation rates. Moreover, we also utilize Random Forest classifier to predict cancellation result. The insights gained can help hotel managers in capacity planning, pricing strategy, and improving customer satisfaction.

## Dataset
The dataset can be accessed by downloading "hotel_bookingscsv" or https://www.kaggle.com/datasets/jessemostipak/hotel-booking-demand.

## File Structure
Our project include four part: data wrangling, EDA, advanced EDA, model building. **The whole process can be run using "ece143_hotel_booking_concise.ipynb", or you can also run part by part** as the following:
- Data Wrangling: "data_cleaning.py", clean and pre-process the data.
- EDA: "EDA.py", get the insights about the data and plot data for detailed analysis.
- Advanced EDA: "STL_analysis.py", check trend or seasonal pattern in the data.
- Model Building: "RFC.py", build random forest classifier for prediction.

## Third-Party Modules
- pandas
- matplotlib
- seaborn
- numpy
- plotly.express
- folium
- sklearn
