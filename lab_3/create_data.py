import pandas as pd
import json
from pathlib import Path


airflow_volume_data_path = Path(r'./DCCAS/business_case_umbrella/dags/data')

# Данные о продажах
sales_data = {
    'товар': ['Товар A', 'Товар B', 'Товар C', 'Товар A', 'Товар B'],
    'магазин': ['Магазин 1', 'Магазин 1', 'Магазин 2', 'Магазин 2', 'Магазин 1'],
    'количество проданных единиц': [10, 5, 8, 7, 6]
}

# Создание DataFrame для продаж
sales_df = pd.DataFrame(sales_data)

# Сохранение в CSV
sales_df.to_csv(f'{airflow_volume_data_path}/sales_data.csv', index=False)
print("Данные о продажах сохранены в sales_data.csv")

# Данные о ценах
prices_data = {
    'товар': ['Товар A', 'Товар B', 'Товар C'],
    'цена': [100, 200, 150]
}

# Создание DataFrame для цен
prices_df = pd.DataFrame(prices_data)

# Сохранение в Excel
prices_df.to_excel(f'{airflow_volume_data_path}/dataprices_data.xlsx', index=False, engine='openpyxl')
print("Данные о ценах сохранены в prices_data.xlsx")

# Данные о скидках
discounts_data = {
    'товар': ['Товар A', 'Товар B'],
    'скидка': [0.1, 0.2]  # скидки в процентах
}

# Сохранение данных о скидках в JSON
with open(f'{airflow_volume_data_path}/discounts_data.json', 'w') as json_file:
    json.dump(discounts_data, json_file)
print("Данные о скидках сохранены в discounts_data.json")
