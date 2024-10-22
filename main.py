import dogs_parser
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# parser = dogs_parser.DogsParser()
# parser.get_product_list()

data = "dogs_dataset.csv"
df = pd.read_csv(data)

# Обработка пропущенных данных по цене
df['price'] = pd.to_numeric(df['price'], errors='coerce')
df['price'] = df.groupby('breed')['price'].transform(lambda x: x.fillna(x.mean()))

# Построение scatterplot
plt.figure(figsize=(14, 8))  # Увеличиваем размер графика для большего количества точек
sns.scatterplot(
    data=df,
    x='breed',
    y='price',
    hue='rare_gen',
    style='rare_gen',
    s=70,  # Размер точек немного уменьшен для улучшения читаемости
    alpha=0.5,  # Прозрачность точек для избежания наложений
)

# Используем логарифмическую шкалу по оси Y для улучшения восприятия
plt.yscale('log')

# Настройка осей и заголовков
plt.xticks(rotation=45, ha='right')
plt.title('Зависимость цены от породы и наличия редкого гена')
plt.ylabel('Цена (логарифмическая шкала)')
plt.xlabel('Порода')
plt.tight_layout()

# Отображение графика
plt.show()