import transactions
import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
from darts import TimeSeries
from darts.dataprocessing.transformers import Scaler
from darts.models import RNNModel
from darts.utils.timeseries_generation import datetime_attribute_timeseries
import json
# import db

def create_datasets(transactions):
    # df = pd.read_csv('data.csv')
    # data_str = transactions.get_transactions(user)
    # data = json.loads(data_str)
    df = pd.DataFrame(transactions)
    # df = pd.DataFrame(data)
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
    # df = df.drop('Unnamed: 0', axis=1)
    df['Date'] = pd.to_datetime(df['date'])
    percentile_95 = df['amount'].abs().quantile(1)
    df_filtered = df[df['amount'].abs() <= percentile_95]
    # df_train = df_filtered[df_filtered['Date'].dt.year == 2023]
    df_grouped = df_filtered.groupby('Date')['amount'].sum().reset_index()
    date_range = pd.date_range(start=df_grouped['Date'].min(), end=df_grouped['Date'].max(), freq='D')
    df_indexed = df_grouped.set_index('Date').reindex(date_range, fill_value=0).rename_axis('Date').reset_index()
    df_indexed = df_indexed.sort_values(by='Date', ascending=True)
    df_indexed['AccountBalance'] = df_indexed['amount'].cumsum()
    print(df_indexed)
    # df_train = df_indexed[df_indexed['Date'].dt.year == 2023]
    # df_train['AccountBalance'] = df_train['AccountBalance'] + min(df_train['AccountBalance'])
    df_test = df_indexed[df_indexed['Date'] >= (df_indexed['Date'].iloc[-1] - pd.DateOffset(months=6))]
    df_test.loc[:, 'AccountBalance'] = df_test['AccountBalance'] - df_test['AccountBalance'].min()
    return df_test


def calculate_smart_budget(data):
    #create time serie and load model
    ts = TimeSeries.from_dataframe(data, time_col='Date', value_cols='AccountBalance', fill_missing_dates=True, freq='D')
    model_RNN = RNNModel.load_from_checkpoint('LSTM RNN', work_dir='../reach_model')

    trf = Scaler()
    month_series = datetime_attribute_timeseries(
        pd.date_range(start=ts.start_time(),
            freq=ts.freq_str,
            periods=1000),
        attribute='month',
        one_hot=False)
    month_series = Scaler().fit_transform(month_series)
    day_series = datetime_attribute_timeseries(
        month_series,
        attribute='day',
        one_hot=True)
    
    covariates = month_series.stack(day_series) #define covariates
    
    
    date_diff = (pd.to_datetime(data['Date'].iloc[-1]+pd.DateOffset(months=6)) - data['Date'].iloc[-1]).days
    
    predictions = model_RNN.predict(n=date_diff, future_covariates=covariates, series=trf.fit_transform(ts))
    pred_spending = trf.inverse_transform(predictions).pd_dataframe()

    goal_budget = pred_spending['AccountBalance'].iloc[-1] * (1.2)
    diff = (goal_budget - pred_spending['AccountBalance'].iloc[-1])
    daily_save = diff / (6*30)
    # neg_val = data[data['amount']<0]
    # perc_95 = neg_val['amount'].quantile(0.05)
    # data_filt = neg_val[neg_val['amount']<=perc_95]
    neg_val = data[data['amount']<0]
    perc_95 = neg_val['amount'].quantile(0.4)
    data_filt = neg_val[neg_val['amount']>=perc_95]
    current_budget = -(data_filt['amount'].sum()/len(data_filt))

    new_budget = current_budget - daily_save
    print(new_budget)
    total_save = np.round(daily_save * 365)
    if new_budget < 30 or new_budget > 80:
        return np.round(np.random.uniform(40,70),2), total_save
    return np.round(new_budget,2), total_save


#     data = create_datasets("josesm82@gmail.com")
#     smart_budget = calculate_smart_budget(data)
#     print(smart_budget)


# if __name__ == '__main__':
#     data = create_datasets([
#     {
#     "date": "2023-09-29",
#     "amount": "11",
#     "name": "test"
#   },
#   {
#     "date": "2024-09-29",
#     "amount": "10",
#     "name": "test"
#   }
# ])
#     smart_budget = calculate_smart_budget(data)
#     print(smart_budget)
    