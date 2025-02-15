######### Import your libraries #######
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly as py
import plotly.graph_objs as go


###### Define your variables #####
tabtitle = 'Titanic!'
color1='#92A5E8'
color2='#8E44AD'
color3='#FFC300'
sourceurl = 'https://git.generalassemb.ly/intuit-ds-15/05-cleaning-combining-data/blob/master/data/drinks.csv'
githublink = 'https://github.com/dpulluri/304-titanic-dropdown'


###### Import a dataframe #######
df = pd.read_csv("assets/drinks.csv", keep_default_na=False)
#df['Female']=df['Sex'].map({'male':0, 'female':1})
#df['Cabin Class'] = df['Pclass'].map({1:'first', 2: 'second', 3:'third'})
variables_list=['beer_servings', 'spirit_servings', 'wine_servings', 'total_litres_of_pure_alcohol']

########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

####### Layout of the app ########
app.layout = html.Div([
    html.H3('Choose a continuous variable for summary statistics:'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in variables_list],
        value=variables_list[0]
    ),
    html.Br(),
    dcc.Graph(id='display-value'),
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A("Data Source", href=sourceurl),
])


######### Interactive callbacks go here #########
@app.callback(Output('display-value', 'figure'),
              [Input('dropdown', 'value')])
def display_value(continuous_var):
    results = df.groupby(['continent']).sum().reset_index()

    # Create a grouped bar chart
    mydata1 = go.Bar(
        x=results.continent,
        y=results[continuous_var],
        marker=dict(color=color1)
    )
    mylayout = go.Layout(
        title='Grouped bar chart',
        xaxis = dict(title = 'Continent'), # x-axis label
        yaxis = dict(title = str(continuous_var)), # y-axis label

    )
    fig = go.Figure(data=[mydata1], layout=mylayout)
    return fig


######### Run the app #########
if __name__ == '__main__':
    app.run_server(debug=True)
