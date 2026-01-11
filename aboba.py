import json


def to_cell(cell_type, source):
    return {
        "cell_type": cell_type,
        "metadata": {},
        "source": [line + "\n" for line in source.split("\n")],
        "outputs": [],
        "execution_count": None
    } if cell_type == "code" else {
        "cell_type": cell_type,
        "metadata": {},
        "source": [line + "\n" for line in source.split("\n")]
    }


md1 = "# Итоговое тестирование"
md2 = "Загрузите файл `salary_fix.csv`. \n\nКодировка: `CP1251`, разделители: `«;»`."
md3 = """В файле представлены данные о заработной плате профессорско-преподавательского состава университета:

|Поле|Содержание|
|:-|:-|
|`'Т/Н'`|табельный номер, уникальный идентификатор работника
|`'Должность'`|должность работника (одна из занимаемых должностей)
|`'Ставка'`|часть ставки, на которую заключен трудовой договор по данной должности в данном подразделении
|`'Оклад (основной)'`|
|`'Оклад (совместительство)'`|
|`'Почасовая оплата'`|Сумма почасовой оплаты труда (обычно сверх оклада)
|`'Итого'`|общая сумма заработной платы"""
md4 = """Обратите внимание, сотрудники идентифицируются по табельному номеру, на некоторых работников есть несколько записей – у них есть внутреннее совместительство.

Существуют сотрудники, у которых есть зарплата только по основному месту работы, есть основное и внутреннее совместительство - это штатные сотрудники. Есть внешние совместители – у них нет оклада по основному месту работы в данной организации.

Необходимо написать программу на Python с использованием модулей `Pandas` и `Pyplot`, которая позволяет получить аналитику данных."""
md5 = """1. (1 балл) Выведите Фонд оплаты труда(ФОТ):

a) всей организации (`r1a`)

b) в разрезе должностей (`r1b`)

c) ФОТ организации без учёта внешних совместителей (`r1c`)

d) ФОТ внешних совместителей (`r1d`)."""

code1 = """import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline

# Загрузка данных
# Согласно заданию используется CP1251. 
try:
    df = pd.read_csv('salary_fix.csv', encoding='cp1251', sep=';', decimal=',')
except:
    df = pd.read_csv('salary_fix.csv', encoding='utf-8', sep=';', decimal=',')

df = df.fillna(0)

# a) всей организации
r1a = df['Итого'].sum()
print(f"ФОТ организации: {r1a:.2f}")

# b) в разрезе должностей
r1b = df.groupby('Должность')['Итого'].sum()
print("\\nФОТ по должностям:")
print(r1b)

# Identify categories
# Группируем по ТН. Если сумма оклада (основного) > 0 -> Штатный, иначе -> Внешний
salary_main = df.groupby('ТН')['Оклад (основной)'].sum()
staff_tns = salary_main[salary_main > 0].index
external_tns = salary_main[salary_main == 0].index

# c) ФОТ без внешних совместителей
r1c = df[df['ТН'].isin(staff_tns)]['Итого'].sum()
print(f"\\nФОТ без внешних совместителей: {r1c:.2f}")

# d) ФОТ внешних совместителей
r1d = df[df['ТН'].isin(external_tns)]['Итого'].sum()
print(f"ФОТ внешних совместителей: {r1d:.2f}")"""

md6 = "2. (1 балл) Выведите данные о структуре персонала по должностям и ставкам и постройте круговую диаграмму"
code2 = """pos_counts = df['Должность'].value_counts()
print("1. Количество сотрудников по должностям (Топ-5 для примера):")
print(pos_counts.head())
print("-" * 30)

# Метод describe() выводит count, mean, std, min, 25%, 50%, 75%, max
rate_stats = df['Ставка'].describe()
print("2. Статистика по ставкам:")
print(rate_stats)
print("-" * 30)

bins = [0, 0.25, 0.50, 0.75, 1.0, float('inf')]
labels = ['до 0.25', '0.25 - 0.50', '0.50 - 0.75', '0.75 - 1.00', 'более 1.00']

df['Диапазон_ставок'] = pd.cut(df['Ставка'], bins=bins, labels=labels, right=True)

range_distribution = df['Диапазон_ставок'].value_counts().sort_index()

print("3. Распределение по диапазонам (Название диапазона, Count):")
print(range_distribution)
print("-" * 30)

fig, axes = plt.subplots(1, 2, figsize=(16, 7))

top_10 = pos_counts.head(10)
if len(pos_counts) > 10:
    others = pd.Series([pos_counts.iloc[10:].sum()], index=['Другие'])
    data_pie = pd.concat([top_10, others])
else:
    data_pie = top_10

axes[0].pie(data_pie, labels=data_pie.index, autopct='%1.1f%%', startangle=90)
axes[0].set_title('Распределение сотрудников по должностям')

range_distribution.plot(kind='bar', ax=axes[1], color='skyblue', edgecolor='black')
axes[1].set_title('Распределение записей по диапазонам ставок')
axes[1].set_xlabel('Диапазон ставок')
axes[1].set_ylabel('Количество')
axes[1].tick_params(axis='x', rotation=45)

for i, v in enumerate(range_distribution):
    axes[1].text(i, v + 0.5, str(v), ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.show()"""

md7 = """3. (1 балл) Проанализируйте заработную плату ассистентов:

- выведите минимальную (`r3a`)
- среднюю (`r3b`)
- максимальную заработную плату (`r3c`)

по этой категории"""
code3 = """assistants = df[df['Должность'].str.lower().str.contains('ассистент')]
r3a = assistants['Итого'].min()
r3b = assistants['Итого'].mean()
r3c = assistants['Итого'].max()

print(f"Минимальная: {r3a:.2f}")
print(f"Средняя: {r3b:.2f}")
print(f"Максимальная: {r3c:.2f}")"""

