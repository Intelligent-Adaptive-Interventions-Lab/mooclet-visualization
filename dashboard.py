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

mooclet_id = [315, 295]

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
    context_var[id] = dresponse.json(
    )['results'][0]['parameters']['contextual_variables']  # Add Try/catch / if else for edge case handle
    context_var[id].remove('version')
    outcome_var[id] = dresponse.json(
    )['results'][0]['parameters']['outcome_variable']  # Add Try/catch / if else for edge case handle


# Read in all the data - hardcoded for now
# 315
mlmxls = pd.ExcelFile('datasets/Modular_Link_MHA_Prototype.xlsx')
mlmrv = outcome_var[315]
mlmur_df = pd.read_excel(mlmxls, 'UR_0')
mlmur_df.loc[mlmur_df[mlmrv] <= 1, mlmrv]  = mlmur_df[mlmrv]*4 + 1
mlmtsc_df = pd.read_excel(mlmxls, 'TSC_4')
mlmtsc_df.loc[mlmtsc_df[mlmrv] <= 1, mlmrv]  = mlmtsc_df[mlmrv]*4 + 1
mlmdf = pd.concat([mlmur_df, mlmtsc_df])

# 295
mhaxls = pd.ExcelFile('datasets/MHAwave1ModularRationale.xlsx')
mharv = outcome_var[295]
mhaur_df = pd.read_excel(mhaxls, 'UR_0')
mhaur_df.loc[mhaur_df[mharv] <= 1, mharv]  = mhaur_df[mharv]*4 + 1
mhatsc_df = pd.read_excel(mhaxls, 'TSC_4')
mhatsc_df.loc[mhatsc_df[mharv] <= 1, mharv]  = mhatsc_df[mharv]*4 + 1
mhadf = pd.concat([mhaur_df, mhatsc_df])

# # 316 Comment out for now as 316 has null handle issue
# mimxls = pd.ExcelFile('datasets/Modular_Interaction_MHA_Prototype.xlsx')
# mimur_df = pd.read_excel(mimxls, 'UR_0')
# mimtsc_df = pd.read_excel(mimxls, 'TSC_4')
# mimdf = pd.concat([mimur_df, mimtsc_df])

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
            options=[{"label": mooclet[moocletid], "value": moocletid}
                     for moocletid in mooclet],
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
            id='tab_time_change',
            children=[
                dcc.RadioItems(
                    ['US/Central', 'US/Eastern'],
                    'US/Central',
                    id='tab_timezone_change_type',
                    inline=True
                ),
                dcc.RadioItems(
                    ['week', 'day'],
                    'week',
                    id='tab_timerange_change_type',
                    inline=True
                )
            ],
            style={
                'display': 'inline-block',
                'marginTop': 20,
                'marginBottom': 20
            }
        ),
        html.Div(
            id='tab_time_slider_div',
            style={
                'textAlign': 'center',
            }
        ),
        html.Div(
            id='summary_table',
            style={
                'marginTop': 20,
                'marginBottom': 20
            }
        ),
        html.H2(
            id='change_arm',
            children='Change Arm',
            style={
                'textAlign': 'left',
                'marginBottom': 20
            }
        ),
        html.Div(
            id='tab_arm_dropdown_div'
        ),
        html.Div(
            id='summary_reward_time_change',
            children=[
                dcc.RadioItems(
                    ['US/Central', 'US/Eastern'],
                    'US/Central',
                    id='summary_reward_timezone_change_type',
                    inline=True
                ),
                dcc.RadioItems(
                    ['week', 'day'],
                    'week',
                    id='summary_reward_timerange_change_type',
                    inline=True
                )
            ],
            style={
                'display': 'inline-block',
                'marginTop': 20,
                'marginBottom': 20
            }
        ),
        html.Div(
            id='summary_reward_time_slider_div',
            style={
                'textAlign': 'center',
                'marginBottom': 5
            }
        ),
        dcc.Graph(id='summary_reward_bar_plot'),
        html.Div(
            id='tab_context_dropdown_div'
        ),
        html.Div(
            id='summary_context_time_change',
            children=[
                dcc.RadioItems(
                    ['US/Central', 'US/Eastern'],
                    'US/Central',
                    id='summary_context_timezone_change_type',
                    inline=True
                ),
                dcc.RadioItems(
                    ['week', 'day'],
                    'week',
                    id='summary_context_timerange_change_type',
                    inline=True
                )
            ],
            style={
                'display': 'inline-block',
                'marginTop': 20,
                'marginBottom': 20
            }
        ),
        html.Div(
            id='summary_context_time_slider_div',
            style={
                'textAlign': 'center',
                'marginBottom': 5
            }
        ),
        dcc.Graph(id='summary_context_bar_plot'),

        dcc.Store(id='selected_mooclet_data')
    ]
)


