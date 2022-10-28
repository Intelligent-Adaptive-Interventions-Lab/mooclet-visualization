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
ur_df["modular_link_mha_prototype_linkrating"] = ur_df["modular_link_mha_prototype_linkrating"] * 4 + 1

tsc_df = pd.read_excel(xls, 'TSC_4')
tsc_df["modular_link_mha_prototype_linkrating"] = tsc_df["modular_link_mha_prototype_linkrating"] * 4 + 1

df = pd.concat([ur_df, tsc_df])

contextual_variables = [
    "modular_link_mha_prototype_hadrecentactivitylast48hours",
    "modular_link_mha_prototype_isweekend", 
    "modular_link_mha_prototype_timeofday", 
    "modular_link_mha_prototype_highmood", 
    "modular_link_mha_prototype_highenergy", 
    "modular_link_mha_prototype_studyday", 
    "modular_link_mha_prototype_k10", 
    "modular_link_mha_prototype_averageresponsiveness", 
    "modular_link_mha_prototype_averagecontentratingsoverall"
]

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
        html.H2(
            id = 'change_policy',
            children = 'Change Policy',
            style = {
                'textAlign':'left',
                'marginBottom':20
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
        html.Div(
            id = 'tab_time_change',
            children = [
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
                'marginTop':20
            }
        ),
        html.Div(
            id = 'tab_time_slider_div', 
            style={
                'textAlign':'center',
            }
        ),
        html.Div(
            id='summary_table', 
            style = {
                'marginTop':20,
                'marginBottom':20
            }
        ),
        html.H2(
            id = 'change_arm',
            children = 'Change Arm',
            style = {
                'textAlign':'left',
                'marginBottom':20
            }
        ),
        dcc.Dropdown(
            id = 'tab_arm_dropdown',
            options =  [ {"label": arm, "value": arm} for idx, arm in enumerate(df["arm"].unique().tolist()) ] + \
                [ {'label': 'All Arms', 'value': '__all__'} ],
            value = '__all__'
        ),
        dcc.Graph(id = 'summary_reward_bar_plot'),
        dcc.Dropdown(
            id = 'tab_context_dropdown',
            options =  [ {"label": context, "value": context} for context in contextual_variables ],
            value = contextual_variables[0]
        ),
        dcc.Graph(id = 'summary_context_bar_plot'),
        
    ]
)

@app.callback(
    Output(component_id='summary_table', component_property= 'children'),
    [
        Input(component_id='tab_policy_dropdown', component_property= 'value'),
        Input(component_id='tab_timezone_change_type', component_property= 'value'),
        Input(component_id='tab_timerange_change_type', component_property= 'value'),
        Input(component_id='tab_time_slider', component_property= 'value')
    ]
)
def update_summary_table(dropdown_value, tab_timezone_change_type, tab_timerange_change_type, tab_time_slider):
    print(dropdown_value, tab_timezone_change_type, tab_timerange_change_type, tab_time_slider)
    if dropdown_value == "uniform_random":
        df_query = ur_df.copy()
    elif dropdown_value == "thompson_sampling_contextual":
        df_query = tsc_df.copy()
    else:
        df_query = df.copy()
    
    df_query['reward_create_time'] = pd.to_datetime(df_query['reward_create_time']).dt.tz_convert(tab_timezone_change_type)
    df_query['arm_assign_time'] = pd.to_datetime(df_query['arm_assign_time']).dt.tz_convert(tab_timezone_change_type)

    day_offset = 7 if tab_timerange_change_type == "week" else 1

    last_reward_idx = df_query['reward_create_time'].last_valid_index()
    last_arm_idx = -1
    
    if last_reward_idx is not None and df_query['reward_create_time'].iloc[last_reward_idx] > df_query['arm_assign_time'].iloc[last_arm_idx]:
        time_range = pd.date_range(
            start=df_query['arm_assign_time'].iloc[0] - pd.offsets.Day(day_offset), 
            end=df_query['reward_create_time'].iloc[last_reward_idx] + pd.offsets.Day(day_offset), 
            tz=tab_timezone_change_type, 
            freq=f"{day_offset}D", 
            inclusive="right"
        )
    else:
        time_range = pd.date_range(
            start=df_query['arm_assign_time'].iloc[0] - pd.offsets.Day(day_offset), 
            end=df_query['arm_assign_time'].iloc[last_arm_idx] + pd.offsets.Day(day_offset), 
            tz=tab_timezone_change_type, 
            freq=f"{day_offset}D", 
            inclusive="right"
        )
    
    df_query = df_query.loc[
        (df_query['arm_assign_time'] >= str(time_range[tab_time_slider[0]])) & \
        (df_query['arm_assign_time'] < str(time_range[tab_time_slider[1]]))
    ]

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

    return [
        dash_table.DataTable(
            columns=[{"name": [item if item != "first" else "{} name".format(i[0]) for item in list(i)], "id": '_'.join(i)} for i in df_query.columns],
            data=[ {"_".join(col): round(val, 3) if isinstance(val, float) else val for col, val in row.items() } for row in df_query.to_dict('records') ],
            merge_duplicate_headers=True,
            sort_action='native',
        )
    ]

