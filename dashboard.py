import dash
from dash import html
from dash import dcc
from dash import dash_table
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
        html.Div(id='summary_table')
    ]
)


@app.callback(
    Output(component_id='summary_table', component_property= 'children'),
    [
        Input(component_id='tab_policy_dropdown', component_property= 'value')
    ]
)
def update_summary_table(dropdown_value):
    print(dropdown_value)
    if dropdown_value == "uniform_random":
        df_query = ur_df.copy()
    elif dropdown_value == "thompson_sampling_contextual":
        df_query = tsc_df.copy()
    else:
        df_query = df.copy()

    if dropdown_value == "__all__":
        df_query = df_query.groupby(["arm"]).agg({
            "arm": ["first", "count"],
            "modular_link_mha_prototype_linkrating": ["mean", "std", "sem", "count"]
        })
    else:
        df_query = df_query.groupby(["policy", "arm"]).agg({
            "policy": ["first"],
            "arm": ["first", "count"],
            "modular_link_mha_prototype_linkrating": ["mean", "std", "sem", "count"]
        })

    return [dash_table.DataTable(
            columns=[{"name": [item if item != "first" else "" for item in list(i)], "id": '_'.join(i)} for i in df_query.columns],
            data=[ {"_".join(col): round(val, 3) if isinstance(val, float) else val for col, val in row.items() } for row in df_query.to_dict('records') ],
            merge_duplicate_headers=True,
        )
    ]


if __name__ == '__main__': 
    app.run_server()