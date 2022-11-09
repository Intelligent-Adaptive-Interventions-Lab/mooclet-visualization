import dash
from dash import html
from dash import dcc
from dash import dash_table
import plotly.graph_objects as go
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd
import sys
import requests
from config import TOKEN

app = dash.Dash()


MOOCLETS = {'315': 'datasets/Modular_Link_MHA_Prototype.xlsx',
           '295': 'datasets/MHAwave1ModularRationale.xlsx'}

# 315, 295:
# MOOCLET_FILES = ['datasets/Modular_Link_MHA_Prototype.xlsx',
#                  'datasets/MHAwave1ModularRationale.xlsx']
# MOOCLET_URLS = ['https://mooclet.canadacentral.cloudapp.azure.com/engine/api/v1/policyparameters?mooclet=315&policy=6',
#                 'https://mooclet.canadacentral.cloudapp.azure.com/engine/api/v1/policyparameters?mooclet=295&policy=6']
# XLS = []
# REWARD = ["modular_link_mha_prototype_linkrating",
#           "MHAwave1ModularMessageReward"]
# UR_DFS = []
# TSC_DFS = []
# DFS = []
#
# UR_DF = [0]
# TSC_DF = [0]
# DF = [0]
# CONTEXTUAL = [[
#     "modular_link_mha_prototype_hadrecentactivitylast48hours",
#     "modular_link_mha_prototype_isweekend",
#     "modular_link_mha_prototype_timeofday",
#     "modular_link_mha_prototype_highmood",
#     "modular_link_mha_prototype_highenergy",
#     "modular_link_mha_prototype_studyday",
#     "modular_link_mha_prototype_k10",
#     "modular_link_mha_prototype_averageresponsiveness",
#     "modular_link_mha_prototype_averagecontentratingsoverall"
# ], [
#     "wave1RecentActivityLast48Hours",
#     "wave1IsWeekend",
#     "wave1isHighMood",
#     "wave1isHighEnergy",
#     "wave1TimeOfDay",
#     "wave1UserLevelRecencyRationale",
#     "wave1PriorRationaleRating",
#     "wave1StudyDay",
#     "wave1K10",
#     "wave1AverageResponsiveness",
#     "wave1AverageContentRatingsOverall"
# ]
# ]

MOOCLET_FILES = []
MOOCLET_URLS = []
XLS = []
REWARD = []

UR_DFS = []
TSC_DFS = []
DFS = []

UR_DF = [0]
TSC_DF = [0]
DF = [0]

CONTEXTUAL = []



def upload_mooclets(file, num):
    MOOCLET_FILES.append(file)
    MOOCLET_URLS.append("https://mooclet.canadacentral.cloudapp.azure.com/engine/api/v1/policyparameters?mooclet={0}&policy=6".format(num))
    XLS.append(pd.ExcelFile(file))


def prepare():
    for i in range(len(XLS)):
        ur_df = pd.read_excel(XLS[i], 'UR_0')
        ur_df[REWARD[i]] = ur_df[REWARD[i]] * 4 + 1
        UR_DFS.append(ur_df)

        tsc_df = pd.read_excel(XLS[i], 'TSC_4')
        tsc_df[REWARD[i]] = ur_df[REWARD[i]] * 4 + 1
        TSC_DFS.append(tsc_df)

        df = pd.concat([ur_df, tsc_df])
        DFS.append(df)
    DF[0] = DFS[0]
    UR_DF[0] = UR_DFS[0]
    TSC_DF[0] = TSC_DFS[0]


def get_reward_contextual_variables():
    for i in range(len(MOOCLET_URLS)):
        mresponse = requests.get(url=MOOCLET_URLS[i],
                                 headers={'Authorization': TOKEN})
        mresponse_json = mresponse.json()
        parameters = mresponse_json["results"][0]["parameters"]
        REWARD.append(parameters["outcome_variable"])
        context = parameters["contextual_variables"]
        context.remove('version')
        CONTEXTUAL.append(context)