md8 = """4. (1 балл) Проанализируйте доцентов-внешних совместителей. Выведите таблицу с их группировкой по табельному номеру, представьте в таблице общую величину ставки и сумму заработной платы (DataFrame `r4a` с `columns=['Ставка', 'Итого']`). 

Выведите их численность с учётом группировки – `r4b`."""
code4 = """docents_ext = df[
    (df['Должность'].str.lower().str.contains('доцент')) & 
    (df['ТН'].isin(external_tns))
]

# Группировка по ТН
r4a = docents_ext.groupby('ТН')[['Ставка', 'Итого']].sum()
print("Таблица доцентов-внешних совместителей:")
print(r4a)

r4b = len(r4a)
print(f"\\nЧисленность: {r4b}")"""

md9 = "5. (1 балл) Проанализируйте заработную плату работников (с учётом совместительства), работающих в данной организации по основному месту работы. Выведите минимальную (`r5a`), среднюю (`r5b`) и максимальную заработную плату (`r5c`) по этой категории."
code5 = """# Агрегируем Итого по ТН для основных сотрудников
staff_df = df[df['ТН'].isin(staff_tns)]
staff_totals = staff_df.groupby('ТН')['Итого'].sum()

r5a = staff_totals.min()
r5b = staff_totals.mean()
r5c = staff_totals.max()

print(f"Минимальная (основные): {r5a:.2f}")
print(f"Средняя (основные): {r5b:.2f}")
print(f"Максимальная (основные): {r5c:.2f}")"""

md10 = "6. (1 балл) Проведите анализ ставок внешних совместителей: выведите минимальную (`r6a`), среднюю (`r6b`) и максимальную ставку (`r6c`) по этой категории."
code6 = """ext_df = df[df['ТН'].isin(external_tns)]
# Агрегируем ставки по сотрудникам
ext_rates = ext_df.groupby('ТН')['Ставка'].sum()

r6a = ext_rates.min()
r6b = ext_rates.mean()
r6c = ext_rates.max()

print(f"Минимальная ставка (внешние): {r6a:.2f}")
print(f"Средняя ставка (внешние): {r6b:.2f}")
print(f"Максимальная ставка (внешние): {r6c:.2f}")"""

md11 = "7. (1 балл) Выведите список табельных номеров доцентов, работающих на 1,0 ставку (`r7a`)"
code7 = """docents = df[df['Должность'].str.lower().str.contains('доцент')]
docent_rates = docents.groupby('ТН')['Ставка'].sum()
# Используем isclose для сравнения float
r7a = docent_rates[np.isclose(docent_rates, 1.0)].index.tolist()

print("Табельные номера доцентов на 1.0 ставку:")
print(r7a)"""

md12 = "8. (1 балл) Найдите самых незагруженных по основному месту работы сотрудников и выведите их табельные номера и ставку (`r8a`)."
code8 = """# Минимальная суммарная ставка среди основных
staff_rates = staff_df.groupby('ТН')['Ставка'].sum()
min_rate = staff_rates.min()
r8a = staff_rates[np.isclose(staff_rates, min_rate)]

print(f"Минимальная ставка: {min_rate}")
print("Сотрудники:")
print(r8a)"""

md13 = """9. (2 балла) Постройте графики формирования ФОТ от меньших зарплат к большим для:

а) всей организации;

б) работников, чьё основное место работы находится в организации (с учётом внутреннего совместительства);

в) внешних совместителей."""
code9 = """# Сортируем суммарные зарплаты
all_totals_sorted = df.groupby('ТН')['Итого'].sum().sort_values().values
main_totals_sorted = staff_totals.sort_values().values
ext_totals_sorted = df[df['ТН'].isin(external_tns)].groupby('ТН')['Итого'].sum().sort_values().values

plt.figure(figsize=(18, 5))

plt.subplot(1, 3, 1)
plt.plot(all_totals_sorted)
plt.title('ФОТ: Вся организация')
plt.xlabel('Ранг (сотрудники)')
plt.ylabel('Зарплата (сумма)')
plt.grid(True)

plt.subplot(1, 3, 2)
plt.plot(main_totals_sorted, color='green')
plt.title('ФОТ: Основные сотрудники')
plt.xlabel('Ранг')
plt.grid(True)

plt.subplot(1, 3, 3)
plt.plot(ext_totals_sorted, color='red')
plt.title('ФОТ: Внешние совместители')
plt.xlabel('Ранг')
plt.grid(True)

plt.tight_layout()
plt.show()"""

cells = [
    to_cell("markdown", md1),
    to_cell("markdown", md2),
    to_cell("markdown", md3),
    to_cell("markdown", md4),
    to_cell("markdown", md5),
    to_cell("code", code1),
    to_cell("markdown", md6),
    to_cell("code", code2),
    to_cell("markdown", md7),
    to_cell("code", code3),
    to_cell("markdown", md8),
    to_cell("code", code4),
    to_cell("markdown", md9),
    to_cell("code", code5),
    to_cell("markdown", md10),
    to_cell("code", code6),
    to_cell("markdown", md11),
    to_cell("code", code7),
    to_cell("markdown", md12),
    to_cell("code", code8),
    to_cell("markdown", md13),
    to_cell("code", code9),
]

notebook = {
    "cells": cells,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "codemirror_mode": {
                "name": "ipython",
                "version": 3
            },
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbconvert_exporter": "python",
            "pygments_lexer": "ipython3",
            "version": "3.8.5"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

with open('result.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=1, ensure_ascii=False)
