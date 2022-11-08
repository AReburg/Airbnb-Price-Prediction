import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from pathlib import Path
import geojson
import logging

cwd = Path().resolve()
token = open(os.path.join(Path(cwd), 'assets', '.mapbox_token')).read()


def get_pie_chart(df):
    """ generates the pie chart with the three main genres of the categories """
    fig = go.Figure(data=[go.Pie(values=df.genre.value_counts().to_list(), labels=df.genre.unique(), textinfo='label',
                                      insidetextorientation='radial', hole=.25, marker_colors=night_colors)])
    fig.update_layout(legend_font_size=14, font=dict(family="Open Sans"))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.update(layout_showlegend=False)
    fig.update_traces(marker=dict(line=dict(color='#9c9c9c', width=1.5)))
    fig.update_traces(opacity=0.7)
    return fig


def get_category_chart(df):
    """generates the bar chart of the category distribution from the "direct" genre """
    direct_cate = df[df.genre == 'direct']
    direct_cate_counts = (direct_cate.mean(numeric_only=True) * direct_cate.shape[0]).sort_values(ascending=False)
    direct_cate_names = list(direct_cate_counts.index)

    fig = px.bar(x=[i.replace("_", " ").title() for i in direct_cate_names], y=direct_cate_counts)
    # fig.update_traces(marker_color=night_colors[0], marker_line_color='#9c9c9c', marker_line_width=1, opacity=0.7)
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    fig.update_layout(xaxis={'visible': True, 'showticklabels': True})
    fig.update_layout(yaxis={'visible': True, 'showticklabels': True})
    fig.update_yaxes(tickfont=dict(family='Helvetica', color='#9c9c9c'),
                     title_font_color='#9c9c9c', mirror=True,
                     ticks='outside', showline=True, gridwidth=1, gridcolor='#4c4c4c')
    fig.update_xaxes(tickfont=dict(family='Helvetica', color='#9c9c9c'),
                     title_font_color='#9c9c9c', mirror=True,
                     ticks='outside', showline=True, gridwidth=1, gridcolor='#4c4c4c')
    fig.update_layout(yaxis_title=None, xaxis_title=None)
    return fig


def get_main_chart(df):
    """ generates the horizontal bar chart with the categories """
    fig = px.bar(df, x='val', y='cate', hover_data=['cate'], orientation='h')#, color='color')
    fig.update_layout(xaxis={'visible': False, 'showticklabels': False},
                      yaxis={'visible': True, 'showticklabels': True})
    fig.update_yaxes(tickfont=dict(family='Helvetica', color='#9c9c9c'),
                     title_font_color='#9c9c9c',
                     ticks='outside', showline=True, gridwidth=1, gridcolor='#4c4c4c')
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                      yaxis_title=None)
    fig.update_traces(marker_color=night_colors[0], marker_line_color='#9c9c9c', marker_line_width=1, opacity=0.7)
    return fig


def get_geo_data():
    """ load geojson data """
    cwd = Path().resolve()
    with open(os.path.join(Path(cwd), 'data', 'geojson', 'vienna.geojson'), encoding='utf-8') as fp:
        counties = geojson.load(fp)
    return counties


def heatmap_airbnb(df, title=''):
    """ """
    districts = get_geo_data()
    agg = df.groupby('neighbourhood').agg(nr_listings=('id', 'count')).reset_index().sort_values('nr_listings',
          ascending=False)
    agg['ratio'] = 100 * agg['nr_listings'] / agg['nr_listings'].sum()
    fig = px.choropleth_mapbox(agg, geojson=districts, locations=agg['neighbourhood'],
                               featureidkey="properties.name", color=agg['ratio'],
                               title=title,
                               mapbox_style="open-street-map", zoom=10, center={"lat": 48.210033, "lon": 16.363449},
                               opacity=0.40)

    fig.add_scattermapbox(
        lat=df['latitude'].tolist(),
        lon=df['longitude'].tolist(),
        mode='markers',
        # text=texts,
        marker_size=2,
        marker_color='#F3F5F6',
        opacity=0.9
    )
    fig.update_layout(mapbox_style="light", mapbox_accesstoken=token)
    fig.update_layout(
            font=dict(family="Open Sans"),
            coloraxis_colorbar_title='$/night',
            legend_font_size=14
            )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_yaxes(linewidth=1, linecolor='LightGrey', gridwidth=1, gridcolor='LightGrey', mirror=True,
                     ticks='outside', showline=True)
    return fig

def bar_airbnb(df):
    """generates the bar chart of the category distribution from the "direct" genre """
    night_colors = ['rgb(56, 75, 126)', 'rgb(18, 36, 37)', 'rgb(34, 53, 101)']
    agg = df.groupby('neighbourhood').agg(nr_listings = ('id', 'count')).reset_index().sort_values('nr_listings', ascending=False)
    agg['ratio'] = 100 * agg['nr_listings'] / agg['nr_listings'].sum()

    fig = px.bar(x=agg['neighbourhood'].tolist(), y=agg['ratio'])
    fig.update_traces(marker_color=night_colors[0], marker_line_color='#9c9c9c', marker_line_width=1, opacity=0.7)
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    fig.update_layout(xaxis={'visible': True, 'showticklabels': True})
    fig.update_layout(yaxis={'visible': True, 'showticklabels': True})
    fig.update_yaxes(tickfont=dict(family='Helvetica', color='#9c9c9c'),
                     title_font_color='#9c9c9c', mirror=True,
                     ticks='outside', showline=True, gridwidth=1, gridcolor='#4c4c4c')
    fig.update_xaxes(tickfont=dict(family='Helvetica', color='#9c9c9c'),
                     title_font_color='#9c9c9c', mirror=True,
                     ticks='outside', showline=True, gridwidth=1, gridcolor='#4c4c4c')
    fig.update_layout(yaxis_title=None, xaxis_title=None)
    return fig