# only for mooclet 315 and 295

# def upload_mooclets2(file):
#     # MOOCLETS.append(file)
#     XLS.append(pd.ExcelFile(file))
#     # REWARD.append(get_reward_name(file))
#     # CONTEXTUAL.append(get_contextual_variables(file))
#
# def prepare2():
#     for i in range(len(XLS)):
#         ur_df = pd.read_excel(XLS[i], 'UR_0')
#         ur_df[REWARD[i]] = ur_df[REWARD[i]] * 4 + 1
#         UR_DFS.append(ur_df)
#
#         tsc_df = pd.read_excel(XLS[i], 'TSC_4')
#         tsc_df[REWARD[i]] = ur_df[REWARD[i]] * 4 + 1
#         TSC_DFS.append(tsc_df)
#
#         df = pd.concat([ur_df, tsc_df])
#         DFS.append(df)
#     DF[0] = DFS[0]
#     UR_DF[0] = UR_DFS[0]
#     TSC_DF[0] = TSC_DFS[0]
#
# for i in MOOCLET_FILES:
#     upload_mooclets2(i)
# prepare2()


def update_df(mooclet_index):
    UR_DF[0] = UR_DFS[mooclet_index]
    TSC_DF[0] = TSC_DFS[mooclet_index]
    DF[0] = DFS[mooclet_index]


# Previous version only for mooclet 315

# df = px.data.stocks()

# xls = pd.ExcelFile('datasets/Modular_Link_MHA_Prototype.xlsx')
# ur_df = pd.read_excel(xls, 'UR_0')
# ur_df["modular_link_mha_prototype_linkrating"] = ur_df["modular_link_mha_prototype_linkrating"] * 4 + 1
#
# tsc_df = pd.read_excel(xls, 'TSC_4')
# tsc_df["modular_link_mha_prototype_linkrating"] = tsc_df["modular_link_mha_prototype_linkrating"] * 4 + 1
#
# df = pd.concat([ur_df, tsc_df])
#
# contextual_variables = [
#     "modular_link_mha_prototype_hadrecentactivitylast48hours",
#     "modular_link_mha_prototype_isweekend",
#     "modular_link_mha_prototype_timeofday",
#     "modular_link_mha_prototype_highmood",
#     "modular_link_mha_prototype_highenergy",
#     "modular_link_mha_prototype_studyday",
#     "modular_link_mha_prototype_k10",
#     "modular_link_mha_prototype_averageresponsiveness",
#     "modular_link_mha_prototype_averagecontentratingsoverall"
# ]
if len(sys.argv) > 1:
    for i in range(1, len(sys.argv)):
        upload_mooclets(MOOCLETS[sys.argv[i]], sys.argv[i])
    get_reward_contextual_variables()
    prepare()
else:
    for mooclet in ['315', '295']:
        upload_mooclets(MOOCLETS[mooclet], mooclet)
    get_reward_contextual_variables()
    prepare()


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
            id = 'change_Mooclet',
            children = 'Change Mooclet',
            style = {
                'textAlign':'left',
                'marginBottom':20
            }
        ),
        dcc.Dropdown(
            id = 'tab_mooclet_dropdown',
            options = [
                {'label': name, 'value': MOOCLET_FILES.index(name)} for name in MOOCLET_FILES
            ],
            value = 0
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
                'marginTop':20,
                'marginBottom':20
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
            options =  [ {"label": arm, "value": arm} for idx, arm in enumerate(DF[0]["arm"].unique().tolist()) ] + \
                       [ {'label': 'All Arms', 'value': '__all__'} ],
            value = '__all__'
        ),
        html.Div(
            id = 'summary_reward_time_change',
            children = [
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
                'marginTop':20,
                'marginBottom':20
            }
        ),
        html.Div(
            id = 'summary_reward_time_slider_div',
            style={
                'textAlign':'center',
                'marginBottom':5
            }
        ),
        dcc.Graph(id = 'summary_reward_bar_plot'),
        # dcc.Dropdown(
        #     id = 'tab_context_dropdown',
        #     options =  [ {"label": context, "value": context} for context in contextual_variables],
        #     value = contextual_variables[0]
        # ),
        dcc.Dropdown(
            id = 'contextual_variables',
            options = [],
        ),
        html.Div(
            id = 'summary_context_time_change',
            children = [
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
                'marginTop':20,
                'marginBottom':20
            }
        ),
        html.Div(
            id = 'summary_context_time_slider_div',
            style={
                'textAlign':'center',
                'marginBottom':5
            }
        ),
        dcc.Graph(id = 'summary_context_bar_plot'),

    ]
)

