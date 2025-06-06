import pandas as pd
import numpy as np
from catboost import CatBoostRegressor
import os


def generate_features(df, days):
    import numpy as np

    data = df.copy()

    # Календарные признаки
    if 'dayofmonth' not in df.columns:
        df['dayofmonth'] = df.index.day
    if 'year' not in df.columns:
        df['year'] = df.index.year
    if 'dayofweek' not in df.columns:
        df['dayofweek'] = df.index.dayofweek
    if 'day_of_year' not in df.columns:
        df['day_of_year'] = df.index.dayofyear

    if 'quarter' not in data.columns:
        data['quarter'] = data.index.quarter
    if 'is_month_start' not in data.columns:
        data['is_month_start'] = data.index.is_month_start.astype(int)
    if 'is_month_end' not in data.columns:
        data['is_month_end'] = data.index.is_month_end.astype(int)
    if 'season' not in data.columns:
        data['season'] = (data.index.month % 12 + 3) // 3

    holiday_map = {
        '01-01': 'Новый год', '01-02': 'Новогодние каникулы', '01-03': 'Новогодние каникулы',
        '01-04': 'Новогодние каникулы', '01-05': 'Новогодние каникулы', '01-06': 'Сочельник',
        '01-07': 'Рождество', '02-14': 'День Святого Валентина', '02-23': 'День защитника Отечества',
        '03-08': 'Международный женский день', '05-01': 'Праздник Весны и Труда',
        '05-09': 'День Победы', '06-12': 'День России', '09-01': 'День знаний', '11-04': 'День народного единства'
    }

    def get_holiday_type(date):
        mm_dd = date.strftime('%m-%d')
        return holiday_map.get(mm_dd, None)

    if 'holiday_type' not in df.columns:
        df['holiday_type'] = df.index.to_series().apply(get_holiday_type).fillna('Обычный день')

    if 'is_weekend' not in df.columns:
        df['is_weekend'] = df['dayofweek'].isin([5, 6]).astype(int)

    if 'dayofyear_sin' not in data.columns:
        data['dayofyear_sin'] = np.sin(2 * np.pi * data.index.dayofyear / 365)
    if 'dayofyear_cos' not in data.columns:
        data['dayofyear_cos'] = np.cos(2 * np.pi * data.index.dayofyear / 365)

    if 'promo_temp' not in data.columns:
        data['promo_temp'] = data['promo_id'] * data['temperature']

    if 'temp_diff_3d' not in data.columns:
        data['temp_diff_3d'] = data.groupby('store_id')['temperature'].diff(3)

    if 'temp_season_avg' not in data.columns:
        data['temp_season_avg'] = data.groupby(['store_id', 'season'])['temperature'].transform('mean')
    if 'temp_deviation' not in data.columns:
        data['temp_deviation'] = data['temperature'] - data['temp_season_avg']

    data = data.sort_index()

    if 'avg_sales' in data.columns:
        data.drop('avg_sales', inplace=True, axis=1)

    if 'date_only' in data.columns:
        data.drop(columns=['date_only'], inplace=True)

    data = data.sort_values(['store_id', 'product_id', 'date']).copy()
    grouped = data.groupby(['store_id', 'product_id'])['sales']

    if 'product_avg_sales' not in data.columns:
        data['product_avg_sales'] = grouped.transform(lambda x: x.shift(1).expanding(min_periods=7).mean())

    for lag in [x for x in range(days, 365, days // 2)]:
        col = f'sales_lag_{lag}'
        if col not in data.columns:
            data[col] = np.log1p(grouped.shift(lag))

    for window in [3, 7, 14, 31, 365]:
        if f'sales_roll_mean_{window}' not in data.columns:
            data[f'sales_roll_mean_{window}'] = np.log1p(grouped.shift(1).rolling(window=window, min_periods=3).mean())
        if f'sales_roll_std_{window}' not in data.columns:
            data[f'sales_roll_std_{window}'] = np.log1p(grouped.shift(1).rolling(window=window, min_periods=3).std())
        if f'sales_roll_min_{window}' not in data.columns:
            data[f'sales_roll_min_{window}'] = np.log1p(grouped.shift(1).rolling(window=window, min_periods=3).min())
        if f'sales_roll_max_{window}' not in data.columns:
            data[f'sales_roll_max_{window}'] = np.log1p(grouped.shift(1).rolling(window=window, min_periods=3).max())

    for lag in [days, days + 14, 365]:
        col = f'promo_lag_{lag}'
        if col not in data.columns:
            data[col] = data.groupby(['store_id', 'product_id'])['promo_id'].shift(lag)

    if 'sales_pct_change_7' not in data.columns:
        data['sales_pct_change_7'] = (np.log1p(grouped.shift(days)) - np.log1p(grouped.shift(days + 7))) / np.log1p(grouped.shift(days + 7)) * 100
    if 'sales_pct_change_14' not in data.columns:
        data['sales_pct_change_14'] = (np.log1p(grouped.shift(days)) - np.log1p(grouped.shift(days + 14))) / np.log1p(grouped.shift(days + 14)) * 100
    if 'sales_pct_change_28' not in data.columns:
        data['sales_pct_change_28'] = (np.log1p(grouped.shift(days)) - np.log1p(grouped.shift(days + 28))) / np.log1p(grouped.shift(days + 28)) * 100

    if 'sales' in data.columns:
        data['sales'] = np.log1p(data['sales'])

    df['holiday_type'] = df['holiday_type'].astype('category')
    df['store_id'] = df['store_id'].astype('category')
    df['promo_id'] = df['promo_id'].astype(int)

    data = data.sort_values(['store_id', 'product_id', 'date']).copy()

    return data


def grouped_time_series_split(data, cutoff_date):
    train = data.groupby(['store_id', 'product_id']).apply(
        lambda x: x.loc[x.index < cutoff_date]
    )
    test = data.groupby(['store_id', 'product_id']).apply(
        lambda x: x.loc[x.index >= cutoff_date]
    )

    # Убираем лишние уровни индекса от groupby+apply
    train.index = train.index.droplevel([0, 1])
    test.index = test.index.droplevel([0, 1])
    return train, test

def predict_sales(file_path, period_days=14, store_id='78СМ23_ОСН', product_id=4600699503804):
    df = pd.read_csv(file_path, parse_dates=['date'], index_col='date')

    cutoff_date = df.index.max() - pd.Timedelta(days=period_days)

    train, test = grouped_time_series_split(generate_features(df, period_days), cutoff_date)

    model_path = os.path.join(os.path.dirname(__file__), f'model_{period_days}.cbm')
    model = CatBoostRegressor()
    model.load_model(model_path)

    if 'sales' in test.columns:
        X = test.drop(columns=['sales'])
    else:
        X = test

    if store_id is not None and product_id is not None:
        X = X[
            (X['store_id'].astype(str) == str(store_id)) &
            (X['product_id'].astype(str) == str(product_id))
            ]

    pred = model.predict(X)
    result = X.copy()
    result['predicted'] = np.expm1(pred)

    result.reset_index(inplace=True)
    return result