@app.callback(
    Output(component_id='selected_mooclet_data', component_property='data'),
    Input(component_id='tab_mooclet_dropdown', component_property='value')
)
def update_selected_mooclet(mooclet_dropdown_value):
    print(mooclet_dropdown_value)
    if mooclet_dropdown_value == 315:
        ur_df = mlmur_df
        tsc_df = mlmtsc_df
        df = mlmdf
    elif mooclet_dropdown_value == 295:
        ur_df = mhaur_df
        tsc_df = mhatsc_df
        df = mhadf
    # elif mooclet_dropdown_value == 316:
    #     ur_df = mimur_df
    #     tsc_df = mimtsc_df
    #     df = mimdf
    datasets = {
        'ur_df': ur_df.to_json(orient='split', date_format='iso'),
        'tsc_df': tsc_df.to_json(orient='split', date_format='iso'),
        'df': df.to_json(orient='split', date_format='iso'),
        'cv': context_var[mooclet_dropdown_value],
        'rv': outcome_var[mooclet_dropdown_value]
    }
    return json.dumps(datasets)


@app.callback(
    Output(component_id='summary_table', component_property='children'),
    [
        Input(component_id='selected_mooclet_data', component_property='data'),
        Input(component_id='tab_policy_dropdown', component_property='value'),
        Input(component_id='tab_timezone_change_type',
              component_property='value'),
        Input(component_id='tab_timerange_change_type',
              component_property='value'),
        Input(component_id='tab_time_slider', component_property='value')
    ]
)
def update_summary_table(df, dropdown_value, tab_timezone_change_type, tab_timerange_change_type, tab_time_slider):
    print(dropdown_value, tab_timezone_change_type,
          tab_timerange_change_type, tab_time_slider)
    ds = json.loads(df)

    if dropdown_value == "uniform_random":
        df_query = pd.read_json(ds['ur_df'], orient='split')
    elif dropdown_value == "thompson_sampling_contextual":
        df_query = pd.read_json(ds['tsc_df'], orient='split')
    else:
        df_query = pd.read_json(ds['df'], orient='split')

    reward_var = ds['rv']
    print('rv')
    print(reward_var)

    # df_query = df_query.dropna(subset=['reward_create_time'])
    df_query['reward_create_time'] = pd.to_datetime(
        df_query['reward_create_time']).dt.tz_convert(tab_timezone_change_type)
    df_query['arm_assign_time'] = pd.to_datetime(
        df_query['arm_assign_time']).dt.tz_convert(tab_timezone_change_type)

    day_offset = 7 if tab_timerange_change_type == "week" else 1

    last_reward_idx = df_query['reward_create_time'].last_valid_index()
    last_arm_idx = -1

    if last_reward_idx is not None and df_query['reward_create_time'].iloc[last_reward_idx] > df_query['arm_assign_time'].iloc[last_arm_idx]:
        time_range = pd.date_range(
            start=df_query['arm_assign_time'].iloc[0] -
            pd.offsets.Day(day_offset),
            end=df_query['reward_create_time'].iloc[last_reward_idx] +
            pd.offsets.Day(day_offset),
            tz=tab_timezone_change_type,
            freq=f"{day_offset}D",
            inclusive="right"
        )
    else:
        time_range = pd.date_range(
            start=df_query['arm_assign_time'].iloc[0] -
            pd.offsets.Day(day_offset),
            end=df_query['arm_assign_time'].iloc[last_arm_idx] +
            pd.offsets.Day(day_offset),
            tz=tab_timezone_change_type,
            freq=f"{day_offset}D",
            inclusive="right"
        )

    df_query = df_query.loc[
        (df_query['arm_assign_time'] >= str(time_range[tab_time_slider[0]])) &
        (df_query['arm_assign_time'] < str(time_range[tab_time_slider[1]]))
    ]

    if dropdown_value == "__all__":
        df_query = df_query.groupby(["arm"]).agg({
            "arm": ["first", "count"],
            reward_var: ["mean", "std", "sem", "count"]
        })
    else:
        df_query = df_query.groupby(["policy", "arm"]).agg({
            "policy": ["first"],
            "arm": ["first", "count"],
            reward_var: ["mean", "std", "sem", "count"]
        })

    return [
        dash_table.DataTable(
            columns=[{"name": [item if item != "first" else "{} name".format(
                i[0]) for item in list(i)], "id": '_'.join(i)} for i in df_query.columns],
            data=[{"_".join(col): round(val, 3) if isinstance(
                val, float) else val for col, val in row.items()} for row in df_query.to_dict('records')],
            merge_duplicate_headers=True,
            sort_action='native',
        )
    ]


