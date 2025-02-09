from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd
import time


# Укажите путь к chromedriver
chrome_driver_path = "/home/dba/.wdm/drivers/chromedriver/linux64/129.0.6668.58/chromedriverlinux64/chromedriver"

# Шаг 1: Настройка драйвера Selenium
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

# Шаг 2: Открытие страницы
url = "https://www.insurancejournal.com/top-100-insurance-agencies/"
driver.get(url)

# Шаг 3: Ждем несколько секунд для загрузки страницы
time.sleep(5)

# Шаг 4: Находим все элементы списка агентств
ranks = []
agency_names = []
pc_revenues = []
other_revenues = []
offices = []
agency_list = driver.find_elements(By.CLASS_NAME, 'rankings-agency-list-item')

# Шаг 5: В цикле извлекает Ранг, Название, P\C Revenue, Other Revenue и Офис
for agency in agency_list:
 rank = agency.find_element(By.CLASS_NAME, 'agency-rank').text.strip()
 ranks.append(rank)

 name = agency.find_element(By.CLASS_NAME, 'agency-name').text.strip()
 agency_names.append(name)

 pc_revenue = agency.find_element(By.CLASS_NAME, 'agencyrevenue').text.strip().replace('P\C REVENUE\n', '').strip()
 pc_revenues.append(pc_revenue)

 # Извлечение Other Revenue (если отсутствует, добавляем None)
try:
    other_revenue = agency.find_element(By.CLASS_NAME, 'agency-otherrevenue').text.strip().replace('OTHER REVENUE\n', '').strip()
except:
    other_revenue = None
    other_revenues.append(other_revenue)

    office = agency.find_element(By.CLASS_NAME, 'agencyoffice').text.strip().replace('OFFICE', '').strip()
    offices.append(office)

# Шаг 6. Создание DataFrame
data = {
 'Rank': ranks,
 'Agency Name': agency_names,
 'P/C Revenue': pc_revenues,
 'Other Revenue': other_revenues,
 'Office': offices
}
df = pd.DataFrame(data)
print(df.head())

# Шаг 7. Закрытие драйвера
driver.quit()
