import pandas as pd
import json
from datetime import datetime
from pathlib import Path

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator


def process_data():
    airflow_volume_data_path = Path(r'./DCCAS/business_case_umbrella/dags/data')

    sales_df = pd.read_csv(f'{airflow_volume_data_path}/sales_data.csv')

    # Чтение данных о ценах из Excel
    prices_df = pd.read_excel(f'{airflow_volume_data_path}/dataprices_data.xlsx')

    # Чтение данных о скидках из JSON
    with open(f'{airflow_volume_data_path}/discounts_data.json') as f:
        discounts_dict = json.load(f)

    # Преобразование скидок в DataFrame
    discounts_df = pd.DataFrame(discounts_dict)

    # Объединение данных
    merged_df = sales_df.merge(prices_df, on='товар').merge(discounts_df, on='товар', how='left')

    # Заполнение NaN значений в колонке скидка нулями
    merged_df['скидка'] = merged_df['скидка'].fillna(0)

    # Расчет итоговой выручки
    merged_df['выручка'] = merged_df['количество проданных единиц'] * merged_df['цена'] * (1 - merged_df['скидка'])

    # Группировка по магазину и суммирование выручки
    revenue_per_store = merged_df.groupby('магазин')['выручка'].sum().reset_index()

    # Сохранение результата в CSV файл
    revenue_per_store.to_csv(f'{airflow_volume_data_path}/revenue_per_store.csv', index=False)


default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 10, 1),
}


with DAG('sales_revenue_dag', default_args=default_args, schedule_interval='@daily', catchup=False) as dag:
    start = DummyOperator(task_id="start", dag=dag)
    process_data_task = PythonOperator(
        task_id='process_data',
        python_callable=process_data,
    )
    end = DummyOperator(task_id="end", dag=dag)


# Запуск задачи
start >> process_data_task >> end