@app.callback(
    Output(component_id='summary_reward_bar_plot',
           component_property='figure'),
    [
        Input(component_id='selected_mooclet_data', component_property='data'),
        Input(component_id='tab_policy_dropdown', component_property='value'),
        Input(component_id='tab_arm_dropdown', component_property='value'),
        Input(component_id='summary_reward_timezone_change_type',
              component_property='value'),
        Input(component_id='summary_reward_timerange_change_type',
              component_property='value'),
        Input(component_id='summary_reward_time_slider',
              component_property='value')
    ]
)
def update_summary_reward_bar_plot(df, policy_dropdown_value, arm_dropdown_value, summary_reward_timezone_change_type, summary_reward_timerange_change_type, summary_reward_time_slider):
    print(policy_dropdown_value, arm_dropdown_value)
    ds = json.loads(df)
    if policy_dropdown_value == "uniform_random":
        df_query = pd.read_json(ds['ur_df'], orient='split')
    elif policy_dropdown_value == "thompson_sampling_contextual":
        df_query = pd.read_json(ds['tsc_df'], orient='split')
    else:
        df_query = pd.read_json(ds['df'], orient='split')

    reward_var = ds['rv']

    # df_query = df_query.dropna(subset=['reward_create_time'])
    df_query['reward_create_time'] = pd.to_datetime(
        df_query['reward_create_time']).dt.tz_convert(summary_reward_timezone_change_type)
    df_query['arm_assign_time'] = pd.to_datetime(
        df_query['arm_assign_time']).dt.tz_convert(summary_reward_timezone_change_type)

    day_offset = 7 if summary_reward_timerange_change_type == "week" else 1

    last_reward_idx = df_query['reward_create_time'].last_valid_index()
    last_arm_idx = -1

    if last_reward_idx is not None and df_query['reward_create_time'].iloc[last_reward_idx] > df_query['arm_assign_time'].iloc[last_arm_idx]:
        time_range = pd.date_range(
            start=df_query['arm_assign_time'].iloc[0] -
            pd.offsets.Day(day_offset),
            end=df_query['reward_create_time'].iloc[last_reward_idx] +
            pd.offsets.Day(day_offset),
            tz=summary_reward_timezone_change_type,
            freq=f"{day_offset}D",
            inclusive="right"
        )
    else:
        time_range = pd.date_range(
            start=df_query['arm_assign_time'].iloc[0] -
            pd.offsets.Day(day_offset),
            end=df_query['arm_assign_time'].iloc[last_arm_idx] +
            pd.offsets.Day(day_offset),
            tz=summary_reward_timezone_change_type,
            freq=f"{day_offset}D",
            inclusive="right"
        )

    df_query = df_query.loc[
        (df_query['arm_assign_time'] >= str(time_range[summary_reward_time_slider[0]])) &
        (df_query['arm_assign_time'] < str(
            time_range[summary_reward_time_slider[1]]))
    ]

    if arm_dropdown_value == "__all__":
        df_query = df_query.groupby([reward_var]).agg({
            reward_var: ["first", "count"]
        })
    else:
        df_query = df_query.groupby(["arm", reward_var]).agg({
            "arm": ["first"],
            reward_var: ["first", "count"]
        })
        df_query = df_query[df_query[("arm", "first")] == arm_dropdown_value]

    fig = go.Figure(
        [
            go.Bar(
                x=df_query[(reward_var, "first")],
                y=df_query[(reward_var, "count")],
                marker=dict(color=df_query[(
                    reward_var, "first")], colorscale='viridis')
            )
        ]
    )

    fig.layout.xaxis2 = go.layout.XAxis(
        overlaying="x", range=[0, 1], showticklabels=False)

    fig.update_layout(
        title='Reward Distribution',
        xaxis_title='Reward Value',
        yaxis_title='Reward Count'
    )

    return fig


