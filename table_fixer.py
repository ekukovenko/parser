import pandas as pd

# data = "dogs_dataset.csv"
#
# df = pd.read_csv(data)
#
# def fix_description(value):
#     if not isinstance(value, str):
#         return "собака"
#     return value
#
# df['description'] = df['description'].apply(fix_description)
#
# df.to_csv("corrected_dogs_dataset.csv", index=False)



data2 = "corrected_dogs_dataset.csv"

df2 = pd.read_csv(data2)

df2['description_length'] = df2['description'].apply(lambda x: len(str(x)))

df2.to_csv("corrected_dogs_dataset.csv", index=False)
