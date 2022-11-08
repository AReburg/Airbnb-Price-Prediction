import warnings
warnings.simplefilter(action='ignore')
import pandas as pd
import numpy as np
import geopandas as gpd
import requests
import os
import pickle
import osmnx as ox
import re
from pathlib import Path
from shapely.geometry.polygon import Polygon
from shapely.geometry.multipolygon import MultiPolygon
from shapely import wkt
from scipy import spatial

cwd = Path().resolve()

class GeoData():
    def __int__(self):
        print("init")

    def parse_input(self, text):
        """ """
        # Universit%C3%A4tsring+2,%201010+Wien
        data_json = requests.get(url=f'https://nominatim.openstreetmap.org/search?q={text}&format=json&polygon=1&addressdetails=1').json()
        lat = data_json[0]['lat']
        lon = data_json[0]['lon']
        df = pd.DataFrame({'Location':[text]})
        gdf = gpd.GeoDataFrame(df, geometry=gpd.GeoSeries.from_xy([lon], [lat], crs=self.get_local_utm_crs()))
        return gdf


    def get_tree(self, df):
        try:
            coords = list(zip(df.geometry.apply(lambda x: x.y).values, df.geometry.apply(lambda x: x.x).values))
            tree = spatial.KDTree(coords)
            return tree
        except Exception as e:
            print(e)


    def find_points_closeby(self, tree, lat_lon, k=500, max_distance=500):
        """  """
        results = tree.query((lat_lon), k=k, distance_upper_bound=max_distance)
        zipped_results = list(zip(results[0], results[1]))
        zipped_results = [i for i in zipped_results if i[0] != np.inf]
        return len(zipped_results)


    def get_region(self):
        """  """
        boundary_geojson = gpd.read_file(os.path.join(Path(cwd), 'data', 'geojson', 'vienna.geojson'))
        boundary_geojson.drop(columns=['cartodb_id', 'created_at', 'updated_at'], inplace=True)
        region = boundary_geojson.geometry.unary_union
        return region


    def get_local_utm_crs(self):
        """ Set longitude and latitude of Vienna """
        lon_latitude = 48.210033
        lon_longitude = 16.363449
        local_utm_crs = self.get_local_crs(lon_latitude, lon_longitude)
        return local_utm_crs


    def get_model(self):
        """ load model from .pkl file """
        with open(os.path.join(Path(cwd), 'model', 'xboost.pkl'), 'rb') as f:
            model = pickle.load(f)
        return model


    def get_local_crs(self, y, x):
        """ get local crs """
        x = ox.utils_geo.bbox_from_point((y, x), dist=500, project_utm=True, return_crs=True)
        return x[-1]


    def get_lat_long(self, point):
        """ get latitude and longitude coordinate from POINT geometry """
        try:
            return pd.Series([point.x, point.y])
        except Exception as e:
            pass


    def geo_coordinates(self, df):
        """ import from csv in geopandas dataframe
        source: https://stackoverflow.com/questions/61122875/geopandas-how-to-read-a-csv-and-convert-to-a-geopandas-dataframe-with-polygons
        """
        df['geometry'] = df['geometry'].apply(lambda x: x.centroid if type(x) == Polygon else (x.centroid if type(x) == MultiPolygon else x))
        df[['long', 'lat']] = df.apply(lambda x: self.get_lat_long(x['geometry']), axis=1)
        df = df[df['geometry'].apply(lambda x : x.type=='Point')]
        df = df.to_crs(self.get_local_utm_crs())
        return df

    def import_csv_to_gpd(self, name):
        """ import the csv file a gepandas dataframe """
        df = pd.read_csv(os.path.join(Path(cwd), 'data', 'osm', f'{name}.csv'), sep=",", usecols=['osmid', 'geometry',
                                                                                                      'name'])
        df['geometry'] = df['geometry'].apply(wkt.loads)
        gdf = gpd.GeoDataFrame(df, crs='epsg:4326')
        return self.geo_coordinates(gdf)


    def get_price(self, price_string):
        """ convert the price string into float """
        try:
            price_string = price_string.replace(' ', '')
            pattern = re.compile(r'\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2})?')
            return float(pattern.findall(price_string)[0].replace(',',''))
        except:
            print(price_string)

    def main(self, df, parameters, names):

        df = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude, df.latitude), crs=4326)
        df = df.to_crs(self.get_local_utm_crs())

        for name, i in zip(names, parameters):
            tree = self.get_tree(i)
            df[name] = df.apply(lambda row: self.find_points_closeby(tree, (row.geometry.y, row.geometry.x)), axis=1)

        return df.iloc[:, 4:-1]



    def import_data(self):
        """ import the airbnb data """
        df = pd.read_csv(os.path.join(Path(cwd), 'data', 'listings.csv.gz'), encoding='utf-8')
        df.drop(['listing_url', 'host_picture_url', 'host_verifications', 'host_thumbnail_url', 'host_about', 'neighborhood_overview', 'picture_url', 'scrape_id', 'neighbourhood_group_cleansed', 'calculated_host_listings_count_shared_rooms', 'calculated_host_listings_count_private_rooms','calculated_host_listings_count_entire_homes'], axis=1, inplace=True)
        df = df[['id', 'name','description', 'host_name','host_since', 'host_response_time', 'host_response_rate', 'host_acceptance_rate', 'host_is_superhost','host_listings_count','host_total_listings_count', 'host_has_profile_pic','host_identity_verified', 'neighbourhood', 'neighbourhood_cleansed', 'latitude', 'longitude', 'property_type', 'room_type', 'accommodates', 'bathrooms', 'bathrooms_text', 'bedrooms', 'beds', 'amenities','price']]
        df['neighbourhood'] = df['neighbourhood_cleansed']
        df.drop(['neighbourhood_cleansed'], axis=1, inplace=True)

        df['price'] = df.apply(lambda x: self.get_price(x['price']), axis=1)

        df['neighbourhood'] = df['neighbourhood'].str.replace('Landstra§e', 'Landstraße')
        df['neighbourhood'] = df['neighbourhood'].str.replace('Rudolfsheim-Fnfhaus', 'Rudolfsheim-Fünfhaus')
        df['neighbourhood'] = df['neighbourhood'].str.replace('Dbling', 'Döbling')
        df['neighbourhood'] = df['neighbourhood'].str.replace('Whring', 'Währing')
        # df['neighbourhood'].value_counts()

        # set data types
        df['host_since'] = pd.to_datetime(df['host_since'])
        return df