@app.callback(
    Output(component_id='summary_context_bar_plot',
           component_property='figure'),
    [
        Input(component_id='selected_mooclet_data', component_property='data'),
        Input(component_id='tab_policy_dropdown', component_property='value'),
        Input(component_id='tab_arm_dropdown', component_property='value'),
        Input(component_id='tab_context_dropdown', component_property='value'),
        Input(component_id='summary_context_timezone_change_type',
              component_property='value'),
        Input(component_id='summary_context_timerange_change_type',
              component_property='value'),
        Input(component_id='summary_context_time_slider',
              component_property='value')
    ]
)
def update_summary_context_bar_plot(df, policy_dropdown_value, arm_dropdown_value, context_dropdown_value, summary_context_timezone_change_type, summary_context_timerange_change_type, summary_context_time_slider):
    print(policy_dropdown_value, arm_dropdown_value, context_dropdown_value)
    ds = json.loads(df)
    if policy_dropdown_value == "uniform_random":
        df_query = pd.read_json(ds['ur_df'], orient='split')
    elif policy_dropdown_value == "thompson_sampling_contextual":
        df_query = pd.read_json(ds['tsc_df'], orient='split')
    else:
        df_query = pd.read_json(ds['df'], orient='split')

    reward_var = ds['rv']

    # df_query = df_query.dropna(subset=['reward_create_time'])

    df_query['reward_create_time'] = pd.to_datetime(
        df_query['reward_create_time']).dt.tz_convert(summary_context_timezone_change_type)
    df_query['arm_assign_time'] = pd.to_datetime(
        df_query['arm_assign_time']).dt.tz_convert(summary_context_timezone_change_type)

    day_offset = 7 if summary_context_timerange_change_type == "week" else 1

    last_reward_idx = df_query['reward_create_time'].last_valid_index()
    last_arm_idx = -1

    if last_reward_idx is not None and df_query['reward_create_time'].iloc[last_reward_idx] > df_query['arm_assign_time'].iloc[last_arm_idx]:
        time_range = pd.date_range(
            start=df_query['arm_assign_time'].iloc[0] -
            pd.offsets.Day(day_offset),
            end=df_query['reward_create_time'].iloc[last_reward_idx] +
            pd.offsets.Day(day_offset),
            tz=summary_context_timezone_change_type,
            freq=f"{day_offset}D",
            inclusive="right"
        )
    else:
        time_range = pd.date_range(
            start=df_query['arm_assign_time'].iloc[0] -
            pd.offsets.Day(day_offset),
            end=df_query['arm_assign_time'].iloc[last_arm_idx] +
            pd.offsets.Day(day_offset),
            tz=summary_context_timezone_change_type,
            freq=f"{day_offset}D",
            inclusive="right"
        )

    df_query = df_query.loc[
        (df_query['arm_assign_time'] >= str(time_range[summary_context_time_slider[0]])) &
        (df_query['arm_assign_time'] < str(
            time_range[summary_context_time_slider[1]]))
    ]

    context_query = df_query.groupby([context_dropdown_value, "arm"]).agg({
        context_dropdown_value: ["first"],
        "arm": ["first"],
        reward_var: ["first", "mean", "std", "sem", "count"]
    })

    all_query = df_query.groupby(["arm"]).agg({
        "arm": ["first"],
        reward_var: ["first", "mean", "std", "sem", "count"]
    })
    all_query[(context_dropdown_value, "first")] = "Overall Average"

    df_query = pd.concat([context_query, all_query])

    df_query[(context_dropdown_value, "first")] = df_query[(
        context_dropdown_value, "first")].astype(str)

    if arm_dropdown_value != "__all__":
        df_query = df_query[df_query[("arm", "first")] == arm_dropdown_value]

    data = []
    for arm in df_query[("arm", "first")].unique().tolist():
        arm_df = df_query[df_query[("arm", "first")] == arm]
        counts = arm_df[(reward_var,
                         "count")].values.tolist()
        means = [round(item, 3) for item in arm_df[(
            reward_var, "mean")].values.tolist()]
        stds = [round(item, 3) for item in arm_df[(
            reward_var, "std")].values.tolist()]
        sems = [round(item, 3) for item in arm_df[(
            reward_var, "sem")].values.tolist()]

        texts = []
        for count, mean, std, sem in zip(counts, means, stds, sems):
            text = f"count = {count} mean = {mean} std = {std} sem= {sem}"
            texts.append(text)

        arm_data = go.Bar(
            name=arm,
            x=df_query[(context_dropdown_value, "first")].unique().tolist(),
            y=means,
            # marker = dict(color = 'rgba(255, 255, 128, 0.5)', line=dict(color='rgb(0,0,0)',width=1.5)),
            hovertext=texts
        )

        data.append(arm_data)

    fig = go.Figure(
        data=data,
        layout=go.Layout(barmode="group"),
        layout_yaxis_range=[0, 5]
    )

    fig.update_layout(
        title='Mean Reward in Different Context Group',
        xaxis_title='Context Group',
        yaxis_title='Mean Reward'
    )

    return fig