@app.callback(
    Output(component_id='summary_reward_bar_plot', component_property= 'figure'),
    [
        Input(component_id='tab_policy_dropdown', component_property= 'value'),
        Input(component_id='tab_arm_dropdown', component_property= 'value')
    ]
)
def update_summary_reward_bar_plot(policy_dropdown_value, arm_dropdown_value):
    print(policy_dropdown_value, arm_dropdown_value)
    if policy_dropdown_value == "uniform_random":
        df_query = ur_df.copy()
    elif policy_dropdown_value == "thompson_sampling_contextual":
        df_query = tsc_df.copy()
    else:
        df_query = df.copy()
    
    if arm_dropdown_value == "__all__":
        df_query = df_query.groupby(["modular_link_mha_prototype_linkrating"]).agg({
            "modular_link_mha_prototype_linkrating": ["first", "count"]
        })
    else:
        df_query = df_query.groupby(["arm", "modular_link_mha_prototype_linkrating"]).agg({
            "arm": ["first"],
            "modular_link_mha_prototype_linkrating": ["first", "count"]
        })
        df_query = df_query[df_query[("arm", "first")] == arm_dropdown_value]
    
    fig = go.Figure(
        [
            go.Bar(
                x = df_query[("modular_link_mha_prototype_linkrating", "first")], 
                y = df_query[("modular_link_mha_prototype_linkrating", "count")],
                marker=dict(color = df_query[("modular_link_mha_prototype_linkrating", "first")], colorscale='viridis')
            )
        ]
    )
    
    fig.layout.xaxis2 = go.layout.XAxis(overlaying="x", range=[0, 1], showticklabels=False)
    
    fig.update_layout(
        title = 'Reward Distribution',
        xaxis_title = 'Reward Value',
        yaxis_title = 'Reward Count'
    )
    
    return fig


