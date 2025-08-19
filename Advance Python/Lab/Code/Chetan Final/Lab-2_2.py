import pandas as pd
import os
import traceback

dir = r"files/program_2"
sales_dir = os.path.join(dir, "sales_data")
products_file = os.path.join(dir, "product_names.csv")
output_file = os.path.join(dir, "sales_summary.csv")

errors = 0

def print_error(e: Exception) -> None:
    tb = traceback.extract_tb(e.__traceback__)
    for filename, line, funcname, text in tb:
        print(f"Error -> {e}")
        print(f"File -> {filename}")
        print(f"Function -> {funcname}, Line -> {line}")
        print(f"Code -> {text}\n")
    global errors
    errors += 1

def load(sales_dir: str, products_file: str):
    sales = pd.DataFrame()
    months = 0
    try:
        for root, _, files in os.walk(sales_dir):
            for file in files:
                sales = pd.concat([sales, pd.read_csv(os.path.join(root, file))], ignore_index=True)
                months += 1
        products = pd.read_csv(products_file)
    except Exception as e:
        print_error(e)
        return None, None, 0
    return sales, products, months

def process(sales: pd.DataFrame, products: pd.DataFrame, months: int):
    try:
        totals = sales.groupby("Product_ID")["Quantity"].sum()
        products["Total"] = products["Product_ID"].map(totals).fillna(0)
        products["Average"] = (products["Total"] / months).round(2)
        top_5 = products.sort_values(by="Total", ascending=False).head(5)
        print("The top 5 products by total quantity are")
        print(top_5[["Name", "Total"]])
    except Exception as e:
        print_error(e)

def func(sales_dir: str, products_file: str, output_file: str):
    sales, products, months = load(sales_dir, products_file)
    if sales is None or products is None:
        return
    process(sales, products, months)
    try:
        products.to_csv(output_file, index=False)
    except Exception as e:
        print_error(e)

def main():
    func(sales_dir, products_file, output_file)
    if errors:
        print(f"Total number of errors occurred -> {errors}")

if __name__ == "__main__":
    main()