@app.callback(
    Output(component_id='tab_time_slider_div', component_property='children'),
    [
        Input(component_id='selected_mooclet_data', component_property='data'),
        Input(component_id='tab_policy_dropdown', component_property='value'),
        Input(component_id='tab_timezone_change_type',
              component_property='value'),
        Input(component_id='tab_timerange_change_type',
              component_property='value')
    ]
)
def update_tab_time_slider(df, tab_policy_dropdown, tab_timezone_change_type, tab_timerange_change_type):
    print(tab_policy_dropdown, tab_timezone_change_type, tab_timerange_change_type)
    ds = json.loads(df)

    if tab_policy_dropdown == "uniform_random":
        df_query = pd.read_json(ds['ur_df'], orient='split')
    elif tab_policy_dropdown == "thompson_sampling_contextual":
        df_query = pd.read_json(ds['tsc_df'], orient='split')
    else:
        df_query = pd.read_json(ds['df'], orient='split')

    # df_query = df_query.dropna(subset=['reward_create_time'])
    df_query['reward_create_time'] = pd.to_datetime(
        df_query['reward_create_time']).dt.tz_convert(tab_timezone_change_type)
    df_query['arm_assign_time'] = pd.to_datetime(
        df_query['arm_assign_time']).dt.tz_convert(tab_timezone_change_type)

    day_offset = 7 if tab_timerange_change_type == "week" else 1

    last_reward_idx = df_query['reward_create_time'].last_valid_index()
    last_arm_idx = -1

    if last_reward_idx is not None and df_query['reward_create_time'].iloc[last_reward_idx] > df_query['arm_assign_time'].iloc[last_arm_idx]:
        time_range = pd.date_range(
            start=df_query['arm_assign_time'].iloc[0] -
            pd.offsets.Day(day_offset),
            end=df_query['reward_create_time'].iloc[last_reward_idx] +
            pd.offsets.Day(day_offset),
            tz=tab_timezone_change_type,
            freq=f"{day_offset}D",
            inclusive="right"
        )
    else:
        time_range = pd.date_range(
            start=df_query['arm_assign_time'].iloc[0] -
            pd.offsets.Day(day_offset),
            end=df_query['arm_assign_time'].iloc[last_arm_idx] +
            pd.offsets.Day(day_offset),
            tz=tab_timezone_change_type,
            freq=f"{day_offset}D",
            inclusive="right"
        )

    return [
        dcc.RangeSlider(
            id="tab_time_slider",
            min=0,
            max=len(time_range) - 1,
            step=len(time_range),
            value=[0, len(time_range) - 1],
            marks={str(idx): time_range[idx].strftime('%m-%d')
                   for idx in range(len(time_range))},
            updatemode='drag'
        )
    ]


