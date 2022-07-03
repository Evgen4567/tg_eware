from typing import TypeVar

import pandas as pd
import numpy as np
import arrow
from pydantic import BaseModel, Field

from data.ozon_methods import get_warehouses_data, get_orders_data


PandasDataFrame = TypeVar('pandas.core.frame.DataFrame')


class StatWarehouse(BaseModel):
    data_ekb: PandasDataFrame = Field(title="prepare_ekb")
    data_msk: PandasDataFrame = Field(title="prepare_msk")


ekb_wh_name = "ЕКАТЕРИНБУРГ"
msk_wh_name = "ХОРУГВИНО"
dict_optimal_wh_value = {ekb_wh_name: 3, msk_wh_name: 5}
koeff_dict = {1: 1.3, 2: 1.3, 3: 1.3, 4: 1.2, 5: 1.1, 6: 1.1, 7: 1.1, 8: 1.1, 9: 1.2, 10: 1.3, 11: 1.4, 12: 1.4}


def filter_orders(df, warehouse, count_months=1, status_filter=('cancelled',)):
    data_filter = int(arrow.utcnow().shift(months=-count_months).timestamp())
    return df[
        (df.order_datetime > data_filter) & ~df.status.isin(status_filter) & df.warehouse.str.contains(warehouse)
    ].reset_index(drop=True)


def filter_wh(df, warehouse):
    return df[df.warehouse_name.str.contains(warehouse)].reset_index(drop=True)


def get_stat_by_wh(orders_df, wh_df, warehouse_name):
    orders_wh = filter_orders(orders_df, warehouse_name).groupby(
        ['name', 'artikul']
    )[['quantity']].agg('sum').reset_index()

    orders_wh.columns = ['name', 'artikul', 'saled']
    wh_by_name = filter_wh(wh_df, warehouse_name)
    wh_by_name.columns = ['warehouse_name', 'name', 'artikul', 'in_ozon']
    df = pd.merge(orders_wh, wh_by_name, on="artikul", how="outer").sort_values("artikul")
    df.name_y.fillna(df.name_x, inplace=True)
    df['optimal'] = float(dict_optimal_wh_value[warehouse_name])
    df = df[['warehouse_name', 'artikul', 'name_y', 'optimal', 'in_ozon', 'saled']].fillna(0).reset_index(drop=True)
    df.columns = ['warehouse_name', 'artikul', 'name', 'optimal', 'in_ozon', 'saled']
    df.warehouse_name = warehouse_name
    return df.fillna(0)


def prepare_to_buy(df, number_month: int = 5):
    koeff = koeff_dict[number_month]
    df['to_buy'] = 0.0
    df['after_delivery'] = 0.0

    df.to_buy = ((df.saled * koeff).apply(np.ceil) - df.in_ozon).clip(lower=0.0)
    df.after_delivery = df.in_ozon + df.to_buy

    df[df.after_delivery < df.optimal].to_buy = (df.optimal - df.after_delivery + df.to_buy).clip(lower=0.0)
    df[df.after_delivery < df.saled].to_buy = (df.saled * koeff - df.in_ozon).clip(lower=0.0)
    df.drop(columns=["after_delivery"], inplace=True)
    return df


def get_prepared_data(df_orders, df_wh, wh_name):
    stat = get_stat_by_wh(df_orders, df_wh, wh_name)
    return prepare_to_buy(stat, arrow.now().month)


def get_data_by_warehouse() -> StatWarehouse:
    wh_data = get_warehouses_data()
    orders = get_orders_data()

    df_wh = pd.DataFrame([s.__dict__ for s in wh_data])
    df_wh.warehouse_name = df_wh.warehouse_name.str.upper()

    df_orders = pd.DataFrame([s.__dict__ for s in orders])
    df_orders['order_datetime'] = df_orders['order_datetime'].astype('datetime64[ns]')
    df_orders['order_datetime'] = (df_orders['order_datetime'] - pd.Timestamp(0)) // pd.Timedelta('1s')

    data_ekb = get_prepared_data(df_orders, df_wh, ekb_wh_name)
    data_msk = get_prepared_data(df_orders, df_wh, msk_wh_name)

    return StatWarehouse(data_ekb=data_ekb, data_msk=data_msk)


if __name__ == '__main__':
    import warnings
    with warnings.catch_warnings(record=True):
        data = get_data_by_warehouse()
        data.data_ekb.to_excel('prepare_ekb.xlsx', index=False)
        data.data_msk.to_excel('prepare_msk.xlsx', index=False)
