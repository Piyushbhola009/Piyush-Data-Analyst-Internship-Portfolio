import pandas as pd
df = pd.read_excel("Internship_Dataset_Working.xlsx")
print(df.head())
print(df.columns)
print("\nMissing Values:")
print(df.isnull().sum())
df["Age"] = df["Age"].fillna(df["Age"].median())
print("\nMissing values after Age cleaning:")
print(df["Age"].isnull().sum())
df["City"] = df["City"].fillna(df["City"].mode()[0])
print("\nMissing values after City cleaning:")
print(df["City"].isnull().sum())
print("\nDuplicate records:")
print(df.duplicated().sum())
df = df.drop_duplicates()
text_columns = ["Gender", "City", "Product", "Category"]

for col in text_columns:
    df[col] = df[col].str.strip().str.title()

df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")
print("\nOrder Date data type:")
print(df["Order_Date"].dtype)
numeric_columns = ["Age", "Quantity", "Unit_Price", "Total_Sales"]

for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

Q1 = df["Total_Sales"].quantile(0.25)
Q3 = df["Total_Sales"].quantile(0.75)

IQR = Q3 - Q1

lower_limit = Q1 - 1.5 * IQR
upper_limit = Q3 + 1.5 * IQR

print("\nTotal Sales Outlier Limits:")
print("Lower Limit:", lower_limit)
print("Upper Limit:", upper_limit)

outliers = df[
    (df["Total_Sales"] < lower_limit) |
    (df["Total_Sales"] > upper_limit)
]

print("\nNumber of Total_Sales outliers:")
print(len(outliers))
def count_outliers(column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    return ((df[column] < lower) | (df[column] > upper)).sum()


print("\nOutlier Counts:")
print("Age:", count_outliers("Age"))
print("Quantity:", count_outliers("Quantity"))
print("Unit_Price:", count_outliers("Unit_Price"))
print("Total_Sales:", count_outliers("Total_Sales"))

df["Age_Group"] = pd.cut(
    df["Age"],
    bins=[0, 18, 30, 45, 60, 100],
    labels=["Under 18", "18-30", "31-45", "46-60", "60+"]
)
print("\nFinal Dataset Information:")
print(df.info())

print("\nFinal Missing Values:")
print(df.isnull().sum())

print("\nFinal Dataset:")
print(df.head())

df.to_excel("Cleaned_Internship_Dataset.xlsx", index=False)