@app.callback(
    Output(component_id='summary_reward_time_slider_div',
           component_property='children'),
    [
        Input(component_id='selected_mooclet_data', component_property='data'),
        Input(component_id='tab_policy_dropdown', component_property='value'),
        Input(component_id='summary_reward_timezone_change_type',
              component_property='value'),
        Input(component_id='summary_reward_timerange_change_type',
              component_property='value')
    ]
)
def update_summary_reward_time_slider(df, tab_policy_dropdown, summary_reward_timezone_change_type, summary_reward_timerange_change_type):
    print(tab_policy_dropdown, summary_reward_timezone_change_type,
          summary_reward_timerange_change_type)
    ds = json.loads(df)

    if tab_policy_dropdown == "uniform_random":
        df_query = pd.read_json(ds['ur_df'], orient='split')
    elif tab_policy_dropdown == "thompson_sampling_contextual":
        df_query = pd.read_json(ds['tsc_df'], orient='split')
    else:
        df_query = pd.read_json(ds['df'], orient='split')

    # df_query = df_query.dropna(subset=['reward_create_time'])
    df_query['reward_create_time'] = pd.to_datetime(
        df_query['reward_create_time']).dt.tz_convert(summary_reward_timezone_change_type)
    df_query['arm_assign_time'] = pd.to_datetime(
        df_query['arm_assign_time']).dt.tz_convert(summary_reward_timezone_change_type)

    day_offset = 7 if summary_reward_timerange_change_type == "week" else 1

    last_reward_idx = df_query['reward_create_time'].last_valid_index()
    last_arm_idx = -1

    if last_reward_idx is not None and df_query['reward_create_time'].iloc[last_reward_idx] > df_query['arm_assign_time'].iloc[last_arm_idx]:
        time_range = pd.date_range(
            start=df_query['arm_assign_time'].iloc[0] -
            pd.offsets.Day(day_offset),
            end=df_query['reward_create_time'].iloc[last_reward_idx] +
            pd.offsets.Day(day_offset),
            tz=summary_reward_timezone_change_type,
            freq=f"{day_offset}D",
            inclusive="right"
        )
    else:
        time_range = pd.date_range(
            start=df_query['arm_assign_time'].iloc[0] -
            pd.offsets.Day(day_offset),
            end=df_query['arm_assign_time'].iloc[last_arm_idx] +
            pd.offsets.Day(day_offset),
            tz=summary_reward_timezone_change_type,
            freq=f"{day_offset}D",
            inclusive="right"
        )

    return [
        dcc.RangeSlider(
            id="summary_reward_time_slider",
            min=0,
            max=len(time_range) - 1,
            step=len(time_range),
            value=[0, len(time_range) - 1],
            marks={str(idx): time_range[idx].strftime('%m-%d')
                   for idx in range(len(time_range))},
            updatemode='drag'
        )
    ]