@app.callback(
    Output(component_id='contextual_variables', component_property= 'options'),
    [
        Input(component_id='tab_mooclet_dropdown', component_property= 'value')
    ]
)
def choose_contextual_variable_given_mooclet(mooclet_index):
    return [{'label': v, 'value': v} for v in CONTEXTUAL[mooclet_index]]


@app.callback(
    Output(component_id='contextual_variables', component_property= 'value'),
    [
        Input(component_id='tab_mooclet_dropdown', component_property= 'value')
    ]
)
def choose_contextual_variable_given_mooclet(mooclet_index):
    return CONTEXTUAL[mooclet_index][0]



@app.callback(
    Output(component_id='summary_table', component_property= 'children'),
    [
        Input(component_id='tab_policy_dropdown', component_property= 'value'),
        Input(component_id='tab_timezone_change_type', component_property= 'value'),
        Input(component_id='tab_timerange_change_type', component_property= 'value'),
        Input(component_id='tab_time_slider', component_property= 'value'),
        Input(component_id='tab_mooclet_dropdown', component_property= 'value')
    ]
)
def update_summary_table(dropdown_value, tab_timezone_change_type, tab_timerange_change_type, tab_time_slider, mooclet_index):
    print(dropdown_value, tab_timezone_change_type, tab_timerange_change_type, tab_time_slider)
    update_df(mooclet_index)
    if dropdown_value == "uniform_random":
        df_query = UR_DF[0].copy()
    elif dropdown_value == "thompson_sampling_contextual":
        df_query = TSC_DF[0].copy()
    else:
        df_query = DF[0].copy()

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
            REWARD[mooclet_index]: ["mean", "std", "sem", "count"]
        })
    else:
        df_query = df_query.groupby(["policy", "arm"]).agg({
            "policy": ["first"],
            "arm": ["first", "count"],
            REWARD[mooclet_index]: ["mean", "std", "sem", "count"]
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
        Input(component_id='tab_arm_dropdown', component_property= 'value'),
        Input(component_id='summary_reward_timezone_change_type', component_property= 'value'),
        Input(component_id='summary_reward_timerange_change_type', component_property= 'value'),
        Input(component_id='summary_reward_time_slider', component_property= 'value'),
        Input(component_id='tab_mooclet_dropdown', component_property= 'value')
    ]
)
def update_summary_reward_bar_plot(policy_dropdown_value, arm_dropdown_value, summary_reward_timezone_change_type, summary_reward_timerange_change_type, summary_reward_time_slider, mooclet_index):
    update_df(mooclet_index)
    print(policy_dropdown_value, arm_dropdown_value)
    if policy_dropdown_value == "uniform_random":
        df_query = UR_DF[0].copy()
    elif policy_dropdown_value == "thompson_sampling_contextual":
        df_query = TSC_DF[0].copy()
    else:
        df_query = DF[0].copy()

    df_query['reward_create_time'] = pd.to_datetime(df_query['reward_create_time']).dt.tz_convert(summary_reward_timezone_change_type)
    df_query['arm_assign_time'] = pd.to_datetime(df_query['arm_assign_time']).dt.tz_convert(summary_reward_timezone_change_type)

    day_offset = 7 if summary_reward_timerange_change_type == "week" else 1

    last_reward_idx = df_query['reward_create_time'].last_valid_index()
    last_arm_idx = -1

    if last_reward_idx is not None and df_query['reward_create_time'].iloc[last_reward_idx] > df_query['arm_assign_time'].iloc[last_arm_idx]:
        time_range = pd.date_range(
            start=df_query['arm_assign_time'].iloc[0] - pd.offsets.Day(day_offset),
            end=df_query['reward_create_time'].iloc[last_reward_idx] + pd.offsets.Day(day_offset),
            tz=summary_reward_timezone_change_type,
            freq=f"{day_offset}D",
            inclusive="right"
        )
    else:
        time_range = pd.date_range(
            start=df_query['arm_assign_time'].iloc[0] - pd.offsets.Day(day_offset),
            end=df_query['arm_assign_time'].iloc[last_arm_idx] + pd.offsets.Day(day_offset),
            tz=summary_reward_timezone_change_type,
            freq=f"{day_offset}D",
            inclusive="right"
        )

    df_query = df_query.loc[
        (df_query['arm_assign_time'] >= str(time_range[summary_reward_time_slider[0]])) & \
        (df_query['arm_assign_time'] < str(time_range[summary_reward_time_slider[1]]))
        ]

    if arm_dropdown_value == "__all__":
        df_query = df_query.groupby([REWARD[mooclet_index]]).agg({
            REWARD[mooclet_index]: ["first", "count"]
        })
    else:
        df_query = df_query.groupby(["arm", REWARD[mooclet_index]]).agg({
            "arm": ["first"],
            REWARD[mooclet_index]: ["first", "count"]
        })
        df_query = df_query[df_query[("arm", "first")] == arm_dropdown_value]

    fig = go.Figure(
        [
            go.Bar(
                x = df_query[(REWARD[mooclet_index], "first")],
                y = df_query[(REWARD[mooclet_index], "count")],
                marker=dict(color = df_query[(REWARD[mooclet_index], "first")], colorscale='viridis')
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
        Input(component_id='contextual_variables', component_property= 'value'),
        Input(component_id='summary_context_timezone_change_type', component_property= 'value'),
        Input(component_id='summary_context_timerange_change_type', component_property= 'value'),
        Input(component_id='summary_context_time_slider', component_property= 'value'),
        Input(component_id='tab_mooclet_dropdown', component_property= 'value')
    ]
)
def update_summary_context_bar_plot(policy_dropdown_value, arm_dropdown_value, context_dropdown_value, summary_context_timezone_change_type, summary_context_timerange_change_type, summary_context_time_slider, mooclet_index):
    update_df(mooclet_index)
    print(policy_dropdown_value, arm_dropdown_value, context_dropdown_value)
    if policy_dropdown_value == "uniform_random":
        df_query = UR_DF[0].copy()
    elif policy_dropdown_value == "thompson_sampling_contextual":
        df_query = TSC_DF[0].copy()
    else:
        df_query = DF[0].copy()

    df_query['reward_create_time'] = pd.to_datetime(df_query['reward_create_time']).dt.tz_convert(summary_context_timezone_change_type)
    df_query['arm_assign_time'] = pd.to_datetime(df_query['arm_assign_time']).dt.tz_convert(summary_context_timezone_change_type)

    day_offset = 7 if summary_context_timerange_change_type == "week" else 1

    last_reward_idx = df_query['reward_create_time'].last_valid_index()
    last_arm_idx = -1

    if last_reward_idx is not None and df_query['reward_create_time'].iloc[last_reward_idx] > df_query['arm_assign_time'].iloc[last_arm_idx]:
        time_range = pd.date_range(
            start=df_query['arm_assign_time'].iloc[0] - pd.offsets.Day(day_offset),
            end=df_query['reward_create_time'].iloc[last_reward_idx] + pd.offsets.Day(day_offset),
            tz=summary_context_timezone_change_type,
            freq=f"{day_offset}D",
            inclusive="right"
        )
    else:
        time_range = pd.date_range(
            start=df_query['arm_assign_time'].iloc[0] - pd.offsets.Day(day_offset),
            end=df_query['arm_assign_time'].iloc[last_arm_idx] + pd.offsets.Day(day_offset),
            tz=summary_context_timezone_change_type,
            freq=f"{day_offset}D",
            inclusive="right"
        )

    df_query = df_query.loc[
        (df_query['arm_assign_time'] >= str(time_range[summary_context_time_slider[0]])) & \
        (df_query['arm_assign_time'] < str(time_range[summary_context_time_slider[1]]))
        ]

    context_query = df_query.groupby([context_dropdown_value, "arm"]).agg({
        context_dropdown_value: ["first"],
        "arm": ["first"],
        REWARD[mooclet_index]: ["first", "mean", "std", "sem", "count"]
    })

    all_query = df_query.groupby(["arm"]).agg({
        "arm": ["first"],
        REWARD[mooclet_index]: ["first", "mean", "std", "sem", "count"]
    })
    all_query[(context_dropdown_value, "first")] = "Overall Average"

    df_query = pd.concat([context_query, all_query])

    df_query[(context_dropdown_value, "first")] = df_query[(context_dropdown_value, "first")].astype(str)

    if arm_dropdown_value != "__all__":
        df_query = df_query[df_query[("arm", "first")] == arm_dropdown_value]

    data = []
    for arm in df_query[("arm", "first")].unique().tolist():
        arm_df = df_query[df_query[("arm", "first")] == arm]
        counts = arm_df[(REWARD[mooclet_index], "count")].values.tolist()
        means = [ round(item, 3) for item in arm_df[(REWARD[mooclet_index], "mean")].values.tolist() ]
        stds = [ round(item, 3) for item in arm_df[(REWARD[mooclet_index], "std")].values.tolist() ]
        sems = [ round(item, 3) for item in arm_df[(REWARD[mooclet_index], "sem")].values.tolist() ]

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
        Input(component_id='tab_timerange_change_type', component_property= 'value'),
        Input(component_id='tab_mooclet_dropdown', component_property= 'value')
    ]
)
def update_tab_time_slider(tab_policy_dropdown, tab_timezone_change_type, tab_timerange_change_type, mooclet_index):
    update_df(mooclet_index)
    print(tab_policy_dropdown, tab_timezone_change_type, tab_timerange_change_type)
    if tab_policy_dropdown == "uniform_random":
        df_query = UR_DF[0].copy()
    elif tab_policy_dropdown == "thompson_sampling_contextual":
        df_query = TSC_DF[0].copy()
    else:
        df_query = DF[0].copy()

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
            marks={str(idx): time_range[idx].strftime('%m-%d') for idx in range(len(time_range))},
            updatemode='drag'
        )
    ]

