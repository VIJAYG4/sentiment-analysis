import pandas as pd
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

# ------------------------------------------------------------------------------
# Import and clean data (importing csv into pandas)
df = pd.read_csv("../tweets_labelled/20201210_185210_full_df.csv")
df.reset_index(inplace=True)
print(df[:5])

stock_price_df = pd.read_csv('../aapl.csv')
print("stock price df is ",stock_price_df.head()) 
# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.H1("Sentiment Analysis to predict Stock Trend", style={'text-align': 'center'}),
    
    
    #select Affected by reason
    dcc.Dropdown(id='slct_affectedBy',
                options=[
                    {"label": "Disease", "value":"Disease"},
                    {"label": "Pesticides", "value":"Pesticides"},
                    {"label": "Unknown", "value":"Unknown"}],
                multi=False,
                value='Dec 2',
                style={'width':"40%"} 
                ),

    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='my_bee_map', figure={}),
    html.Br(),
    
    dcc.Graph(
            id='stock_price', 
            figure={
                'data':[
                    {'x':stock_price_df['Date'], 'y':stock_price_df['Open'], 'type':'line', 'name':'Opening price'},
                    {'x':stock_price_df['Date'], 'y':stock_price_df['Close'], 'type':'line', 'name':'Closing price'}
                ],
                'layout':{
                    'title': 'Opening and closing stock prices'
                }
            })

])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='my_bee_map', component_property='figure')],
    [Input(component_id='slct_affectedBy', component_property='value')]
)
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    #container = "The year chosen by user was: {}".format(option_slctd)
    container = "The Affected by reason chosen by user was: {}".format(option_slctd)

    #df processing for line graph
    dff = df.copy()
    dff['sentiment_numbers']=1

    #line graph
    fig = px.pie(
        data_frame=dff,
        names='sentiment',
        values='sentiment_numbers',
        #color='State',
        #hover_name='State',
        template='plotly_dark'
    )
    
    fig.update_layout(
        title_text="Twitter sentiment",
        title_xanchor="center",
        title_font=dict(size=24),
        title_x=0.5,
        showlegend=True
    )

    return container, fig

# def sentiment_chart():
#     dff=df.copy()

#     fig=px.pie(
#         data_frame=dff,
#         names='sentiment',
#         values='sentiment',
#         template='plotly_dark'
#     )
#     fig.update_layout(
#         title_text="Percentage of each sentiment",
#         title_xanchor="center",
#         title_font=dict(size=24),
#         title_x=0.5,
#         showlegend=True
#     )
#     return fig

def stockPrice():
    stock_price_dff = stock_price_df.copy()

    fig=px.line(
        stock_price_dff,
        x='Date',
        y='Open',
    )
    
    fig.update_layout(
        title_text="Opening price of stock",
        title_xanchor="center",
        title_font=dict(size=24),
        title_x=0.5,
        showlegend=True
    )
    return fig 

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)