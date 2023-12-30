#import the libraries
import pandas as pd
from pytrends.request import TrendReq
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px  # pip install plotly-express
import os
import datetime


# st.write("""
# #
# # My first app
# Hello *world!*
# """)

pytrend = TrendReq()

# Get Google Keyword Suggestions
# keywords = pytrend.suggestions(keyword='CVE-2021-44228')
# df = pd.DataFrame(keywords)
# df.head(5)

# Function to get Google Trends data
def get_google_trends_data(keyword, start_date, end_date):
    pytrends = TrendReq(hl='en-US', tz=360)
    # Build payload
    pytrends.build_payload(kw_list=[keyword], timeframe=f'{start_date} {end_date}')

    # Get interest over time
    interest_over_time_df = pytrends.interest_over_time()

    return interest_over_time_df
# Specify the keyword and date range
# search_term = "CVE-2021-44228"
# start_date = "2021-12-01"
# end_date = "2022-01-31"
def save_google_trends_CSV(trends_data, file_name):
    trends_data.to_csv(f'google_trends_csv/{file_name}.csv', encoding='utf-8')

def avoid_headacke(data, start_date):
    r =[]
    t = 0
    indexs = [i for i in data.index]
    for i in data.index:
        if i > start_date:
            t += 1
            if t == 1:
                r = r + indexs[indexs.index(i)-4: indexs.index(i)]
            r.append(i)
    return r[1]
def plot_trends(search_term, start_date, end_date, patch_date=None):
    
    if search_term+'.csv' in os.listdir('google_trends_csv/'):
        pass
        # trends_data = pd.read_csv(f'google_trends_csv/{search_term}.csv').set_index('date')

    else:
        trends_data = get_google_trends_data(search_term, "2004-12-01", datetime.datetime.now().strftime("%Y-%m-%d"))
        save_google_trends_CSV(trends_data, search_term)

    trends_data = pd.read_csv(f'google_trends_csv/{search_term}.csv').set_index('date')
    # st.dataframe(trends_data)
    pstart_date = avoid_headacke(trends_data, start_date)
    # st.title(pstart_date)
    # st.title(ggg)
    trends_data = trends_data.loc[(trends_data.index > pstart_date) & (trends_data.index < end_date)]

    # st.dataframe(trends_data)
    fig = px.line(trends_data, x=trends_data.index, y=trends_data.columns[0], markers=True, line_shape='linear')
    fig.add_shape(
    type="rect",
    x0=start_date,
    y0=0,
    x1=patch_date,
    y1=max(trends_data[search_term].tolist())+3,
    fillcolor="rgba(245,40,40,0.2)",  # Fill color with alpha for transparency
    line=dict(width=0),
    layer="below"  # Ensure the filled area is below the line plot
    )
    # Customize the layout
    fig.update_layout(
        title=f'Google Trends for {"".join(trends_data.columns[0])}',
        xaxis_title='Date',
        yaxis_title='Interest Over Time',
        template='plotly',
        legend_title="LEGEND",
        showlegend=True,
        legend=dict(
            title="Legend",
            orientation='h',
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    fig.add_vline(x=start_date, line_width=2, line_dash="solid", line_color="red")
    if patch_date != None:
        fig.add_vline(x=patch_date, line_width=2, line_dash="solid", line_color="green")


    st.plotly_chart(fig)
    