@app.callback(
    Output(component_id='summary_reward_time_slider_div', component_property= 'children'),
    [
        Input(component_id='tab_policy_dropdown', component_property= 'value'),
        Input(component_id='summary_reward_timezone_change_type', component_property= 'value'),
        Input(component_id='summary_reward_timerange_change_type', component_property= 'value'),
        Input(component_id='tab_mooclet_dropdown', component_property= 'value')
    ]
)
def update_summary_reward_time_slider(tab_policy_dropdown, summary_reward_timezone_change_type, summary_reward_timerange_change_type, mooclet_index):
    update_df(mooclet_index)
    print(tab_policy_dropdown, summary_reward_timezone_change_type, summary_reward_timerange_change_type)
    if tab_policy_dropdown == "uniform_random":
        df_query = UR_DF[0].copy()
    elif tab_policy_dropdown == "thompson_sampling_contextual":
        df_query = TSC_DF[0].copy()
    else:
        df_query = DF[0].copy()

    df_query['reward_create_time'] = pd.to_datetime(df_query['reward_create_time']).dt.tz_convert(summary_reward_timezone_change_type)
    df_query['arm_assign_time'] = pd.to_datetime(df_query['arm_assign_time']).dt.tz_convert(summary_reward_timezone_change_type)

    day_offset = 7 if summary_reward_timerange_change_type == "week" else 1

    last_reward_idx = df_query['reward_create_time'].last_valid_index()
    last_arm_idx = -1

    if last_reward_idx is not None and df_query['reward_create_time'].iloc[last_reward_idx] > df_query['arm_assign_time'].iloc[last_arm_idx]:
        time_range = pd.date_range(
            start=df_query['arm_assign_time'].iloc[0] - pd.offsets.Day(day_offset),
            end=df_query['reward_create_time'].iloc[last_reward_idx] + pd.offsets.Day(day_offset),
            tz=summary_reward_timezone_change_type,
            freq=f"{day_offset}D",
            inclusive="right"
        )
    else:
        time_range = pd.date_range(
            start=df_query['arm_assign_time'].iloc[0] - pd.offsets.Day(day_offset),
            end=df_query['arm_assign_time'].iloc[last_arm_idx] + pd.offsets.Day(day_offset),
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
            marks={str(idx): time_range[idx].strftime('%m-%d') for idx in range(len(time_range))},
            updatemode='drag'
        )
    ]

