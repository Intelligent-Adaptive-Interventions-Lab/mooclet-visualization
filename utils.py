from typing import Tuple, List
from scipy.stats import invgamma

import pandas as pd
import numpy as np
import json


def get_dataset(df, dropdown_value):
    ds = json.loads(df)

    if dropdown_value == "uniform_random":
        df_query = pd.read_json(ds['ur_df'], orient='split').copy()
    elif dropdown_value == "thompson_sampling_contextual":
        df_query = pd.read_json(ds['tsc_df'], orient='split').copy()
    else:
        df_query = pd.read_json(ds['df'], orient='split').copy()

    reward_var = ds['rv']

    return df_query, reward_var


def filter_by_time(df_query, timezone_change_type, timerange_change_type, time_slider=None):
    df_query['reward_create_time'] = pd.to_datetime(df_query['reward_create_time']).dt.tz_convert(timezone_change_type)
    df_query['arm_assign_time'] = pd.to_datetime(df_query['arm_assign_time']).dt.tz_convert(timezone_change_type)

    day_offset = 7 if timerange_change_type == "week" else 1

    last_reward_idx = df_query['reward_create_time'].last_valid_index()
    last_arm_idx = -1

    if last_reward_idx is not None and df_query['reward_create_time'].iloc[last_reward_idx] > df_query['arm_assign_time'].iloc[last_arm_idx]:
        time_range = pd.date_range(
            start=df_query['arm_assign_time'].iloc[0] -
            pd.offsets.Day(day_offset),
            end=df_query['reward_create_time'].iloc[last_reward_idx] +
            pd.offsets.Day(day_offset),
            tz=timezone_change_type,
            freq=f"{day_offset}D",
            inclusive="right"
        )
    else:
        time_range = pd.date_range(
            start=df_query['arm_assign_time'].iloc[0] -
            pd.offsets.Day(day_offset),
            end=df_query['arm_assign_time'].iloc[last_arm_idx] +
            pd.offsets.Day(day_offset),
            tz=timezone_change_type,
            freq=f"{day_offset}D",
            inclusive="right"
        )
    
    if time_slider:
        df_query = df_query.loc[
            (df_query['arm_assign_time'] >= str(time_range[max(0, time_slider[0])])) & \
            (df_query['arm_assign_time'] < str(time_range[min(time_slider[1], len(time_range) - 1)]))
        ]
    
    return df_query, time_range


def estimate_coef_mean(df_query: pd.DataFrame, order_by: str) -> pd.DataFrame:

    def mean_confidence_interval_quantile(
        samples: List[float], 
        confidence: float = 0.95
    ) -> Tuple[float, float, float]:
        m = np.mean(samples)
        lower = np.quantile(np.asarray(samples), (1 - confidence) / 2.)
        upper = np.quantile(np.asarray(samples), confidence + (1 - confidence) / 2.)

        return m, lower, upper

    df_query_tsc = df_query[df_query["policy"] == "thompson_sampling_contextual"]

    if len(df_query_tsc) == 0:
        return None

    columns = list(df_query_tsc.columns)
    for column_name in ["regression_formula", "coef_mean", "coef_cov", "variance_a", "variance_b"]:
        if column_name not in columns:
            return None

    df_query_tsc = df_query_tsc.drop_duplicates(
        subset=["regression_formula", "coef_mean", "coef_cov", "variance_a", "variance_b"],
        keep="last"
    )
    df_query_tsc = df_query_tsc.reset_index(drop=True)
    df_query_tsc = df_query_tsc.reset_index()

    if len(df_query_tsc) == 0:
        return None

    df_query_tsc.loc[:,"coef_mean"] = df_query_tsc["coef_mean"].apply(
        lambda x: np.fromstring(
            x.replace('\n','').replace('[','').replace(']','').strip(), 
            sep=','
        )
    )

    # print("COEF MEAN")
    # print(df_query_tsc.loc[:,"coef_mean"])
    # print(len(df_query_tsc.loc[0,"coef_mean"]))

    length = len(df_query_tsc.loc[0,"coef_mean"])

    df_query_tsc.loc[:,"coef_cov"] = df_query_tsc["coef_cov"].apply(
        lambda x: np.fromstring(
            x.replace('\n','').replace('[','').replace(']','').strip(), 
            sep=','
        )
    ).apply(
        lambda x: x.reshape(length, length)
    )

    all_evaluation_df = []
    for (idx, row) in df_query_tsc.iterrows():
        formula = row['regression_formula'].strip()
        all_vars_str = formula.split('~')[1].strip()
        dependent_var = formula.split('~')[0].strip()
        vars_list = all_vars_str.split('+')
        vars_list = ["INTERCEPT"] + list(map(str.strip, vars_list))

        mean = row['coef_mean']
        cov = row['coef_cov']
        variance_a = row['variance_a']
        variance_b = row['variance_b']

        precesion_draws = invgamma.rvs(variance_a, 0, variance_b, size=100)

        #Calculate coef draw for each precesion draw
        coef_draws = np.array([np.random.multivariate_normal(mean, p * cov) for p in precesion_draws])

        columns = [order_by, "term", "coef_mean", "lower_bound", "upper_bound", "trail"]
        
        evaluation_df = pd.DataFrame(columns=columns)
        for sample_ind in range(coef_draws.shape[1]):
            samples = coef_draws[sample_ind]
            sample_coef_mean, sample_lower_ci, sample_upper_ci = mean_confidence_interval_quantile(samples)
            sample_evaluation = {
                order_by: row["arm_assign_time"] if order_by == "By time" else row["Index"],
                "trail": idx,
                "term": vars_list[sample_ind],
                "coef_mean": float(sample_coef_mean),
                "lower_bound": float(sample_lower_ci),
                "upper_bound": float(sample_upper_ci)
            }

            evaluation_df = pd.concat([evaluation_df, pd.DataFrame.from_records([sample_evaluation])])

        all_evaluation_df.append(evaluation_df)

    all_evaluation = pd.concat(all_evaluation_df)

    return all_evaluation
