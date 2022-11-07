import dash
from dash import html
from dash import dcc
from dash import dash_table
import plotly.graph_objects as go
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd
import requests
from config import TOKEN
import json


app = dash.Dash()

# df = px.data.stocks()

mooclet_id = [315, 295, 316]


# Get mooclet policy name and corresponding contextual variable.
mooclet = {}
context_var = {}
outcome_var = {}
for id in mooclet_id:
    mooclet_url = 'https://mooclet.canadacentral.cloudapp.azure.com/engine/api/v1/mooclet/' + \
        str(id)
    mresponse = requests.get(url=mooclet_url, headers={
                             'Authorization': TOKEN})
    name = mresponse.json()['name']
    mooclet[id] = name
    print(mooclet)
    cv_url = 'https://mooclet.canadacentral.cloudapp.azure.com/engine/api/v1/policyparameters?mooclet=' + \
        str(id) + '&policy=6'
    dresponse = requests.get(url=cv_url, headers={
                             'Authorization': TOKEN})
    context_var[name] = dresponse.json(
    )['results'][0]['parameters']['contextual_variables']  # Add Try/catch / if else for edge case handle
    context_var[name].remove('version')
    outcome_var[name] = dresponse.json(
    )['results'][0]['parameters']['outcome_variable']  # Add Try/catch / if else for edge case handle

# Generate Mooclet Option List
mooclet_option = []
for m in mooclet:
    option = {}
    option['label'] = mooclet[m]
    option['value'] = m
    print(option)
    mooclet_option.append(option)

xls = pd.ExcelFile('datasets/Modular_Link_MHA_Prototype.xlsx')
ur_df = pd.read_excel(xls, 'UR_0')
tsc_df = pd.read_excel(xls, 'TSC_4')
df = pd.concat([ur_df, tsc_df])

# # 315
# mlmxls = pd.ExcelFile('datasets/Modular_Link_MHA_Prototype.xlsx')
# mlmur_df = pd.read_excel(mlmxls, 'UR_0')
# mlmtsc_df = pd.read_excel(mlmxls, 'TSC_4')
# mlmdf = pd.concat([mlmur_df, mlmtsc_df])

# # 295
# mhaxls = pd.ExcelFile('datasets/MHAwave1ModularRationale.xlsx')
# mhaur_df = pd.read_excel(mhaxls, 'UR_0')
# mhatsc_df = pd.read_excel(mhaxls, 'TSC_4')
# mhadf = pd.concat([mhaur_df, mhatsc_df])

# # 316
# mimxls = pd.ExcelFile('datasets/Modular_Interaction_MHA_Prototype.xlsx')
# mimur_df = pd.read_excel(mimxls, 'UR_0')
# mimtsc_df = pd.read_excel(mimxls, 'TSC_4')
# mimdf = pd.concat([mimur_df, mimtsc_df])

xls = pd.ExcelFile('datasets/Modular_Link_MHA_Prototype.xlsx')
ur_df = pd.read_excel(xls, 'UR_0')
tsc_df = pd.read_excel(xls, 'TSC_4')
df = pd.concat([ur_df, tsc_df])

app.layout = html.Div(
    id='parent', children=[
        html.H1(
            id='H1',
            children='Testing Modular Link Table',
            style={
                'textAlign': 'center',
                'marginTop': 40,
                'marginBottom': 40
            }
        ),
        html.H2(
            id='change_mooclet',
            children='Change Mooclet',
            style={
                'textAlign': 'left',
                'marginBottom': 20
            }
        ),
        dcc.Dropdown(
            id='tab_mooclet_dropdown',
            options=mooclet_option,
            value=315
        ),
        html.H2(
            id='change_policy',
            children='Change Policy',
            style={
                'textAlign': 'left',
                'marginBottom': 20
            }
        ),
        dcc.Dropdown(
            id='tab_policy_dropdown',
            options=[
                {'label': 'Uniform Random', 'value': 'uniform_random'},
                {'label': 'TS Contextual', 'value': 'thompson_sampling_contextual'},
                {'label': 'All Policies', 'value': '__any__'},
                {'label': 'All Data', 'value': '__all__'},
            ],
            value='__all__'
        ),
        html.Div(
            id='summary_table',
            style={
                'marginTop': 20,
                'marginBottom': 20
            }
        )
        # html.H2(
        #     id='change_arm',
        #     children='Change Arm',
        #     style={
        #         'textAlign': 'left',
        #         'marginBottom': 20
        #     }
        # ),
        # dcc.Dropdown(
        #     id='tab_arm_dropdown',
        #     options=[{"label": arm, "value": arm} for idx, arm in enumerate(df["arm"].unique().tolist())] +
        #     [{'label': 'All Arms', 'value': '__all__'}],
        #     value='__all__'
        # ),
        # dcc.Graph(id='summary_reward_bar_plot')
    ]
)


