import pandas as pd

df = pd.read_excel('input.xlsx')

for column in df.columns:
    if df[column].dtype in ['int64', 'float64']:
        df[column] = df[column].fillna(df[column].mean())
    else:
        df[column] = df[column].fillna(df[column].mode()[0])

df = df.drop_duplicates()

df.to_excel('cleaned_data_output.xlsx', index=False)

print("Data cleaning completed successfully!")
print(f"Cleaned data saved to 'cleaned_data_output.xlsx'")