@app.callback(
    Output(component_id='summary_context_time_slider_div', component_property= 'children'),
    [
        Input(component_id='tab_policy_dropdown', component_property= 'value'),
        Input(component_id='summary_context_timezone_change_type', component_property= 'value'),
        Input(component_id='summary_context_timerange_change_type', component_property= 'value'),
        Input(component_id='tab_mooclet_dropdown', component_property= 'value')
    ]
)
def update_summary_context_time_slider(tab_policy_dropdown, summary_context_timezone_change_type, summary_context_timerange_change_type, mooclet_index):
    update_df(mooclet_index)
    print(tab_policy_dropdown, summary_context_timezone_change_type, summary_context_timerange_change_type)
    if tab_policy_dropdown == "uniform_random":
        df_query = UR_DF[0].copy()
    elif tab_policy_dropdown == "thompson_sampling_contextual":
        df_query = TSC_DF[0].copy()
    else:
        df_query = DF[0].copy()

    df_query['reward_create_time'] = pd.to_datetime(df_query['reward_create_time']).dt.tz_convert(summary_context_timezone_change_type)
    df_query['arm_assign_time'] = pd.to_datetime(df_query['arm_assign_time']).dt.tz_convert(summary_context_timezone_change_type)

    day_offset = 7 if summary_context_timerange_change_type == "week" else 1

    last_reward_idx = df_query['reward_create_time'].last_valid_index()
    last_arm_idx = -1

    if last_reward_idx is not None and df_query['reward_create_time'].iloc[last_reward_idx] > df_query['arm_assign_time'].iloc[last_arm_idx]:
        time_range = pd.date_range(
            start=df_query['arm_assign_time'].iloc[0] - pd.offsets.Day(day_offset),
            end=df_query['reward_create_time'].iloc[last_reward_idx] + pd.offsets.Day(day_offset),
            tz=summary_context_timezone_change_type,
            freq=f"{day_offset}D",
            inclusive="right"
        )
    else:
        time_range = pd.date_range(
            start=df_query['arm_assign_time'].iloc[0] - pd.offsets.Day(day_offset),
            end=df_query['arm_assign_time'].iloc[last_arm_idx] + pd.offsets.Day(day_offset),
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
            marks={str(idx): time_range[idx].strftime('%m-%d') for idx in range(len(time_range))},
            updatemode='drag'
        )
    ]

if __name__ == '__main__':
    app.run_server()