@app.callback(
    Output(component_id='summary_context_bar_plot', component_property= 'figure'),
    [
        Input(component_id='tab_policy_dropdown', component_property= 'value'),
        Input(component_id='tab_arm_dropdown', component_property= 'value'),
        Input(component_id='tab_context_dropdown', component_property= 'value'),
    ]
)
def update_summary_context_bar_plot(policy_dropdown_value, arm_dropdown_value, context_dropdown_value):
    print(policy_dropdown_value, arm_dropdown_value, context_dropdown_value)
    if policy_dropdown_value == "uniform_random":
        df_query = ur_df.copy()
    elif policy_dropdown_value == "thompson_sampling_contextual":
        df_query = tsc_df.copy()
    else:
        df_query = df.copy()
    
    context_query = df_query.groupby([context_dropdown_value, "arm"]).agg({
    context_dropdown_value: ["first"],
        "arm": ["first"],
        "modular_link_mha_prototype_linkrating": ["first", "mean", "std", "sem", "count"]
    })
    
    all_query = df_query.groupby(["arm"]).agg({
        "arm": ["first"],
        "modular_link_mha_prototype_linkrating": ["first", "mean", "std", "sem", "count"]
    })
    all_query[(context_dropdown_value, "first")] = "Overall Average"

    df_query = pd.concat([context_query, all_query])
    
    df_query[(context_dropdown_value, "first")] = df_query[(context_dropdown_value, "first")].astype(str)

    if arm_dropdown_value != "__all__":
        df_query = df_query[df_query[("arm", "first")] == arm_dropdown_value]

    data = []
    for arm in df_query[("arm", "first")].unique().tolist():
        arm_df = df_query[df_query[("arm", "first")] == arm]
        counts = arm_df[("modular_link_mha_prototype_linkrating", "count")].values.tolist()
        means = [ round(item, 3) for item in arm_df[("modular_link_mha_prototype_linkrating", "mean")].values.tolist() ] 
        stds = [ round(item, 3) for item in arm_df[("modular_link_mha_prototype_linkrating", "std")].values.tolist() ] 
        sems = [ round(item, 3) for item in arm_df[("modular_link_mha_prototype_linkrating", "sem")].values.tolist() ]

        texts = []
        for count, mean, std, sem in zip(counts, means, stds, sems):
            text = f"count = {count} mean = {mean} std = {std} sem= {sem}"
            texts.append(text)

        arm_data = go.Bar(
            name = arm,
            x = df_query[(context_dropdown_value, "first")].unique().tolist(), 
            y = means,
            # marker = dict(color = 'rgba(255, 255, 128, 0.5)', line=dict(color='rgb(0,0,0)',width=1.5)),
            hovertext = texts
        )

        data.append(arm_data)

    fig = go.Figure(
        data = data,
        layout = go.Layout(barmode = "group"), 
        layout_yaxis_range=[0, 5]
    )

    fig.update_layout(
        title = 'Mean Reward in Different Context Group',
        xaxis_title = 'Context Group',
        yaxis_title = 'Mean Reward'
    )

    return fig


@app.callback(
    Output(component_id='tab_time_slider_div', component_property= 'children'),
    [
        Input(component_id='tab_policy_dropdown', component_property= 'value'),
        Input(component_id='tab_timezone_change_type', component_property= 'value'),
        Input(component_id='tab_timerange_change_type', component_property= 'value')
    ]
)
def update_tab_time_slider(tab_policy_dropdown, tab_timezone_change_type, tab_timerange_change_type):
    print(tab_policy_dropdown, tab_timezone_change_type, tab_timerange_change_type)
    if tab_policy_dropdown == "uniform_random":
        df_query = ur_df.copy()
    elif tab_policy_dropdown == "thompson_sampling_contextual":
        df_query = tsc_df.copy()
    else:
        df_query = df.copy()

    df_query['reward_create_time'] = pd.to_datetime(df_query['reward_create_time']).dt.tz_convert(tab_timezone_change_type)
    df_query['arm_assign_time'] = pd.to_datetime(df_query['arm_assign_time']).dt.tz_convert(tab_timezone_change_type)

    day_offset = 7 if tab_timerange_change_type == "week" else 1

    last_reward_idx = df_query['reward_create_time'].last_valid_index()
    last_arm_idx = -1
    
    if last_reward_idx is not None and df_query['reward_create_time'].iloc[last_reward_idx] > df_query['arm_assign_time'].iloc[last_arm_idx]:
        time_range = pd.date_range(
            start=df_query['arm_assign_time'].iloc[0] - pd.offsets.Day(day_offset), 
            end=df_query['reward_create_time'].iloc[last_reward_idx] + pd.offsets.Day(day_offset), 
            tz=tab_timezone_change_type, 
            freq=f"{day_offset}D", 
            inclusive="right"
        )
    else:
        time_range = pd.date_range(
            start=df_query['arm_assign_time'].iloc[0] - pd.offsets.Day(day_offset), 
            end=df_query['arm_assign_time'].iloc[last_arm_idx] + pd.offsets.Day(day_offset), 
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
            marks={str(idx): time_range[idx].strftime('%m-%d') for idx in range(len(time_range))}
        )
    ]


if __name__ == '__main__': 
    app.run_server()
