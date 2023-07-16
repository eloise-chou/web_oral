import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
from geo_util import count_points_within_radius

@st.cache_data
def get_traffic_accident_data(): 
    traffic_data = pd.read_csv('./車流量整理.csv', encoding= 'unicode_escape')
    accident_data = pd.read_csv('./111_traffic_accident.csv', encoding= 'unicode_escape').drop_duplicates(subset=['X', 'Y'])
    return traffic_data, accident_data

traffic_data, accident_data = get_traffic_accident_data()
accident_coor = accident_data[['X','Y']]
traffic_data['morning_scooter'] = traffic_data['morning_scooter'] / 70
traffic_data['afternoon_scooter'] = traffic_data['afternoon_scooter'] / 70

radius = st.slider('Accident within radius', 100, 1000, 100, 100)
traffic_data['accident_num'] = \
    count_points_within_radius(traffic_data['X'], traffic_data['Y'], accident_data['X'], accident_data['Y'], radius) / 5

show_mode = st.radio("Mode",
                             options=["morning", "afternoon","accident"])

if show_mode == "accident":
    st.pydeck_chart(pdk.Deck(
        map_style=None,
        initial_view_state=pdk.ViewState(
            latitude=25.04,
            longitude=121.54,
            zoom=12.5,
            ),
        layers=[
            pdk.Layer(
                'ScatterplotLayer',
                data=traffic_data,
                get_position='[X, Y]',
                get_color='[255, 209, 26 , 160]',
                get_radius= radius,
            ),
            pdk.Layer(
                'ScatterplotLayer',
                data=accident_coor  ,
                get_position='[X, Y]',
                get_color='[0, 0, 0, 160]',
                get_radius=5,
            )
        ],
    ))
elif show_mode == "morning":
    st.pydeck_chart(pdk.Deck(
        map_style=None,
        initial_view_state=pdk.ViewState(
            latitude=25.04,
            longitude=121.54,
            zoom=12.5,
            ),
        layers=[
            pdk.Layer(
                'ScatterplotLayer',
                data=traffic_data,
                get_position='[X, Y]',
                get_color='[30, 200, 0, 160]',
                get_radius='morning_scooter',
            ),
            pdk.Layer(
                'ScatterplotLayer',
                data=accident_coor  ,
                get_position='[X, Y]',
                get_color='[0, 0, 0, 160]',
                get_radius=5,
            )
        ],  
    ))
elif show_mode == "afternoon":
    st.pydeck_chart(pdk.Deck(
        map_style=None,
        initial_view_state=pdk.ViewState(
            latitude=25.04,
            longitude=121.54,
            zoom=12.5,
            ),
        layers=[
            pdk.Layer(
                'ScatterplotLayer',
                data=traffic_data,
                get_position='[X, Y]',
                get_color='[200, 30, 0, 160]',
                get_radius='afternoon_scooter',
            ), 
            pdk.Layer(
                'ScatterplotLayer',
                data=accident_coor  ,
                get_position='[X, Y]',
                get_color='[0, 0, 0, 160]',
                get_radius=5,
            )
        ],  
    ))