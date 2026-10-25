import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)

rows = 5000

products = [
    "Laptop",
    "Mobile",
    "Tablet",
    "Printer",
    "Monitor",
    "Keyboard",
    "Mouse",
    "Headphones",
    "Camera",
    "Smartwatch"
]

regions = [
    "North",
    "South",
    "East",
    "West",
    "Central"
]

customer_types = [
    "Retail",
    "Corporate",
    "Online"
]


# Generate dates
dates = [
    datetime(2023,1,1) +
    timedelta(days=np.random.randint(0,730))
    for _ in range(rows)
]


product_data = np.random.choice(
    products,
    rows
)


# Category mapping

categories = []

for product in product_data:

    if product in [
        "Laptop",
        "Mobile",
        "Tablet",
        "Camera",
        "Smartwatch"
    ]:
        categories.append("Electronics")

    elif product in [
        "Printer",
        "Monitor"
    ]:
        categories.append("Office")

    else:
        categories.append("Accessories")



units_sold = np.random.randint(
    1,
    100,
    rows
)


unit_price = np.random.randint(
    500,
    80000,
    rows
)


discount = np.random.randint(
    0,
    31,
    rows
)


marketing_spend = np.random.randint(
    1000,
    50000,
    rows
)


sales = (
    units_sold *
    unit_price *
    (1 - discount/100)
    +
    marketing_spend*0.3
    +
    np.random.normal(0,5000,rows)
)


sales = np.round(
    np.maximum(sales,0),
    2
)


df = pd.DataFrame({

    "Order_ID": range(10001,10001+rows),

    "Date": dates,

    "Product": product_data,

    "Category": categories,

    "Region": np.random.choice(
        regions,
        rows
    ),

    "Customer_Type": np.random.choice(
        customer_types,
        rows
    ),

    "Units_Sold": units_sold,

    "Unit_Price": unit_price,

    "Discount": discount,

    "Marketing_Spend": marketing_spend,

    "Sales": sales

})


df.to_csv(
    "sales_forecasting_dataset_5000.csv",
    index=False
)


print("Dataset created successfully!")
print(df.head())
print("Shape:", df.shape)