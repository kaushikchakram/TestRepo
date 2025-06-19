# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Options for Dropdown Variables for Task 1:
launch_sites = spacex_df['Launch Site'].value_counts().index
launch_options=(
    [{'label': 'All Sites', 'value': 'ALL'},
    {'label': launch_sites[0], 'value': launch_sites[0]},
    {'label':launch_sites[1],'value':launch_sites[1]},
    {'label':launch_sites[2],'value':launch_sites[2]},
    {'label':launch_sites[3],'value':launch_sites[3]}
    ]
) 
# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(
                                    id='site-dropdown', options =launch_options,
                                    placeholder ='Select a Launch Site Here',
                                    value = 'ALL', searchable = True
                                    ),

                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(
                                    id='payload-slider',
                                    min=0, max=10000, step=1000,
                                    value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ]
    )

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output:
@app.callback(Output(component_id ='success-pie-chart',component_property='figure'),Input(component_id='site-dropdown',component_property='value'))
#Now get pie-chart for Task 2:
def get_pie_chart(launch_options):
    if launch_options == 'ALL':
        all_sites_df = spacex_df.groupby('Launch Site')['class'].mean().reset_index()
        fig = (
            px.pie(all_sites_df, values='class', names='Launch Site',
            title='Success Rate for All Launch Sites')
        )
        return fig
    else:
        # return the outcomes piechart for a selected site
        #filter df:
        filtered_df = spacex_df[['Launch Site','class']].value_counts().reset_index()
        #map 'class' column to 1- 'Success' or 0 - 'Failure':
        filtered_df['class'] = filtered_df['class'].map({0:'Failure',1:'Success'})
        #plot pie:
        fig = (
            px.pie(filtered_df[filtered_df['Launch Site']==launch_options],
            values = 'count',names ='class',
            title = f'Success Rate of Launch Site {launch_options}',
            color ='class',
            color_discrete_map ={'Failure': 'red', 'Success': 'green'})
        )
        
        return fig 
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
# Function decorator to specify function input and output:
@app.callback(Output(
    component_id='success-payload-scatter-chart',component_property='figure'),
    [Input(component_id='site-dropdown',component_property='value'),
    Input(component_id='payload-slider',component_property ='value')
    ]
    )
# Now get scatter plot for Task 4:
def get_scatter_plot(launch_options,value):
    if launch_options == 'ALL':
        fig = px.scatter(
            spacex_df,x='Payload Mass (kg)',y ='class',
            title = 'Payload mass (kg) vs. Success for ALL Launch Sites grouped by Booster Version.',
            color = 'Booster Version Category', range_x =value
        )
        return fig
    else:
        #filter data for launch site and then plot scatter:
        filtered_df = spacex_df[spacex_df['Launch Site']==launch_options]
        fig =px.scatter(
            filtered_df,x='Payload Mass (kg)',y ='class',
            title = f'Payload mass (kg) vs. Success grouped by Booster Version for {launch_options}.',
            color = 'Booster Version Category' , range_x =value
        )
        return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
