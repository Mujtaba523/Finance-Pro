# Importing Libraries
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from streamlit_lottie import st_lottie
import yfinance as yf
import datetime
import json
import plotly.graph_objects as go
import folium
from streamlit_folium import folium_static
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def load_lottie(filepath):
    """Reading Lottie files"""
    with open(filepath, 'r') as f:
        return json.load(f)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def currency_converter():
    """Functionality behind currency converter"""
    one,two = st.columns(2)
    with one:
        amount = st.number_input("Enter Amount", value=1.00, min_value=0.01)
        source_currency = st.selectbox("Select Source Currency", options=["USD", "EUR", "JPY", "GBP", "AUD", "CAD", "CHF", "CNY", "NZD","PKR"])
        target_currency = st.radio("Select Target Currency", options=["USD", "EUR", "JPY", "GBP", "AUD", "CAD", "CHF", "CNY", "NZD", "PKR"])
        if st.button("Convert"):
            url = f"https://api.exchangerate-api.com/v4/latest/{source_currency}"
            response = requests.get(url)
            data = response.json()
            conversion_rate = data["rates"][target_currency]
            converted_amount = amount * conversion_rate
            st.success(f"{amount} {source_currency} is equivalent to {converted_amount:.2f} {target_currency}")
    with two:
        animation1 = load_lottie("Animations/3.json")
        st_lottie(animation1, loop=True)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def historical_financial_data_download():
    """Functionality behind daily price & historical data"""
    left, right = st.columns(2)
    with left:
        animation1 = load_lottie("Animations/2.json")
        st_lottie(animation1, loop=True)
    with right:
        # Daily Price
        st.header("Daily Price")
        data_type = st.selectbox("Select Data Type", options=["Stock Price", "Cryptocurrency Price"])
        symbol = st.text_input("Enter Symbol", max_chars=10)
        if st.button("Get Data"):
            try:
                if data_type == "Stock Price":
                    stock_url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey=2N5MLM5DNRFKB9DO"
                    stock_response = requests.get(stock_url)
                    stock_data = stock_response.json()
                    if "Global Quote" in stock_data.keys():
                        stock_price = float(stock_data["Global Quote"]["05. price"])
                        st.success(f"The stock price of {symbol} is: {stock_price:.2f} USD")
                    else:
                        st.error("Invalid symbol entered or stock data not available. Please check the symbol and try again.")
                elif data_type == "Cryptocurrency Price":
                    crypto_url = f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={symbol}&to_currency=USD&apikey=2N5MLM5DNRFKB9DO"
                    crypto_response = requests.get(crypto_url)
                    crypto_data = crypto_response.json()
                    if 'Realtime Currency Exchange Rate' in crypto_data.keys():
                        crypto_price = float(crypto_data['Realtime Currency Exchange Rate']['5. Exchange Rate'])
                        st.success(f"The cryptocurrency price of {symbol} is: {crypto_price:.2f} USD")
                    else:
                        st.error("Invalid symbol entered or cryptocurrency data not available. Please check the symbol and try again.")
            except Exception as e:
                st.error(f"Error: {e}")
        # Historical Data
        st.header("Historical Data")
        symbol = st.text_input("Enter Symbol", max_chars=10, key='download')
        start_date = st.date_input("Start date:", datetime.date(2020, 1, 1))
        end_date = st.date_input("End date:", datetime.date.today())
        if st.button("Historical Data"):
            try:
                # Fetch data from yfinance
                df = yf.download(symbol, start=start_date, end=end_date)
                # Display downloaded data
                st.write("Downloaded data:")
                st.write(df)
                if df.empty:
                    st.warning("No data available for the selected symbol and date range.")
            except Exception as e:
                # Display error message if data download fails
                st.error(f"Error: {e}")
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def finance_analytics():
    """Functionality behind finance analytics"""
    st.header("Financial Data Analytics")
    one,two = st.columns(2)
    with one:
        ticker = st.text_input("Enter Stock Ticker Symbol", value="AAPL", max_chars=5)
        start_date = st.date_input("Select Start Date", datetime.date(2022, 12, 1))
        end_date = st.date_input("Select End Date", datetime.date.today())
        data = yf.download(ticker, start=start_date, end=end_date)
        if data.empty:
            st.warning("No data available for the selected symbol and date range.")
        elif start_date==end_date:
            st.warning("Incorrect date range specified.")
        else:
            current_price = data.iloc[-1]['Close']
            prev_close = data.iloc[-2]['Close']
            percentage_change = ((current_price - prev_close) / prev_close) * 100
            st.subheader(f'Stock Symbol: {ticker}')
            st.write('---')
            # KPIs
            left, right = st.columns(2)
            with left:
                st.metric(
                label='Current Price',
                value=f'${current_price:.2f}',
                delta='',
                delta_color='normal',
            )
            with right:
                color = 'normal' if percentage_change >= 0 else 'inverse'
                icon = '🔺' if percentage_change >= 0 else '🔻'
                st.metric(
                    label='Percentage Change',
                    value=f'{icon} {percentage_change:.2f}%',
                    delta='',
                    delta_color=color,          
                )
            # Descriptive Statistics
            st.subheader("Descriptive Statistics")
            st.write(data.describe())
            # Line Chart
            fig1 = go.Figure()
            fig1.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines',
                                    name='Closing Price'))
            fig1.update_xaxes(title_text='Date')
            fig1.update_yaxes(title_text='Closing Price ($)')
            fig1.update_layout(title=f"{ticker} Stock Price")
            fig1.update_traces(marker_color='#FBAB28')
            st.plotly_chart(fig1)
    with two:
        animation1 = load_lottie("Animations/1.json")
        st_lottie(animation1, loop=True, width=800, height=860)
        # Histogram
        fig3 = px.histogram(data, x='Close', nbins=30, title=f"{ticker} Stock Price - Histogram")
        fig3.update_xaxes(title_text='Closing Price ($)')
        fig3.update_yaxes(title_text='Frequency')
        fig3.update_traces(marker_color='#FBAB28')
        st.plotly_chart(fig3)
       
    # Candlestick chart
    fig2 = go.Figure()
    fig2.add_trace(go.Candlestick(x=data.index,
                                open=data['Open'],
                                high=data['High'],
                                low=data['Low'],
                                close=data['Close'],
                                name='Stock Price',
                                increasing=dict(line=dict(color='#FBAB28')),  
                                decreasing=dict(line=dict(color='#7BA9DA'))))
    fig2.update_xaxes(title_text='Date')
    fig2.update_yaxes(title_text='Price ($)')
    fig2.update_layout(title=f"{ticker} Candlestick Chart")
    fig2.update_layout(width=1400, height=600) 
    st.plotly_chart(fig2)
    # Map
    currencies = {
        'KWD': {'value_in_usd': 3.28, 'lat': 29.3117, 'lon': 47.4818},
        'BHD': {'value_in_usd': 2.66, 'lat': 26.0667, 'lon': 50.5577},
        'OMR': {'value_in_usd': 2.60, 'lat': 23.6083, 'lon': 58.5922},
        'JOD': {'value_in_usd': 1.41, 'lat': 31.9539, 'lon': 35.9106},
        'KYD': {'value_in_usd': 1.20, 'lat': 19.3133, 'lon': -81.2546},
        'GBP': {'value_in_usd': 1.39, 'lat': 51.5074, 'lon': -0.1278},
        'EUR': {'value_in_usd': 1.18, 'lat': 48.8566, 'lon': 2.3522},
        'CHF': {'value_in_usd': 1.05, 'lat': 46.2044, 'lon': 6.1432},
        'BSD': {'value_in_usd': 1.00, 'lat': 25.0343, 'lon': -77.3963},
        'PAB': {'value_in_usd': 1.00, 'lat': 8.5380, 'lon': -80.7821}
    }
    currency_df = pd.DataFrame.from_dict(currencies, orient='index')
    m = folium.Map(location=[0, 0], zoom_start=2, tiles='cartodb dark_matter')
    for _, currency in currency_df.iterrows():
        folium.Marker(
            location=[currency['lat'], currency['lon']],
            tooltip=f"Currency: {_}<br>Value in USD: {currency['value_in_usd']}",
            icon=folium.Icon(icon='money', color='orange')
        ).add_to(m)
    st.subheader('Top 10 Strongest Currencies in the World')
    folium_static(m, width=1400, height=600)

def main():
    """Driver Program"""
    st.set_page_config(layout="wide")
    st.title("FinancePro - Your Ultimate Financial Companion!")
    option = st.sidebar.selectbox("Select an option", ["Currency Converter", "Financial Data", "Analytics"])
    if option == "Currency Converter":
        st.header("Currency Converter")
        currency_converter()
    elif option == "Financial Data": 
        historical_financial_data_download()
    elif option == "Analytics":
        finance_analytics()
main()