@app.callback(
    Output(component_id='selected_mooclet_data', component_property='data'),
    [
        Input(component_id='tab_mooclet_dropdown', component_property='value')
    ]
)
def update_selected_mooclet(mooclet_dropdown_value):
    print(mooclet_dropdown_value)
    if mooclet_dropdown_value == 315:
        xls = pd.ExcelFile('datasets/Modular_Link_MHA_Prototype.xlsx')
        ur_df = pd.read_excel(xls, 'UR_0')
        tsc_df = pd.read_excel(xls, 'TSC_4')
        df = pd.concat([ur_df, tsc_df])
    elif mooclet_dropdown_value == 295:
        xls = pd.ExcelFile('datasets/MHAwave1ModularRationale.xlsx')
        ur_df = pd.read_excel(xls, 'UR_0')
        tsc_df = pd.read_excel(xls, 'TSC_4')
        df = pd.concat([ur_df, tsc_df])
    elif mooclet_dropdown_value == 316:
        xls = pd.ExcelFile('datasets/Modular_Interaction_MHA_Prototype.xlsx')
        ur_df = pd.read_excel(xls, 'UR_0')
        tsc_df = pd.read_excel(xls, 'TSC_4')
        df = pd.concat([ur_df, tsc_df])
    datasets = {
        'ur_df': ur_df.to_json(orient='split', date_format='iso'),
        'tsc_df': tsc_df.to_json(orient='split', date_format='iso'),
        'df': df.to_json(orient='split', date_format='iso'),
    }
    return json.dumps(datasets)


@app.callback(
    Output(component_id='summary_table', component_property='children'),
    [
        # Input(component_id='selected_mooclet_data', component_property='data'),
        Input(component_id='tab_policy_dropdown', component_property='value')
    ]
)
def update_summary_table(dropdown_value):
    # print(dropdown_value)
    # datasets = json.loads(mooclet_data)
    # if dropdown_value == "uniform_random":
    #     df_query = datasets["ur_df"].copy()
    # elif dropdown_value == "thompson_sampling_contextual":
    #     df_query = datasets["tsc_df"].copy()
    # else:
    #     df_query = datasets["df"].copy()

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
            columns=[{"name": [item if item != "first" else "{} name".format(
                i[0]) for item in list(i)], "id": '_'.join(i)} for i in df_query.columns],
            data=[{"_".join(col): round(val, 3) if isinstance(
                val, float) else val for col, val in row.items()} for row in df_query.to_dict('records')],
            merge_duplicate_headers=True,
            sort_action='native',
            )
            ]


# @app.callback(
#     Output(component_id='summary_reward_bar_plot',
#            component_property='figure'),
#     [
#         Input(component_id='tab_policy_dropdown', component_property='value'),
#         Input(component_id='tab_arm_dropdown', component_property='value')
#     ]
# )
# def update_summary_reward_bar_plot(policy_dropdown_value, arm_dropdown_value):
#     print(policy_dropdown_value, arm_dropdown_value)
#     if policy_dropdown_value == "uniform_random":
#         df_query = ur_df.copy()
#     elif policy_dropdown_value == "thompson_sampling_contextual":
#         df_query = tsc_df.copy()
#     else:
#         df_query = df.copy()

#     if arm_dropdown_value == "__all__":
#         df_query = df_query.groupby(["modular_link_mha_prototype_linkrating"]).agg({
#             "modular_link_mha_prototype_linkrating": ["first", "count"]
#         })
#     else:
#         df_query = df_query.groupby(["arm", "modular_link_mha_prototype_linkrating"]).agg({
#             "arm": ["first"],
#             "modular_link_mha_prototype_linkrating": ["first", "count"]
#         })
#         df_query = df_query[df_query[("arm", "first")] == arm_dropdown_value]

#     fig = go.Figure(
#         [
#             go.Bar(
#                 x=df_query[("modular_link_mha_prototype_linkrating", "first")],
#                 y=df_query[("modular_link_mha_prototype_linkrating", "count")],
#                 marker=dict(color=df_query[(
#                     "modular_link_mha_prototype_linkrating", "first")], colorscale='viridis')
#             )
#         ]
#     )

#     fig.layout.xaxis2 = go.layout.XAxis(
#         overlaying="x", range=[0, 1], showticklabels=False)

#     fig.update_layout(
#         title='Reward Distribution',
#         xaxis_title='Reward Value',
#         yaxis_title='Reward Count'
#     )

#     return fig


if __name__ == '__main__':
    app.run_server()
