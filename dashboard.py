import dash
from dash import html
from dash import dcc
import plotly.graph_objects as go
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd


app = dash.Dash()

# df = px.data.stocks()

xls = pd.ExcelFile('datasets/Modular_Link_MHA_Prototype.xlsx')
ur_df = pd.read_excel(xls, 'UR_0')
tsc_df = pd.read_excel(xls, 'TSC_4')
df = pd.concat([ur_df, tsc_df])

app.layout = html.Div(
    id = 'parent', children = [
        html.H1(
            id = 'H1',
            children = 'Testing Modular Link Table',
            style = {
                'textAlign':'center',
                'marginTop':40,
                'marginBottom':40
            }
        ),
        dcc.Dropdown(
            id = 'tab_policy_dropdown',
            options = [
                {'label': 'Uniform Random', 'value': 'uniform_random' },
                {'label': 'TS Contextual', 'value': 'thompson_sampling_contextual'},
                {'label': 'All Policies', 'value': '__any__'},
                {'label': 'All Data', 'value': '__all__'},
                ],
            value = '__all__'
        ),
        dcc.Graph(id = 'summary_table')
    ]
)


@app.callback(Output(component_id='bar_plot', component_property= 'figure'),
              [Input(component_id='dropdown', component_property= 'value')])
def graph_update(dropdown_value):
    print(dropdown_value)
    # GROUP BY (Given policy, contextual)
    fig = go.Figure([
        go.Scatter(
            x = df['date'],
            y = df['{}'.format(dropdown_value)],
            line = dict(color = 'firebrick', width = 4)
        )
    ])

    fig.update_layout(
        title = 'Stock prices over time',
        xaxis_title = 'Dates',
        yaxis_title = 'Prices'
    )
    return fig  



if __name__ == '__main__': 
    app.run_server()