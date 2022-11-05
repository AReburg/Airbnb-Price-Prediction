# import modules/libraries
import warnings
warnings.simplefilter(action='ignore')
import pandas as pd
import numpy as np
import geopandas as gpd
import time
import os
import pickle
import geojson
import plotly.express as px
from sqlalchemy import create_engine
import re
import sqlite3
from pathlib import Path
from shapely.geometry.polygon import Polygon
from shapely.geometry.multipolygon import MultiPolygon


cwd = Path().resolve()

def get_price(price_string):
    """ convert the price string into float """
    try:
        price_string = price_string.replace(' ', '')
        pattern = re.compile(r'\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2})?')
        return float(pattern.findall(price_string)[0].replace(',',''))
    except:
        print(price_string)

def import_data():
    """ import the airbnb data """
    df = pd.read_csv(os.path.join(Path(cwd), 'data', 'listings.csv.gz'), encoding='utf-8')
    df.drop(['listing_url', 'host_picture_url', 'host_verifications', 'host_thumbnail_url', 'host_about', 'neighborhood_overview', 'picture_url', 'scrape_id', 'neighbourhood_group_cleansed', 'calculated_host_listings_count_shared_rooms', 'calculated_host_listings_count_private_rooms','calculated_host_listings_count_entire_homes'], axis=1, inplace=True)
    df = df[['id', 'name','description', 'host_name','host_since', 'host_response_time', 'host_response_rate', 'host_acceptance_rate', 'host_is_superhost','host_listings_count','host_total_listings_count', 'host_has_profile_pic','host_identity_verified', 'neighbourhood', 'neighbourhood_cleansed', 'latitude', 'longitude', 'property_type', 'room_type', 'accommodates', 'bathrooms', 'bathrooms_text', 'bedrooms', 'beds', 'amenities','price']]
    df['neighbourhood'] = df['neighbourhood_cleansed']
    df.drop(['neighbourhood_cleansed'], axis=1, inplace=True)
    df_cal = pd.read_csv(os.path.join(Path(cwd), 'data', 'calendar.csv'), index_col=False, sep=",")
    df_rev = pd.read_csv(os.path.join(Path(cwd), 'data', 'reviews.csv'), index_col=False, sep=",")

    df['price'] = df.apply(lambda x: get_price(x['price']), axis=1)

    df['neighbourhood'] = df['neighbourhood'].str.replace('Landstra§e', 'Landstraße')
    df['neighbourhood'] = df['neighbourhood'].str.replace('Rudolfsheim-Fnfhaus', 'Rudolfsheim-Fünfhaus')
    df['neighbourhood'] = df['neighbourhood'].str.replace('Dbling', 'Döbling')
    df['neighbourhood'] = df['neighbourhood'].str.replace('Whring', 'Währing')
    # df['neighbourhood'].value_counts()

    # set data types
    df_cal['date'] = pd.to_datetime(df_cal['date'])
    df_rev['date'] = pd.to_datetime(df_rev['date'])
    df['host_since'] = pd.to_datetime(df['host_since'])

    return df