import pandas as pd

data = {
    'Name': ['John', 'Alice', None, 'Bob', 'John', 'Charlie'],
    'Age': [25, 30, 28, None, 25, 35],
    'City': ['New York', None, 'London', 'Paris', 'New York', 'Tokyo'],
    'Salary': [50000, 60000, None, 70000, 50000, 80000]
}

df = pd.DataFrame(data)
df.to_excel('input.xlsx', index=False)

print("Sample input.xlsx file created with missing values and duplicates!")
