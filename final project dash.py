# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 21:48:56 2022

@author: Asira
"""
# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
airline_data =  pd.read_csv('spacex_launch_dash.csv')

# Create a dash application
app = dash.Dash(__name__)
sites=list(airline_data['Launch Site'].unique())
print(sites)
min_payload=airline_data['Payload Mass (kg)'].min()

max_payload=airline_data['Payload Mass (kg)'].max()
# Build dash app layout
app.layout = html.Div(children=[ html.H1('SpaceX Falcon 9 Launch data', 
                                style={'textAlign': 'center', 'color': '#503D36',
                                'font-size': 24}),
                                
                                html.Div([
                                    dcc.Dropdown(id='input-type1',options=[ {'label': 'All Sites', 'value': 'ALL'},
                                                                           {'label':'CCAFS LC-40',
                                                                           'value':'CCAFS LC-40'},
                                                                              {'label':'VAFB SLC-4E',
                                                                            'value':'VAFB SLC-4E'},
                                                                              {'label':'KSC LC-39A',
                                                                            'value':'KSC LC-39A'},
                                                                           {'label':'CCAFS SLC-40',
                                                                            'value':'CCAFS SLC-40'}],
                                                 placeholder=' Select a Launch Site here',searchable=True,value='ALL',style={'width':'80%', 'font-size': '20px','textAlign':'center','padding':'3px'}),
                                   ]),
                               
                                
                                # Segment 1
                                html.Div([
                                        html.Div(dcc.Graph(id='success-plot'))]),
                                html.Div(dcc.RangeSlider(id='payload',
                min=0, max=10000, step=1000,
                marks={0: '0',
                       1000: '1000',
                      2000: '2000',
                              
                       3000: '3000',
                       4000: '4000',
                       5000: '5000',
                               6000: '6000',
                               7000: '7000',
                               8000:'8000',9000:'9000',10000:'10000'},
                
                value=[min_payload, max_payload])),html.Br(),html.Br(),
                                html.Div(dcc.Graph(id='scatter'))
                                       ])
                                # Segment 2
                                
                                # Segment 3
                                

""" Compute_info function description

This function takes in airline data and selected year as an input and performs computation for creating charts and plots.

Arguments:
    airline_data: Input airline data.
    entered_year: Input year for which computation needs to be performed.

Returns:
    Computed average dataframes for carrier delay, weather delay, NAS delay, security delay, and late aircraft delay.

"""
def compute_info(airline_data,site,payload):
    
    # Compute delay averages
    if site=='ALL':
        df=airline_data.groupby('Launch Site').sum()[['class']]
        df.reset_index(inplace=True)
        scat=airline_data[['class','Booster Version','Payload Mass (kg)']]
        scat=scat[(scat['Payload Mass (kg)']).astype('int')>=payload[0]]
        scat=scat[(scat['Payload Mass (kg)']).astype('int')<=payload[1]]
    else:
        if site=='CCAFS LC-40':
            df=airline_data[airline_data['Launch Site']=='CCAFS LC-40'][['Launch Site','class']]
            df=df.groupby('class').count()
            df.reset_index(inplace=True)
            scat=airline_data[['class','Booster Version','Payload Mass (kg)','Launch Site']]
            scat=scat[(scat['Payload Mass (kg)']).astype('int')>=payload[0]]
            scat=scat[(scat['Payload Mass (kg)']).astype('int')<=payload[1]]
            scat=scat[scat['Launch Site']=='CCAFS LC-40']
        elif site=='CCAFS SLC-40':
            df=airline_data[airline_data['Launch Site']=='CCAFS SLC-40'][['Launch Site','class']]
            df=df.groupby('class').count()
            df.reset_index(inplace=True)
            scat=airline_data[['class','Booster Version','Payload Mass (kg)','Launch Site']]
            scat=scat[(scat['Payload Mass (kg)']).astype('int')>=payload[0]]
            scat=scat[(scat['Payload Mass (kg)']).astype('int')<=payload[1]]
            scat=scat[scat['Launch Site']=='CCAFS SLC-40']
        elif site=='KSC LC-39A':
            df=airline_data[airline_data['Launch Site']=='KSC LC-39A'][['Launch Site','class']]
            df=df.groupby('class').count()
            df.reset_index(inplace=True)
            scat=airline_data[['class','Booster Version','Payload Mass (kg)','Launch Site']]
            scat=scat[(scat['Payload Mass (kg)']).astype('int')>=payload[0]]
            scat=scat[(scat['Payload Mass (kg)']).astype('int')<=payload[1]]
            scat=scat[scat['Launch Site']=='KSC LC-39A']
        elif site=='VAFB SLC-4E':
            df=airline_data[airline_data['Launch Site']=='VAFB SLC-4E'][['Launch Site','class']]
            df=df.groupby('class').count()
            df.reset_index(inplace=True)
            scat=airline_data[['class','Booster Version','Payload Mass (kg)','Launch Site']]
            scat=scat[(scat['Payload Mass (kg)']).astype('int')>=payload[0]]
            scat=scat[(scat['Payload Mass (kg)']).astype('int')<=payload[1]]
            scat=scat[scat['Launch Site']=='VAFB SLC-4E']
    return df,scat
"""Callback Function

Function that returns fugures using the provided input year.

Arguments:

    entered_year: Input year provided by the user.

Returns:

    List of figures computed using the provided helper function `compute_info`.
"""
# Callback decorator
@app.callback( 
              [ Output(component_id='success-plot', component_property='figure'),
              
               Output(component_id='scatter', component_property='figure')]
              ,Input(component_id='input-type1',component_property='value'),
              Input(component_id='payload',component_property='value')
               )
# Computation to callback function and return graph
def get_graph(site,payload):
    df,scat=compute_info(airline_data,site,payload)
    # Compute required information for creating graph from the data
    if site=='ALL':
        fig=px.pie(data_frame=df,names='Launch Site',values='class',title='Success rate of each Launch site')
    
        scatter=px.scatter(data_frame=scat,x='Payload Mass (kg)',y='class',color='Booster Version')
    else:
        fig=px.pie(data_frame=df,values='Launch Site',names='class',title='Success rate of %s Launch site'%site)
        scatter=px.scatter(data_frame=scat,x='Payload Mass (kg)',y='class',color='Booster Version')
    return fig,scatter

# Run the app
if __name__ == '__main__':
    app.run_server()