@app.callback(
    Output(component_id='summary_context_time_slider_div',
           component_property='children'),
    [
        Input(component_id='selected_mooclet_data', component_property='data'),
        Input(component_id='tab_policy_dropdown', component_property='value'),
        Input(component_id='summary_context_timezone_change_type',
              component_property='value'),
        Input(component_id='summary_context_timerange_change_type',
              component_property='value')
    ]
)
def update_summary_context_time_slider(df, tab_policy_dropdown, summary_context_timezone_change_type, summary_context_timerange_change_type):
    print(tab_policy_dropdown, summary_context_timezone_change_type,
          summary_context_timerange_change_type)
    ds = json.loads(df)

    if tab_policy_dropdown == "uniform_random":
        df_query = pd.read_json(ds['ur_df'], orient='split')
    elif tab_policy_dropdown == "thompson_sampling_contextual":
        df_query = pd.read_json(ds['tsc_df'], orient='split')
    else:
        df_query = pd.read_json(ds['df'], orient='split')

    # df_query = df_query.dropna(subset=['reward_create_time'])
    df_query['reward_create_time'] = pd.to_datetime(
        df_query['reward_create_time']).dt.tz_convert(summary_context_timezone_change_type)
    df_query['arm_assign_time'] = pd.to_datetime(
        df_query['arm_assign_time']).dt.tz_convert(summary_context_timezone_change_type)

    day_offset = 7 if summary_context_timerange_change_type == "week" else 1

    last_reward_idx = df_query['reward_create_time'].last_valid_index()
    last_arm_idx = -1

    if last_reward_idx is not None and df_query['reward_create_time'].iloc[last_reward_idx] > df_query['arm_assign_time'].iloc[last_arm_idx]:
        time_range = pd.date_range(
            start=df_query['arm_assign_time'].iloc[0] -
            pd.offsets.Day(day_offset),
            end=df_query['reward_create_time'].iloc[last_reward_idx] +
            pd.offsets.Day(day_offset),
            tz=summary_context_timezone_change_type,
            freq=f"{day_offset}D",
            inclusive="right"
        )
    else:
        time_range = pd.date_range(
            start=df_query['arm_assign_time'].iloc[0] -
            pd.offsets.Day(day_offset),
            end=df_query['arm_assign_time'].iloc[last_arm_idx] +
            pd.offsets.Day(day_offset),
            tz=summary_context_timezone_change_type,
            freq=f"{day_offset}D",
            inclusive="right"
        )

    return [
        dcc.RangeSlider(
            id="summary_context_time_slider",
            min=0,
            max=len(time_range) - 1,
            step=len(time_range),
            value=[0, len(time_range) - 1],
            marks={str(idx): time_range[idx].strftime('%m-%d')
                   for idx in range(len(time_range))},
            updatemode='drag'
        )
    ]


@app.callback(
    Output(component_id='tab_arm_dropdown_div', component_property='children'),
    [
        Input(component_id='selected_mooclet_data', component_property='data')
    ]
)
def update_tab_arm_dropdown(data):
    ds = json.loads(data)

    df = pd.read_json(ds['df'], orient='split')

    return [
        dcc.Dropdown(
            id="tab_arm_dropdown",
            options=[{"label": arm, "value": arm} for idx, arm in enumerate(df["arm"].unique().tolist())] +
            [{'label': 'All Arms', 'value': '__all__'}],
            value='__all__'
        )
    ]


@app.callback(
    Output(component_id='tab_context_dropdown_div',
           component_property='children'),
    [
        Input(component_id='selected_mooclet_data', component_property='data')
    ]
)
def update_tab_arm_dropdown(data):
    ds = json.loads(data)

    contextual_variables = ds['cv']

    return [
        dcc.Dropdown(
            id='tab_context_dropdown',
            options=[{"label": context, "value": context}
                     for context in contextual_variables],
            value=contextual_variables[0]
        )
    ]


if __name__ == '__main__':
    app.run_server()
